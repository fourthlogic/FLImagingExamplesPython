# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

from numpy import byte, uint


# 메인 함수 // Main function
def main():

	# 3D 객체 선언 // Declare 3D object
	arrLearnObject = [CFL3DObject() for _ in range(3)]
	floSourceObject = CFL3DObject()

	# 3D 뷰 선언 // Declare 3D view	
	view3DDst = CGUIView3D()
	arrView3DLearn = [CGUIView3D() for _ in range(3)]
	view3DSource = CGUIView3D()

	# 알고리즘 동작 결과 // Algorithm execution result
	res = CResult()

	while True:		

		arrPath = [
			"../../ExampleImages/SurfaceMatch3DMulti/Box1.ply",
			"../../ExampleImages/SurfaceMatch3DMulti/Box2.ply",
			"../../ExampleImages/SurfaceMatch3DMulti/Cylinder.ply",
		]

		arrClassName = [
			"../../ExampleImages/SurfaceMatch3DMulti/Box1",
			"../../ExampleImages/SurfaceMatch3DMulti/Box2",
			"../../ExampleImages/SurfaceMatch3DMulti/Cylinder",
		]

		arrMaxObject = [
			1,
			1,
			3,
		]

		vertexMatch3DMultiMulti = CVertexMatch3DMulti()

		# Source 3D 뷰 생성
		if(res := view3DSource.Create(100, 500, 500, 900)).IsFail() :		
			ErrorPrint(res, "Failed to create the Source 3D view.\n")
			break
		
		# Dst 3D 뷰 생성
		if(res := view3DDst.Create(500, 500, 900, 900)).IsFail() :		
			ErrorPrint(res, "Failed to create the Destination 3D view.\n")
			break

		for i in range(3):
			# Source Object 로드 // Load the Source object
			if(res := arrLearnObject.Load(arrPath[i])).IsFail() :		
				ErrorPrint(res, "Failed to load the object file.\n")
				break

			# Learn 3D 뷰 생성
			if(res := arrView3DLearn[i].Create(100 + 400 * i, 100, 100 + 400 * (i + 1), 500)).IsFail() :			
				ErrorPrint(res, "Failed to create the Source 3D view.\n")
				break
			

			if(res := arrView3DLearn[i].PushObject(arrLearnObject[i])).IsFail() :			
				ErrorPrint(res, "Failed to display the 3D object.\n")
				break

			arrView3DLearn[i].SetShadingType(EShadingType3D.Flat)

			# Learn object 설정 // Set the learn object
			vertexMatch3DMultiMulti.SetLearnObject(arrLearnObject[i])

			# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
			if(res := vertexMatch3DMultiMulti.Learn(arrClassName[i])).IsFail() :			
				ErrorPrint(res, "Failed to learn Vertex Match 3D Multi.")
				break			

			arrView3DLearn[i].SynchronizeWindow(view3DDst)
			arrView3DLearn[i].SynchronizeWindow(view3DSource)

		
		
		if(res := floSourceObject.Load("../../ExampleImages/SurfaceMatch3DMulti/Source.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the object file.\n")
			break

		if(res := view3DSource.PushObject(floSourceObject)).IsFail() :		
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break
		
		# Source object 설정 // Set the source object
		vertexMatch3DMulti.SetSourceObject(floSourceObject)
		# Min score 설정 // Set the min score
		vertexMatch3DMulti.SetMinScore(0.3)
		# 최대 결과 개수 설정 // Set the max count of match result
		vertexMatch3DMulti.SetMaxObject(4)
		# 학습 샘플링 거리 설정 // Set the learn sampling distance
		vertexMatch3DMulti.SetLearnSamplingDistance(0.03)
		# 장면 샘플링 거리 설정 // Set the scene sampling distance
		vertexMatch3DMulti.SetSceneSamplingDistance(0.03)
		# 키포인트 비율 설정 // Set the keypoint ratio.
		vertexMatch3DMulti.SetKeypointRatio(0.5)
		# 엣지 학습 여부 설정 // Set the edge train
		vertexMatch3DMulti.EnableTrainEdge(False)
		# 배경 제거 여부 설정 // Set the background removal
		vertexMatch3DMulti.EnableBackgroundRemoval(False)
		# 클러스터링 범위 설정 // Set the clustering range
		vertexMatch3DMulti.SetClusterRange(0.02)
		# 포즈 조정 반복 횟수 설정 // Set the iteration value of pose refinement
		vertexMatch3DMulti.SetIteration(5)
		# 검출 시 사용될 탐색 방식을 설정합니다. // Set the search method to be used for detection.
		vertexMatch3DMulti.SetMaxObjectMode(CMatchBase3DMulti.EMaxObjectMode.Class)

		# 최대 결과 개수 설정 // Set the max count of match result
		for i in range(3):
			vertexMatch3DMulti.SetMaxObject(arrClassName[i], arrMaxObject[i])

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := vertexMatch3DMulti.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute Vertex Match 3D Multi.")
			break


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately		
		layer3DDst = view3DDst.GetLayer(0)
		layer3DSource = view3DSource.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer3DDst.Clear()
		layer3DSource.Clear()

		# View 정보를 디스플레이 합니다. // Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double](0, 0)

		if(res := layer3DSource.DrawTextCanvas(flp, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := layer3DDst.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		for i in range(3) :
			arrView3DLearn[i].ZoomFit()

			layer3DLearn = arrView3DLearn[i].GetLayer(0)

			layer3DLearn.Clear()

			if(res := layer3DLearn.DrawTextCanvas(flp, "Class Name" + arrClassName[i], EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
				ErrorPrint(res, "Failed to draw text.\n")
				break

		# 3D 오브젝트 뷰에 결과 Object와 비교를 위한 Source 오브젝트 디스플레이		
		listColors = floSourceObject.GetVertexColors()

		for i in range(listColors.Count) :		
			listColors[i].x = 127;
			listColors[i].y = 127;
			listColors[i].z = 127;		

		floSourceObject.SetVertexColors(listColors);

		# 3D 오브젝트 뷰에 결과 Object와 비교를 위한 Source 오브젝트 디스플레이
		if(res := view3DDst.PushObject(vertexMatch3DMulti.GetSourceObject())).IsFail():
			ErrorPrint(res, "Failed to set object on the 3D View.\n")
			break
		
		sResult = SPoseMatrixParametersMulti()

		f64ArrRotX = 0.0
		f64ArrRotY = 0.0
		f64ArrRotZ = 0.0
		f64Score = 0.0
		f64Residual = 0.0

		i64ResultCount = vertexMatch3DMulti.GetResultCount()

		if i64ResultCount == 0 :		
			ErrorPrint(res, "Failed to estimate pose matrix.\n")
			break
		
		for i in range(0, i64ResultCount) :
			floLearnTransform = CFL3DObject()
			flpTrans = CFLPoint3[Double]()
			tp3Center = TPoint3[Double]()
			tp3RotVec = TPoint3[Double]()

			# 추정된 포즈 행렬 가져오기
			res, sResult = vertexMatch3DMulti.GetResultPoseMatrix(i, sResult)

			if res.IsFail():			
				ErrorPrint(res, "Failed to estimate pose matrix.\n")
				break
			
			f64Residual = sResult.f64Residual
			f64Score = sResult.f64Score
			f64ArrRotX = sResult.tp3Angle.x
			f64ArrRotY = sResult.tp3Angle.y
			f64ArrRotZ = sResult.tp3Angle.z
			tp3RotVec.x = sResult.tp3RotationVector.x
			tp3RotVec.y = sResult.tp3RotationVector.y
			tp3RotVec.z = sResult.tp3RotationVector.z
			flpTrans.x = sResult.tp3TranslationVector.x
			flpTrans.y = sResult.tp3TranslationVector.y
			flpTrans.z = sResult.tp3TranslationVector.z

			# 추정한 포즈 결과를 Console창에 출력한다 // Print the estimated pose matrix to the console window
			Console.WriteLine(" ▷ Pose Matrix 0", i)
			Console.WriteLine("  1. R : Rotation, T : Translation\n")
			Console.WriteLine("    Class Name : {0}", sResult.strClassName
			Console.WriteLine("    Rx   : {0}", f64ArrRotX)
			Console.WriteLine("    Ry   : {0}", f64ArrRotY)
			Console.WriteLine("    Rz   : {0}", f64ArrRotZ)
			Console.WriteLine("    Rotation Vector X   : {0}", tp3RotVec.x)
			Console.WriteLine("    Rotation Vector Y   : {0}", tp3RotVec.y)
			Console.WriteLine("    Rotation Vector Z   : {0}", tp3RotVec.z)
			Console.WriteLine("    Tx   : {0}", flpTrans.x)
			Console.WriteLine("    Ty   : {0}", flpTrans.y)
			Console.WriteLine("    Tz   : {0}", flpTrans.z)
			Console.WriteLine("    Score : {0}", f64Score)
			Console.WriteLine("    Residual : {0}", f64Residual)
			Console.WriteLine("\n")

			res, floLearnTransform, tp3Center = vertexMatch3DMulti.GetResultObject(i, floLearnTransform, tp3Center)

			if res.IsFail() :			
				ErrorPrint(res, "Failed to set object on the 3d view.\n")
				break
			
			if(res := view3DDst.PushObject(floLearnTransform)).IsFail() :
			
				ErrorPrint(res, "Failed to set object on the 3d view.\n")
				break
			
			strText = String.Format("Class Name : {0}\nR({1, 6:0.000000},{2, 6:0.000000},{3, 6:0.000000})\nRVec({4, 6:0.000000},{5, 6:0.000000},{6, 6:0.000000})\nT({7, 6:0.000000},{8, 6:0.000000},{9, 6:0.000000})\nScore : {10, 6:0.000000}\nResidual : {11, 6:0.000000}",
								   sResult.strClassName, tp3F64Rotation.x, tp3F64Rotation.y, tp3F64Rotation.z, tp3F64RotVec.x, tp3F64RotVec.y, tp3F64RotVec.z, flp3F64Translation.x, flp3F64Translation.y, flp3F64Translation.z, f64Score, f64Residual)

			# 추정된 포즈 행렬 및 score 출력
			if(res := layer3DDst.DrawText3D(tp3Center, strText, EColor.YELLOW, EColor.BLACK, 15)).IsFail() :			
				ErrorPrint(res, "Failed to draw text.\n")
				break
			
		view3DDst.ZoomFit()
		view3DSource.ZoomFit()

		# 이미지 뷰를 갱신 합니다. // Update image view
		view3DSource.Invalidate(True)
		view3DDst.Invalidate(True)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 // Wait for the image and 3D view to close
		while arrView3DLearn[0].IsAvailable() and arrView3DLearn[1].IsAvailable() and arrView3DLearn[2].IsAvailable() and view3DSource.IsAvailable() and view3DDst.IsAvailable() :
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()