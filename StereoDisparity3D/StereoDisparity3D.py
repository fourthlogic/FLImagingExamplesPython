# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliSourceImage2 = CFLImage()
	fliDestinationImage = CFLImage()
	fliTextureImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageSource2 = CGUIViewImage()
	viewImageDestination = CGUIViewImage()
	view3DDestination = CGUIView3D()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/StereoDisparity3D/Left.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Source 2 이미지 로드 # Load the source 2 image
		if (res := fliSourceImage2.Load('../../ExampleImages/StereoDisparity3D/Right.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Page 0 선택 # Select page 0
		fliSourceImage.SelectPage(0);
		fliSourceImage2.SelectPage(0);

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSource.Create(100, 0, 548, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Source 2 이미지 뷰 생성 # Create source 2 image view
		if (res := viewImageSource2.Create(548, 0, 996, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage))[0].IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource2.SetImagePtr(fliSourceImage2))[0].IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰 생성 # Create destination image view
		if (res := viewImageDestination.Create(100, 448, 548, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDestination.SetImagePtr(fliDestinationImage))[0].IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 이미지 뷰 생성 # Create destination image view
		if (res := view3DDestination.Create(548, 448, 996, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizeWindow(viewImageSource2))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizeWindow(viewImageDestination))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizeWindow(view3DDestination))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# Stereo Calibrator 3D 객체 생성 # Create Stereo Calibrator 3D object
		stereoDisparity = CStereoDisparity3D()
		
		# Source 이미지 설정 # Set source image
		stereoDisparity.SetSourceImage(fliSourceImage)
		
		# Source 2 이미지 설정 # Set source 2 image
		stereoDisparity.SetSourceImage2(fliSourceImage2)
		
		# Destination Height Map 이미지 설정 # Set the destination height map image
		stereoDisparity.SetDestinationHeightMapImage(fliDestinationImage)
		
		# 최소 허용 Disparity 값 설정 # Set the minimum allowed disparity value
		stereoDisparity.SetMinimumDisparity(-20)
		
		# Disparity 범위 설정 # Set the range of disparity
		stereoDisparity.SetMaximumDisparity(0)
		
		# Matched Block 크기 설정 # Set the matched block size
		stereoDisparity.SetMatchBlockSize(3)
		
		# 좌우 간 최대 허용 차이 값 설정 # Set maximum allowed difference value between left and right
		stereoDisparity.SetMaximumDifference(30)
		
		# 고유비 값 설정 # Set the uniqueness ratio value
		stereoDisparity.SetUniquenessRatio(0)
		
		# P1 값 설정 # Set P1 Value
		stereoDisparity.SetP1(200)
		
		# P2 값 설정 # Set P2 Value
		stereoDisparity.SetP2(800)
		
		# Median Morphology 커널 사이즈 설정 # Set the median morphology kernel size
		stereoDisparity.SetFilterSize(5)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := stereoDisparity.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Stereo Calibrator 3D.')
			break
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDestination.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSource.GetLayer(0)
		layerSource2 = viewImageSource2.GetLayer(0)
		layerDestination = viewImageDestination.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerSource2.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)
		
		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerSource2.DrawTextCanvas(flpPoint, 'Source Image 2', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 3D 뷰 결과 출력 # Display 3D view result
		fl3DOHM = CFL3DObjectHeightMap(fliDestinationImage)
		fl3DOHM.SetTextureImage(fliTextureImage)
		
		if (res := view3DDestination.PushObject(fl3DOHM)).IsFail():
			ErrorPrint(res, 'Failed to add 3D Object.')
			break
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := view3DDestination.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageSource.Invalidate(True)
		viewImageSource2.Invalidate(True)
		viewImageDestination.Invalidate(True)
		view3DDestination.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSource.IsAvailable() and viewImageSource2.IsAvailable() and viewImageDestination.IsAvailable() and view3DDestination.IsAvailable():
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
