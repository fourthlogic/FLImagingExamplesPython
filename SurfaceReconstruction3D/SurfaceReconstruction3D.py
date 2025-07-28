# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

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
		if(res := floSourceObject.Load("../../ExampleImages/SurfaceReconstruction3D/Source.ply")).IsFail() :		
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
		
		# SurfaceReconstruction 객체 생성 // Create SurfaceReconstruction object
		surfaceReconstruction3D = CSurfaceReconstruction3D()

		# Source Object 설정 // Set the source object
		surfaceReconstruction3D.SetSourceObject(floSourceObject)

		# Destination object 설정 // Set the destination object
		surfaceReconstruction3D.SetDestinationObject(floDestinationObject)

		# Reconstruction Method 설정 // Set the reconstruction method
		surfaceReconstruction3D.SetReconstructionMethod(CSurfaceReconstruction3D.EReconstructionMethod.Explicit_RegionGrowing)

		# 최대 반경 자동 계산하도록 설정 // Set to auto-calculate maximum radius
		surfaceReconstruction3D.EnableExplicitAutoRadius(True)

		# 최대 반경 계수 설정 // Set the maximum radius coefficient
		surfaceReconstruction3D.SetExplicitMaxRadiusCoefficient(5)

		# Hole filling 최대 반경 자동 계산하도록 설정 // Set to auto-calculate hole filling maximum radius
		surfaceReconstruction3D.EnableExplicitHoleFillingAutoRadius(True)

		# 최대 반경 계수 설정 // Set the maximum radius coefficient
		surfaceReconstruction3D.SetExplicitHoleFillingRadiusCoefficient(1)

		# 시작 지점 최대 개수 설정 // Set the maximum number of starting points
		surfaceReconstruction3D.SetExplicitMaxSeed(10000)

		# 그리드 셀 거리 자동 계산하도록 설정 // Set to auto-calculate grid cell distance
		surfaceReconstruction3D.EnableExplicitAutoCellRadius(True)

		# 그리드 셀 거리 계수 설정 // Set the grid cell distance coefficient
		surfaceReconstruction3D.SetExplicitCellRadiusCoefficient(1)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := surfaceReconstruction3D.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute Surface Reconstruction 3D.")
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
		if(res := view3DDst.PushObject(floDestinationObject)).IsFail() :		
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