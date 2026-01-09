# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 객체 선언 # Declare 3D object	
	floSource = CFL3DObject()
	arrFloResult = [CFL3DObject() for _ in range(3)]	

	# 3D 뷰 선언 # Declare 3D view	
	
	view3DSource = CGUIView3D()
	arr3DView = [CGUIView3D() for _ in range(3)]
	arrI32Sensitivity = [1, 3, 5]

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:		
		# Source Object 로드 # Load the Source object
		if(res := floSource.Load("../../ExampleImages/PointCloudResamplerEdgePreserving3D/Box.fl3do")).IsFail() :		
			ErrorPrint(res, "Failed to load the object file.\n")
			break
		

		# 3D 뷰 생성 # Create 3D View
		if(res := view3DSource.Create(100, 0, 612, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# 3D 뷰 생성 # Create 3D View
		if(res := arr3DView[0].Create(100, 512, 612, 1024)).IsFail() :		
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# 3D 뷰 생성 # Create 3D View
		if(res := arr3DView[1].Create(612, 512, 1124, 1024)).IsFail() :		
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# 3D 뷰 생성 # Create 3D View
		if(res := arr3DView[2].Create(1124, 512, 1636, 1024)).IsFail() :		
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break
		
		# PointCloudResamplerEdgePreserving3D 객체 생성 # Create PointCloudResamplerEdgePreserving3D object
		pointCloudResamplerEdgePreserving3D = CPointCloudResamplerEdgePreserving3D()

		# Source object 설정 # Set the source object
		pointCloudResamplerEdgePreserving3D.SetSourceObject(floSource)

		# 법선 벡터 각도 임계 설정 # Set the normal angle threshold
		pointCloudResamplerEdgePreserving3D.SetNormalAngleThreshold(15)

		# 탐색할 최근접 이웃 수 설정 # Set the number of nearest neighbors to search
		pointCloudResamplerEdgePreserving3D.SetNormalEstimationNeighborCount(20)

		# 반경 자동 계산 여부 설정 # Sets whether the radius is calculated automatically.
		pointCloudResamplerEdgePreserving3D.EnableAutoRadiusCalculation(True)

		# 결과 법선 포함 여부 설정 # Sets whether to retain result normals.
		pointCloudResamplerEdgePreserving3D.EnableNormalRetainment(False)

		# 반경 계수 설정 # Set the radius coefficient
		pointCloudResamplerEdgePreserving3D.SetRadiusCoefficient(5)

		# 입력 샘플링 개수 설정 # Set the source sampling size
		pointCloudResamplerEdgePreserving3D.SetSourceSamplingSize(2500)

		# 결과 샘플링 개수 설정 # Set the result sampling size
		pointCloudResamplerEdgePreserving3D.SetResultSamplingSize(10000)

		# 점 재배치 반복 횟수 설정 # Set the point reposition iterations
		pointCloudResamplerEdgePreserving3D.SetRepositionIterations(5)

		tpPosition = CFLPoint[Double](0, 0)

		for i in range(3):
			# Destination object 설정 # Set the destination object
			pointCloudResamplerEdgePreserving3D.SetDestinationObject(arrFloResult[i]);

			# 에지 민감도 설정 # Set the edge sensitivity
			pointCloudResamplerEdgePreserving3D.SetEdgeSensitivity(arrI32Sensitivity[i]);

			# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
			if(res := pointCloudResamplerEdgePreserving3D.Execute()).IsFail() :				
				ErrorPrint(res, "Failed to execute Point Cloud Resampler Edge Preserving 3D.")
				break		

			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately					
			view3DLayer = arr3DView[i].GetLayer(0)
		
			# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
			view3DLayer.Clear()

			# View 정보를 디스플레이 합니다. # Display View information.
			# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
			# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
			#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
			# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
			#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic			

			strText = f'Edge Sensitivity {arrI32Sensitivity[i]}'

			if(res := view3DLayer.DrawTextCanvas(tpPosition, strText, EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
				ErrorPrint(res, "Failed to draw text.\n")
				break

				# 3D 오브젝트 뷰에 결과 오브젝트 디스플레이
			if (res := arr3DView[i].PushObject(arrFloResult[i])).IsFail() :
				ErrorPrint(res, "Failed to set object on the 3D View.\n")
				break

			view3DSource.SynchronizePointOfView(arr3DView[i])
		
		view3DLayerSource = view3DSource.GetLayer(0)		
		view3DLayerSource.Clear()

		if(res := view3DLayerSource.DrawTextCanvas(tpPosition, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break

			# 3D 오브젝트 뷰에 결과 오브젝트 디스플레이
		if (res := view3DSource.PushObject(floSource)).IsFail() :
			ErrorPrint(res, "Failed to set object on the 3D View.\n")
			break

		# 이미지 뷰를 갱신 합니다. # Update image view
		view3DSource.ZoomFit()
		view3DSource.Invalidate(True)    	

		for i in range(3):
			arr3DView[i].Invalidate(True)
		
		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while view3DSource.IsAvailable() and arr3DView[0].IsAvailable() and arr3DView[1].IsAvailable() and arr3DView[2].IsAvailable() :
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()