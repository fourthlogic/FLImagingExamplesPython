# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():
	CLibraryUtilities.Initialize()

	# 3D 객체 선언 // Declare 3D object
	floDestinationObject = CFL3DObject()
	floSourceObject = CFL3DObject()

	# 3D 뷰 선언 // Declare 3D view	
	view3DDst = CGUIView3D()
	view3DSource = CGUIView3D()

	# 알고리즘 동작 결과 // Algorithm execution result
	res = CResult()

	while True:		
		# Source Object 로드 // Load the Source object
		if(res := floSourceObject.Load("../../ExampleImages/VoxelGrid3D/VoxelGrid3DExample.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the object file.\n")
			break
		

		# Source 3D 뷰 생성
		if(res := view3DSource.Create(612, 0, 1124, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the Source 3D view.\n")
			break
		

		# Dst 3D 뷰 생성
		if(res := view3DDst.Create(1124, 0, 1636, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the Destination 3D view.\n")
			break
		

		# Source Object 3D 뷰 생성 // Create the source object 3D view
		if(res := view3DSource.PushObject(floSourceObject)).IsFail() :		
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break
		
		# VoxelGrid3D 객체 생성 // Create VoxelGrid3D object
		VoxelGrid3D = CVoxelGrid3D()

		# Destination object 설정 // Set the learn object
		VoxelGrid3D.SetDestinationObject(floDestinationObject)
		# Source object 설정 // Set the source object
		VoxelGrid3D.SetSourceObject(floSourceObject)
		# 샘플링 거리 설정 // Set the sampling distance
		VoxelGrid3D.SetSamplingDistance(0.03)
		# 샘플링 방법 설정 // Set the sampling method
		VoxelGrid3D.SetSamplingMethod(CVoxelGrid3D.ESamplingMethod.Mean)
		# 점 색상 포함 여부 설정 // Set whether the color of the vertex is included
		VoxelGrid3D.EnableIncludingVertexColor(True)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := VoxelGrid3D.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute Voxel Grid 3D.")
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
		flp = CFLPoint[Double]()

		if(res := layer3DSource.DrawTextCanvas(flp, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := layer3DDst.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		# 3D 오브젝트 뷰에 결과 오브젝트 디스플레이
		if(res := view3DDst.PushObject(VoxelGrid3D.GetDestinationObject())).IsFail() :		
			ErrorPrint(res, "Failed to set object on the 3D View.\n")
			break

		view3DDst.ZoomFit()
		view3DSource.ZoomFit()
            	
		# 이미지 뷰를 갱신 합니다. // Update image view
		view3DSource.Invalidate(True)
		view3DDst.Invalidate(True)

		view3DDst.SynchronizePointOfView(view3DSource)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 // Wait for the image and 3D view to close
		while view3DSource.IsAvailable() and view3DDst.IsAvailable() :
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