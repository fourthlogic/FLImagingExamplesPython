# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 뷰 선언 # Declare image view
	viewImage = [CGUIViewImage() for _ in range(3)]

	while True:

		# 이미지 뷰 생성 # Create image views
		for i in range(3):
			if (res := viewImage[i].Create(200 + i * 500, 0, 700 + i * 500, 500)).IsFail():
				ErrorPrint(res, "Failed to create the image view.\n")
				break

		if res.IsFail():
			break

		# 각 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoint of each image view.
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail() or \
			(res := viewImage[1].SynchronizePointOfView(viewImage[2])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view\n")
			break

		# 각 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the position of each image view window
		if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail() or \
			(res := viewImage[1].SynchronizeWindow(viewImage[2])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window.\n")
			break

		# 곡선 y = 0.004 * (x - 250)^2 + 200 위의 점들에 노이즈를 추가하여 데이터 생성
		# Generate data by adding noise to points on the curve y = 0.004 * (x - 250)^2 + 200
		flpaData = CFLPointArray()

		for i in range(41):
			f64X = 50.0 + i * 10.0
			f64Y = 0.004 * (f64X - 250.0) * (f64X - 250.0) + 200.0 + CRandomGenerator.Double(-5.0, 5.0)

			# 일부 점은 곡선에서 크게 벗어나도록 만든다. # Make some points deviate greatly from the curve.
			if i == 6:
				f64Y -= 90.0
			elif i == 20:
				f64Y += 110.0
			elif i == 33:
				f64Y += 100.0

			# 일부 점은 곡선에서 조금 벗어나도록 만든다. (임계값이 작을 때만 제외됨)
			# Make some points deviate slightly from the curve. (Excluded only when the threshold is small)
			if i == 13:
				f64Y -= 25.0
			elif i == 27:
				f64Y += 25.0

			flpaData.PushBack(CFLPoint[Double](f64X, f64Y))

		# CLeastSquares<double> 객체 생성 # Create CLeastSquares<double> object
		leastSquares = CLeastSquares[Double]()

		# 데이터를 할당 # Assign data
		if (res := leastSquares.Assign(flpaData)).IsFail():
			ErrorPrint(res, "Failed to assign data.\n")
			break

		# 피팅할 다항식의 차수 # Degree of the polynomial to fit
		i32Degree = 2

		# 각 뷰에서 사용할 Outlier 파라미터 # Outlier parameters for each view
		arrStrViewName = ["Default", "Parameter 1", "Parameter 2"]
		arrI64OutlierThresholdCount = [0, 1, 3]
		arrF64OutlierThreshold = [3.0, 3.0, 1.5]

		print("Source Points")
		print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaData)}\n")

		for i in range(3):
			# 계수 값을 받기 위해 List 생성 # Create List to receive coefficient values
			listCoef = List[Double]()
			# R square 값을 받기 위해 변수 선언 # Declare variable to receive R square value
			f64RSquare = 0.0
			# 제외된 Outlier 점들의 인덱스를 받기 위해 List 생성 # Create List to receive the indices of excluded outlier points
			listOutlierIndices = List[Int64]()

			# 다항식 계수를 얻는다. (내림차순 : a, b, c → y = ax^2 + bx + c)
			# Get polynomial coefficients. (Descending order : a, b, c -> y = ax^2 + bx + c)
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			res, listCoef, f64RSquare, listOutlierIndices = leastSquares.GetPoly(i32Degree, listCoef, f64RSquare, ECoefficientOrder.Descending, ELeastSqauresAccuracy.TemplateType, arrI64OutlierThresholdCount[i], arrF64OutlierThreshold[i], listOutlierIndices)

			if res.IsFail():
				ErrorPrint(res, "Failed to calculate.\n")
				break

			# Outlier 인덱스로 Outlier PointArray 생성 # Create Outlier PointArray from the outlier indices
			flpaOutlier = CFLPointArray()

			for i64Index in listOutlierIndices:
				flpaOutlier.PushBack(flpaData.GetAt(i64Index))

			# 얻어온 계수로 곡선을 계산하여 짧은 선분들로 표현 # Calculate the curve with the obtained coefficients and represent it with short line segments
			flfaCurve = CFLFigureArray()
			f64PrevX = 0.0
			f64PrevY = 0.0

			for x in range(30, 471, 4):
				f64X = float(x)
				f64Y = 0.0

				for f64Coef in listCoef:
					f64Y = f64Y * f64X + f64Coef

				if x != 30:
					flfaCurve.PushBack(CFLLine[Double](f64PrevX, f64PrevY, f64X, f64Y))

				f64PrevX = f64X
				f64PrevY = f64Y

			# 화면에 출력하기 위해 Image View 에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
			layer = viewImage[i].GetLayer(0)

			if arrI64OutlierThresholdCount[i] != 0:
				strParameter = f"Outlier Threshold Count : {arrI64OutlierThresholdCount[i]}\r\nOutlier Threshold : {arrF64OutlierThreshold[i]:.3f}"
			else:
				strParameter = f"Outlier Threshold Count : {arrI64OutlierThresholdCount[i]}"

			strResult = f"y = {listCoef[0]:.6f}x^2 {listCoef[1]:+.6f}x {listCoef[2]:+.6f}\r\nR square : {f64RSquare:.6f}\r\nOutlier Count : {listOutlierIndices.Count}"

			# 레이어에 Figure 와 Text 를 출력 # Draw Figure and Text to the layer
			# 피팅 결과 곡선 : CYAN, 데이터 : LIME, 제외된 Outlier 점 : RED
			# Fitted curve : CYAN, Data : LIME, Excluded outlier points : RED
			layer.DrawFigureImage(flfaCurve, EColor.BLACK, 5)
			layer.DrawFigureImage(flfaCurve, EColor.CYAN, 3)
			layer.DrawFigureImage(flpaData, EColor.BLACK, 3)
			layer.DrawFigureImage(flpaData, EColor.LIME, 1)
			layer.DrawFigureImage(flpaOutlier, EColor.RED, 1)
			layer.DrawTextCanvas(CFLPoint[Int32](0, 0), arrStrViewName[i], EColor.YELLOW, EColor.BLACK, 30)
			layer.DrawTextCanvas(CFLPoint[Int32](0, 40), strParameter, EColor.YELLOW, EColor.BLACK, 15)
			layer.DrawTextCanvas(CFLPoint[Int32](0, 80), strResult, EColor.YELLOW, EColor.BLACK, 15)

			# Console 출력 # Console output
			print(f"[{arrStrViewName[i]}]")
			print(strParameter)
			print(f"{strResult}\n")

		if res.IsFail():
			break

		# 이미지 뷰들을 갱신 합니다. # Update the image views.
		for i in range(3):
			viewImage[i].Invalidate(True)

		# 이미지 뷰가 셋중에 하나라도 꺼지면 종료로 간주 # Consider closed when any of the three image views are turned off
		while viewImage[0].IsAvailable() and viewImage[1].IsAvailable() and viewImage[2].IsAvailable():
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
