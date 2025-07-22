# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *
from numpy import byte, uint


# 메인 함수 // Main function
def main():

	# 3D 객체 선언 // Declare 3D object
	floDestinationObject = CFL3DObject()
	floLearnObject = CFL3DObject()
	floSourceObject = CFL3DObject()

	# 3D 뷰 선언 // Declare 3D view	
	view3DDst = CGUIView3D()
	view3DLearn = CGUIView3D()
	view3DSource = CGUIView3D()

	# 알고리즘 동작 결과 // Algorithm execution result
	res = CResult()

	while True:		
		# Source Object 로드 // Load the Source object
		if(res := floLearnObject.Load("../../ExampleImages/VertexMatch3D/ResultPoints.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the object file.\n")
			break
		
		if(res := floSourceObject.Load("../../ExampleImages/VertexMatch3D/ReferencePoints.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the object file.\n")
			break

		# Learn 3D 뷰 생성
		if(res := view3DLearn.Create(0, 0, 500, 500)).IsFail() :		
			ErrorPrint(res, "Failed to create the Source 3D view.\n")
			break

		if(res := view3DLearn.PushObject(floLearnObject)).IsFail() :		
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break

		# Source 3D 뷰 생성
		if(res := view3DSource.Create(500, 0, 1000, 500)).IsFail() :		
			ErrorPrint(res, "Failed to create the Source 3D view.\n")
			break
		

		if(res := view3DSource.PushObject(floSourceObject)).IsFail() :		
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break

		# Dst 3D 뷰 생성
		if(res := view3DDst.Create(0, 500, 500, 1000)).IsFail() :		
			ErrorPrint(res, "Failed to create the Destination 3D view.\n")
			break
				
		# Vertex3D 객체 생성 // Create Vertex3D object
		VertexMatch3D = CVertexMatch3D()

		# Learn object 설정 // Set the learn object
		VertexMatch3D.SetLearnObject(floLearnObject)
		# Source object 설정 // Set the source object
		VertexMatch3D.SetSourceObject(floSourceObject)
		# Min score 설정 // Set the min score
		VertexMatch3D.SetMinScore(0.3)
		# 최대 결과 개수 설정 // Set the max count of match result
		VertexMatch3D.SetMaxObject(1)
		# 학습 샘플링 거리 설정 // Set the learn sampling distance
		VertexMatch3D.SetLearnSamplingDistance(0.03)
		# 장면 샘플링 거리 설정 // Set the scene sampling distance
		VertexMatch3D.SetSceneSamplingDistance(0.03)
		# 키포인트 비율 설정 // Set the keypoint ratio.
		VertexMatch3D.SetKeypointRatio(0.5)
		# 엣지 학습 여부 설정 // Set the edge train
		VertexMatch3D.EnableTrainEdge(False)
		# 배경 제거 여부 설정 // Set the background removal
		VertexMatch3D.EnableBackgroundRemoval(False)
		# 클러스터링 범위 설정 // Set the clustering range
		VertexMatch3D.SetClusterRange(0.02)
		# 포즈 조정 반복 횟수 설정 // Set the iteration value of pose refinement
		VertexMatch3D.SetIteration(15)
		# 초기 점수 설정 // Set the initial score
		VertexMatch3D.SetInitialScore(0.1)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := VertexMatch3D.Learn()).IsFail() :	
			ErrorPrint(res, "Failed to learn Vertex Match 3D.")
			break
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := VertexMatch3D.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute Vertex Match 3D.")
			break


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately		
		layer3DDst = view3DDst.GetLayer(0)
		layer3DSource = view3DSource.GetLayer(0)
		layer3DLearn = view3DLearn.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer3DDst.Clear()
		layer3DSource.Clear()
		layer3DLearn.Clear()

		# View 정보를 디스플레이 합니다. // Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()

		if(res := layer3DLearn.DrawTextCanvas(flp, "Learn Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if(res := layer3DSource.DrawTextCanvas(flp, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := layer3DDst.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		# 3D 오브젝트 뷰에 결과 Object와 비교를 위한 Source 오브젝트 디스플레이
		if(res := view3DDst.PushObject(VertexMatch3D.GetSourceObject())).IsFail():
			ErrorPrint(res, "Failed to set object on the 3D View.\n")
			break
		
		sResult = SPoseMatrixParameters()

		f64ArrRotX = 0.0
		f64ArrRotY = 0.0
		f64ArrRotZ = 0.0
		f64Score = 0.0
		f64Residual = 0.0

		i64ResultCount = VertexMatch3D.GetResultCount()

		if i64ResultCount == 0 :		
			ErrorPrint(res, "Failed to estimate pose matrix.\n")
			break
		
		for i in range(0, i64ResultCount) :
			floLearnTransform = CFL3DObject()
			flpTrans = CFLPoint3[Double]()
			tp3Center = TPoint3[Double]()
			tp3RotVec = TPoint3[Double]()

			# 추정된 포즈 행렬 가져오기
			res, sResult = VertexMatch3D.GetResultPoseMatrix(i, sResult)

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

			res, floLearnTransform, tp3Center = VertexMatch3D.GetResultObject(i, floLearnTransform, tp3Center)

			if res.IsFail() :			
				ErrorPrint(res, "Failed to set object on the 3d view.\n")
				break
			
			if(res := view3DDst.PushObject(floLearnTransform)).IsFail() :
			
				ErrorPrint(res, "Failed to set object on the 3d view.\n")
				break
			
			strChannel = String.Format("R({0,6:0.000000}, {1,6:0.000000}, {2,6:0.000000}) , \nRVec({3,6:0.000000}, {4,6:0.000000}, {5,6:0.000000}) , \nT({6,6:0.000000}, {7,6:0.000000}, {8,6:0.000000})\nScore : {9,6:0.000000}\nResidual {10,6:0.000000}:"
								, f64ArrRotX, f64ArrRotY, f64ArrRotZ, tp3RotVec.x, tp3RotVec.y, tp3RotVec.z, flpTrans.x, flpTrans.y, flpTrans.z, f64Score, f64Residual)

			# 추정된 포즈 행렬 및 score 출력
			if(res := layer3DDst.DrawText3D(tp3Center, strChannel, EColor.YELLOW, EColor.BLACK, 15)).IsFail() :			
				ErrorPrint(res, "Failed to draw text.\n")
				break
			
		view3DDst.ZoomFit()
		view3DLearn.ZoomFit()
		view3DSource.ZoomFit()

		# 이미지 뷰를 갱신 합니다. // Update image view
		view3DLearn.Invalidate(True)
		view3DSource.Invalidate(True)
		view3DDst.Invalidate(True)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 // Wait for the image and 3D view to close
		while view3DSource.IsAvailable() and view3DLearn.IsAvailable() and view3DDst.IsAvailable() :
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