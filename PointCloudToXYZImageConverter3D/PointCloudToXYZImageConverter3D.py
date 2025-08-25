# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

from System.Collections.Generic import List


# 메인 함수 # Main function
def main():
	
	# 3D 객체 선언 # Declare 3D object
	floSource = CFL3DObject()

	# 이미지 객체 선언 # Declare the image object
	fliDestination = CFLImage()
	fliTexture = CFLImage()

	# 3D 뷰 선언 # Declare 3D view	
	view3D = CGUIView3D()
	viewXYZImage = CGUIViewImage()
	viewTextureImage = CGUIViewImage()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:		
		# Point Cloud 로드 # Load the point cloud
		if(res := floSource.Load("../../ExampleImages/PointCloudToXYZImageConverter3D/3DSrc.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the point cloud.\n")
			break
		
		# PointCloudToXYZImageConverter3D 객체 생성 # Create PointCloudToXYZImageConverter3D object
		pointCloudToXYZImageConverter3D = CPointCloudToXYZImageConverter3D()

		# Source Point Cloud 설정 # Set the source point cloud.
		pointCloudToXYZImageConverter3D.SetSourceObject(floSource)

		# Texture 결과 이미지 설정 # Set the destination texture image.
		pointCloudToXYZImageConverter3D.SetDestinationImageTexture(fliTexture)

		# Destination 이미지 설정 # Set the destination image
		pointCloudToXYZImageConverter3D.SetDestinationImage(fliDestination)

		# 이미지 크기 설정 # Set the size of the destination image
		pointCloudToXYZImageConverter3D.SetImageSize(140, 200)

		
		# 입력 3D 뷰 생성 # Create input 3D view
		if(res := view3D.Create(100, 0, 612, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the Source 3D view.\n")
			break		

		# 이미지 뷰 생성 # Create image view
		if(res := viewXYZImage.Create(100, 512, 612, 1024)).IsFail() :		
			ErrorPrint(res, "Failed to create the Destination image view.\n")
			break		

		if(res := viewTextureImage.Create(612, 512, 1124, 1024)).IsFail() :		
			ErrorPrint(res, "Failed to create the Texture image view.\n")
			break
		
		# 이미지 포인터 설정 # Set image pointer
		viewXYZImage.SetImagePtr(fliDestination)
		viewTextureImage.SetImagePtr(fliTexture)


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately		
		layerView3D = view3D.GetLayer(0)
		layerViewDepth = viewXYZImage.GetLayer(0)
		layerViewTexture = viewTextureImage.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerView3D.Clear()
		layerViewDepth.Clear()
		layerViewTexture.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()
		
		if(res := layerView3D.DrawTextCanvas(flp, "Source Point Cloud", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		if(res := layerViewTexture.DrawTextCanvas(flp, "Destination XYZV Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		if(res := layerViewDepth.DrawTextCanvas(flp, "Destination Texture Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if(res := pointCloudToXYZImageConverter3D.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute Point Cloud To XYZ Image Converter 3D.")
			break
		
		# 3D View 카메라 설정 # Set 3D view camera
		fl3DCam = CFL3DCamera()

		fl3DCam.SetDirection(CFLPoint3[Single](0, 0, -1))
		fl3DCam.SetDirectionUp(CFLPoint3[Single](0, 1, 0))
		fl3DCam.SetPosition(CFLPoint3[Single](10, -20, 750))

		view3D.SetCamera(fl3DCam)

		view3D.PushObject(floSource)
		view3D.UpdateObject(-1)
		view3D.UpdateScreen()

		viewXYZImage.ZoomFit()
		viewTextureImage.ZoomFit()
        
		# 이미지 뷰를 갱신 합니다. # Update image view
		viewTextureImage.Invalidate(True)
		viewXYZImage.Invalidate(True)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while viewTextureImage.IsAvailable() and viewXYZImage.IsAvailable() and view3D.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()