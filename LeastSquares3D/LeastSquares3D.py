# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

import math

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare 3D view
	view3D = [CGUIView3D(), CGUIView3D()]

	while True:

		# 3D 뷰 생성 # Create 3D views
		if (res := view3D[0].Create(100, 0, 700, 600)).IsFail() or \
			(res := view3D[1].Create(700, 0, 1300, 600)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# 곡선 (100s, 40sin(πs), 20s^2), s = 0 ~ 1 위의 점들에 노이즈를 추가하여 데이터 생성
		# Generate data by adding noise to points on the curve (100s, 40sin(πs), 20s^2), s = 0 ~ 1
		flpaData = CFLPointArray3[Double]()

		for i in range(41):
			f64S = i / 40.0
			f64X = 100.0 * f64S + CRandomGenerator.Double(-1.0, 1.0)
			f64Y = 40.0 * math.sin(math.pi * f64S) + CRandomGenerator.Double(-1.0, 1.0)
			f64Z = 20.0 * f64S * f64S + CRandomGenerator.Double(-1.0, 1.0)

			# 일부 점은 곡선에서 크게 벗어나도록 만든다. # Make some points deviate greatly from the curve.
			if i == 8:
				f64Z += 25.0
			elif i == 22:
				f64Y -= 30.0
			elif i == 35:
				f64Z -= 25.0

			flpaData.PushBack(CFLPoint3[Double](f64X, f64Y, f64Z))

		# CLeastSquares3D<double> 객체 생성 # Create CLeastSquares3D<double> object
		leastSquares3D = CLeastSquares3D[Double]()

		# 데이터를 할당 # Assign data
		if (res := leastSquares3D.Assign(flpaData)).IsFail():
			ErrorPrint(res, "Failed to assign data.\n")
			break

		# 피팅할 다항식의 차수 # Degree of the polynomial to fit
		i32Degree = 3

		# 결과 점을 얻을 매개변수 t 목록 (-0.3 ~ 1.3, 0.01 간격)
		# 데이터의 t 는 누적 거리 비율(0 ~ 1)로 지정되므로, 범위 밖의 t 는 데이터 끝부분 너머의 점을 추정합니다.
		# List of parameter t to get result points (-0.3 to 1.3, 0.01 interval)
		# Since t of the data is the cumulative distance ratio (0 to 1), t outside the range gives points beyond the ends of the data.
		listTargetT = List[Double]()

		for i in range(-30, 131):
			listTargetT.Add(i / 100.0)

		# 각 뷰에서 사용할 Outlier 파라미터 # Outlier parameters for each view
		arrStrViewName = ["Default", "Outlier Exclusion"]
		arrI64OutlierThresholdCount = [0, 3]
		arrF64OutlierThreshold = [3.0, 3.0]

		# 점 크기 및 색상 (R, G, B) # Point size and colors (R, G, B)
		f32PointSize = 5.0
		tpColorData = TPoint3[Byte](0, 255, 255)    # CYAN
		tpColorOutlier = TPoint3[Byte](255, 0, 0)   # RED
		tpColorInside = TPoint3[Byte](0, 255, 0)    # LIME
		tpColorOutside = TPoint3[Byte](0, 0, 255)   # BLUE

		for i in range(2):
			# 각 축의 다항식 계수를 얻는다. (x(t), y(t), z(t), 내림차순)
			# Get polynomial coefficients of each axis. (x(t), y(t), z(t), descending order)
			listCoefX = List[Double]()
			listCoefY = List[Double]()
			listCoefZ = List[Double]()
			listOutlierIndices = List[Int64]()

			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			res, listCoefX, listCoefY, listCoefZ, listOutlierIndices = leastSquares3D.GetParametricPoly(i32Degree, listCoefX, listCoefY, listCoefZ, ECoefficientOrder.Descending, arrI64OutlierThresholdCount[i], arrF64OutlierThreshold[i], listOutlierIndices)

			if res.IsFail():
				ErrorPrint(res, "Failed to calculate.\n")
				break

			# 매개변수 t 에 대한 결과 점들을 얻는다. # Get result points for parameter t
			flpaResult = CFLPointArray3[Double]()

			res, flpaResult = leastSquares3D.GetParametricPoints(i32Degree, listTargetT, flpaResult, arrI64OutlierThresholdCount[i], arrF64OutlierThreshold[i])

			if res.IsFail():
				ErrorPrint(res, "Failed to calculate.\n")
				break

			# 결과 점 : 데이터 범위(t = 0 ~ 1) 안은 LIME, 밖은 BLUE
			# Result points : LIME inside the data range (t = 0 to 1), BLUE outside
			listResultVertices = List[TPoint3[Single]]()
			listResultColors = List[TPoint3[Byte]]()

			for j in range(flpaResult.GetCount()):
				flpResult = flpaResult.GetAt(j)
				f64T = listTargetT[j]
				bInside = 0.0 <= f64T <= 1.0

				listResultVertices.Add(TPoint3[Single](flpResult.x, flpResult.y, flpResult.z))
				listResultColors.Add(tpColorInside if bInside else tpColorOutside)

			# 데이터 점 : CYAN, 제외된 Outlier 점 : RED # Data points : CYAN, Excluded outlier points : RED
			listDataVertices = List[TPoint3[Single]]()
			listDataColors = List[TPoint3[Byte]]()

			for j in range(flpaData.GetCount()):
				flpData = flpaData.GetAt(j)

				listDataVertices.Add(TPoint3[Single](flpData.x, flpData.y, flpData.z))
				listDataColors.Add(tpColorData)

			for i64Index in listOutlierIndices:
				listDataColors[int(i64Index)] = tpColorOutlier

			# 점 크기를 지정하여 3D 뷰에 점들을 추가 # Add points to the 3D view with the specified point size
			view3DObjectResult = CGUIView3DObject(CFL3DObject(listResultVertices, listResultColors))
			view3DObjectResult.SetPointSize(f32PointSize)

			view3DObjectData = CGUIView3DObject(CFL3DObject(listDataVertices, listDataColors))
			view3DObjectData.SetPointSize(f32PointSize)

			if (res := view3D[i].PushObject(view3DObjectResult)).IsFail() or \
				(res := view3D[i].PushObject(view3DObjectData)).IsFail():
				ErrorPrint(res, "Failed to push the object.\n")
				break

			# 화면에 출력하기 위해 View 에서 레이어 0번을 얻어옴 # Obtain layer number 0 from view for display
			# 이 객체는 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to a view and does not need to be released separately
			layer = view3D[i].GetLayer(0)

			if arrI64OutlierThresholdCount[i] != 0:
				strParameter = f"Outlier Threshold Count : {arrI64OutlierThresholdCount[i]}, Outlier Threshold : {arrF64OutlierThreshold[i]:.3f}"
			else:
				strParameter = f"Outlier Threshold Count : {arrI64OutlierThresholdCount[i]}"

			strOutlierCount = f"Outlier Count : {listOutlierIndices.Count}"

			layer.DrawTextCanvas(CFLPoint[Double](0, 0), arrStrViewName[i], EColor.YELLOW, EColor.BLACK, 20)
			layer.DrawTextCanvas(CFLPoint[Double](0, 30), strParameter, EColor.YELLOW, EColor.BLACK, 13)
			layer.DrawTextCanvas(CFLPoint[Double](0, 50), strOutlierCount, EColor.YELLOW, EColor.BLACK, 13)
			layer.DrawTextCanvas(CFLPoint[Double](0, 70), "Data : CYAN, Outlier : RED", EColor.YELLOW, EColor.BLACK, 13)
			layer.DrawTextCanvas(CFLPoint[Double](0, 90), "Result (t = 0 ~ 1) : LIME, Result (extrapolated) : BLUE", EColor.YELLOW, EColor.BLACK, 13)

			# Console 출력 # Console output
			print(f"[{arrStrViewName[i]}]")
			print(strParameter)
			print(strOutlierCount)

			arrStrAxis = ["x", "y", "z"]
			arrListCoef = [listCoefX, listCoefY, listCoefZ]

			for k in range(3):
				listCoef = arrListCoef[k]
				print(f"{arrStrAxis[k]}(t) = {listCoef[0]:.6f}t^3 {listCoef[1]:+.6f}t^2 {listCoef[2]:+.6f}t {listCoef[3]:+.6f}")

			print()

		if res.IsFail():
			break

		# 두 뷰의 시점을 맞춤 # Fit the viewpoint of the two views
		view3D[0].ZoomFit()
		view3D[0].SynchronizePointOfView(view3D[1])

		# 두 뷰를 하나의 창으로 취급 # Treat the two views as one window
		view3D[0].SynchronizeWindow(view3D[1])

		for i in range(2):
			view3D[i].Invalidate()

		# 3D 뷰가 하나라도 꺼지면 종료로 간주 # Consider closed when any of the 3D views are turned off
		while view3D[0].IsAvailable() and view3D[1].IsAvailable():
			CThreadUtilities.Sleep(1)

		break

	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
	main()
