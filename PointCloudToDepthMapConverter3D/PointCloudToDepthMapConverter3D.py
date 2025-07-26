# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

from System.Collections.Generic import List


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliDestination = CFLImage()
	fliDestinationTexture = CFLImage()

	# 3D 객체 선언 // Declare 3D object
	floSource = CFL3DObject()

	# 3D 뷰 선언 // Declare 3D view	
	view3D = CGUIView3D()
	viewDepthImage = CGUIViewImage()
	viewDestinationTextureImage = CGUIViewImage()

	# 알고리즘 동작 결과 // Algorithm execution result
	res = CResult()

	while True:		
		# Source Object 로드 // Load the Source object
		if(res := floSource.Load("../../ExampleImages/PointCloudToDepthMapConverter3D/Example.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the 3d object.\n")
			break

		# 이미지 뷰 생성 // Create image view
		if(res := viewDepthImage.Create(100, 0, 612, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the Source image view.\n")
			break		

		if(res := viewDestinationTextureImage.Create(612, 0, 1124, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the Texture image view.\n")
			break
		
		# 결과 3D 뷰 생성 // Create result 3D view
		if(res := view3D.Create(100, 512, 612, 1024)).IsFail() :		
			ErrorPrint(res, "Failed to create the Result 3D view.\n")
			break		

		# DepthMapToPointCloudConverter 객체 생성 // Create DepthMapToPointCloudConverter object
		PointCloudToDepthMapConverter3D = CPointCloudToDepthMapConverter3D()

		# Destination 이미지 설정 // Set the Destination image.
		PointCloudToDepthMapConverter3D.SetDestinationImage(fliDestination)

		# Destination Texture 이미지 설정 // Set the texture image.
		PointCloudToDepthMapConverter3D.SetDestinationImageTexture(fliDestinationTexture)

		# 이미지 크기 설정 // Set the image size.
		PointCloudToDepthMapConverter3D.SetImageSize(2064, 1544)

		# Camera Matrix 설정 // Set the camera matrix
		flpFocalLength = CFLPoint[Single]()
		flpPrincipalPoint = CFLPoint[Single]()

		flpFocalLength.x = 2328.800049
		flpFocalLength.y = 2330.899902
		flpPrincipalPoint.x = 988.599976
		flpPrincipalPoint.y = 750.299988

		PointCloudToDepthMapConverter3D.SetIntrinsicParameter(flpFocalLength, flpPrincipalPoint)

		#왜곡 계수 설정 // Set the distortion coefficient
		flaDistortionCoefficient = List[Double]()

		flaDistortionCoefficient.Add(-0.2333453150000)
		flaDistortionCoefficient.Add(0.1352355330000)
		flaDistortionCoefficient.Add(0.0005843197580)
		flaDistortionCoefficient.Add(-0.0005675755000)
		flaDistortionCoefficient.Add(-0.0246060137000)

		PointCloudToDepthMapConverter3D.SetDistortionCoefficient(flaDistortionCoefficient)

		# Z축 방향 설정 // Set z-axis direction.
		PointCloudToDepthMapConverter3D.SetDirectionType(EDirectionType.Increment)

		# Source 3D Object 설정 // Set the source 3D object
		PointCloudToDepthMapConverter3D.SetSourceObject(floSource)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := PointCloudToDepthMapConverter3D.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute Depth Map To Point Cloud Converter 3D.")
			break
		
		# 이미지 포인터 설정 // Set image pointer
		viewDepthImage.SetImagePtr(fliDestination)
		viewDestinationTextureImage.SetImagePtr(fliDestinationTexture)

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately		
		layerViewDepth = viewDepthImage.GetLayer(0)
		layerViewDestinationTexture = viewDestinationTextureImage.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerViewDepth.Clear()
		layerViewDestinationTexture.Clear()

		# View 정보를 디스플레이 합니다. // Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()

		if(res := layerViewDestinationTexture.DrawTextCanvas(flp, "Destination Texture Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := layerViewDepth.DrawTextCanvas(flp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		# 3D 오브젝트 뷰에 결과 오브젝트 디스플레이
		if(res := view3D.PushObject(floSource)).IsFail() :		
			ErrorPrint(res, "Failed to set object on the 3D View.\n")
			break
		
		view3D.PushObject(floSource)
		view3D.UpdateObject(-1)
		view3D.UpdateScreen()
		view3D.ZoomFit()

		viewDepthImage.ZoomFit()
		viewDestinationTextureImage.ZoomFit()
            	
		# 이미지 뷰를 갱신 합니다. // Update image view
		viewDestinationTextureImage.Invalidate(True)
		viewDepthImage.Invalidate(True)

		viewDepthImage.SynchronizePointOfView(viewDestinationTextureImage)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 // Wait for the image and 3D view to close
		while viewDestinationTextureImage.IsAvailable() and viewDepthImage.IsAvailable() :
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