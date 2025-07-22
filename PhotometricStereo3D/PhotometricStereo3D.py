# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()
	fliTextureImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageDestination = CGUIViewImage()
	viewImage3D = CGUIView3D()

	while True:
		
		# Source 이미지 로드 # Load the learn image
		if (res := fliSourceImage.Load('../../ExampleImages/PhotometricStereo3D/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Page 0 선택 # Select page 0
		fliSourceImage.SelectPage(0);
		
		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSource.Create(100, 0, 548, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 이미지 뷰 생성 # Create destination image view
		if (res := viewImageDestination.Create(100, 448, 548, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDestination.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 3D 이미지 뷰 생성 # Create destination 3D image view
		if (res := viewImage3D.Create(548, 448, 996, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the 3D view.')
			break

		# Stereo Calibrator 3D 객체 생성 # Create Stereo Calibrator 3D object
		photometric = CPhotometricStereo3D()
		
		# Source 이미지 설정 # Set source image
		photometric.SetSourceImage(fliSourceImage)
		
		# Destination 이미지 설정 # Set destination image
		photometric.SetDestinationHeightMapImage(fliDestinationImage)
		
		# Texture 이미지 설정 # Set texture image
		photometric.SetDestinationTextureImage(fliTextureImage)
		
		# 동작 방식 설정 # Set Operation Mode
		photometric.SetReconstructionMode(CPhotometricStereo3D.EReconstructionMode.Poisson_FP32)

		# Valid 픽셀의 기준 설정 # Set valid pixel ratio
		photometric.SetValidPixelThreshold(0.125)
		
		# 각 이미지의 광원 Slant 값 입력
		mvdSlant = CMultiVar[Double]();

		mvdSlant.PushBack(39.831506);
		mvdSlant.PushBack(28.682381);
		mvdSlant.PushBack(20.989625);
		mvdSlant.PushBack(19.346638);
		mvdSlant.PushBack(20.785800);
		mvdSlant.PushBack(26.005273);
		mvdSlant.PushBack(19.038004);
		mvdSlant.PushBack(9.253585);
		mvdSlant.PushBack(16.425454);
		mvdSlant.PushBack(23.712574);
		mvdSlant.PushBack(26.003058);
		mvdSlant.PushBack(19.069500);
		mvdSlant.PushBack(11.801071);
		mvdSlant.PushBack(20.484473);
		mvdSlant.PushBack(25.909730);
		mvdSlant.PushBack(43.055332);
		mvdSlant.PushBack(39.043981);
		mvdSlant.PushBack(30.041029);
		mvdSlant.PushBack(26.067657);
		mvdSlant.PushBack(26.126303);

		# 각 이미지의 광원 Tilt 값 입력
		mvdTilt = CMultiVar[Double]();

		mvdTilt.PushBack(123.359091);
		mvdTilt.PushBack(123.952892);
		mvdTilt.PushBack(154.836215);
		mvdTilt.PushBack(-173.353324);
		mvdTilt.PushBack(-147.483507);
		mvdTilt.PushBack(109.497340);
		mvdTilt.PushBack(115.825606);
		mvdTilt.PushBack(-169.019112);
		mvdTilt.PushBack(-119.343654);
		mvdTilt.PushBack(-109.319167);
		mvdTilt.PushBack(66.944279);
		mvdTilt.PushBack(48.136896);
		mvdTilt.PushBack(-5.157068);
		mvdTilt.PushBack(-54.033519);
		mvdTilt.PushBack(-66.856636);
		mvdTilt.PushBack(60.456870);
		mvdTilt.PushBack(53.388008);
		mvdTilt.PushBack(36.447691);
		mvdTilt.PushBack(13.056294);
		mvdTilt.PushBack(-5.976723);

		photometric.SetLightAngleDegrees(mvdSlant, mvdTilt);


		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := photometric.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Photometric Stereo 3D.')
			break

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDestination.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSource.GetLayer(0)
		layerDestination = viewImageDestination.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 18)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Height Map Image', EColor.YELLOW, EColor.BLACK, 18)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 3D 뷰 결과 출력 # Display 3D view result
		fl3DObject = CFL3DObjectHeightMap(fliDestinationImage)
		fl3DObject.SetTextureImage(fliTextureImage);

		viewImage3D.PushObject(fl3DObject)
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImage3D.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageSource.Invalidate(True)
		viewImageDestination.Invalidate(True)
		viewImage3D.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSource.IsAvailable() and viewImageDestination.IsAvailable() and viewImage3D.IsAvailable():
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
