# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()
	fliIndexImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageDestination = CGUIViewImage()
	viewImageIndex = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/PagePooling/Multiple File_Max.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSource.Create(200, 0, 712, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create destination image view
		if (res := viewImageDestination.Create(712, 0, 1224, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Index 이미지 뷰 생성 // Create index image view
		if (res := viewImageIndex.Create(1224, 0, 1736, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
		if (res := viewImageSource.SynchronizeWindow(viewImageDestination))[0].IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
		if (res := viewImageSource.SynchronizeWindow(viewImageIndex))[0].IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views. 
		if (res := viewImageSource.SynchronizePointOfView(viewImageDestination))[0].IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views. 
		if (res := viewImageSource.SynchronizePointOfView(viewImageIndex))[0].IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDestination.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageIndex.SetImagePtr(fliIndexImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 객체 생성 // Create object
		PagePooling = CPagePooling()

		# Source 이미지 설정 // Set the source image
		PagePooling.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set the destination image
		PagePooling.SetDestinationImage(fliDestinationImage);

		# Index 이미지 // Index image
		#	- 각 픽셀별로 추출한 결과 값이 위치한 페이지 인덱스 값을 대응되는 좌표의 픽셀로 출력합니다. // For each pixel, output the page index value where the resulting value is located to the pixel of the corresponding coordinates.
		#	- Sampling 메소드가 Min Gaussian, Max Gaussian 모드인 경우 출력되는 인덱스 이미지는 각각 Min, Max 모드로 동작할 때 출력되는 인덱스 이미지와 동일합니다. // If the sampling method is in Min Gaussian and Max Gaussian modes, the output index image is the same as the output index image when operating in Min and Max modes, respectively.
		#	- Sampling 메소드가 Mean 모드인 경우는 인덱스 이미지 출력을 지원하지 않습니다. // Index image output is not supported when the Sampling method is in Mean mode.
		#	- 추출할 결과 값이 여러 페이지에 동일하게 존재할 경우, 가장 앞의 인덱스를 출력합니다. // Outputs the leading index if the resulting values to be extracted are equally present on multiple pages.
		#	- SetIndexImage 는 SetSourceImage 나 SetDestinationImage 에서 설정한 이미지와 동일하면 동작하지 않습니다. // - SetIndexImage will not work if it is the same as the image set in SetSourceImage or SetDestinationImage.
		#	- Index Image 를 지정하지 않을 경우 인덱스 이미지를 출력하지 않는 모드로 동작합니다. // If SetIndexImage is not specified, it operates in a mode that does not output the index image.
		#	- 인덱스 이미지 추출은 최대 65535 장 까지만 지원됩니다. // Index image extraction is supported up to 65535 pages
		#	- Source ROI 영역 밖에 해당하는 인덱스는 무효 값으로 8bit 인덱스 이미지에서는 255, 16bit 인덱스 이미지에서는 65535 가 입력됩니다. // Indexes outside the Source ROI area are invalid values, with 255 for an 8-bit index image and 65535 for a 16-bit index image.
		
		# Index 이미지 설정 // Set the index image
		PagePooling.SetIndexImage(fliIndexImage);

		# Sampling 메소드 설정 // Set the sampling method
		#	- Max : 입력된 이미지 가운데 최대 값을 출력합니다. // Max : Outputs the maximum value of the entered image.
		#	- MaxGaussian : 입력된 이미지 가운데 가장 앞 쪽 인덱스에 위치한 최대 값을 기준으로 가우시안 값을 출력합니다. // MaxGaussian : Outputs the Gaussian value based on the maximum value located in the leading index of the entered image.
		#	- Min : 입력된 이미지 가운데 최소 값을 출력합니다. // Min : Outputs the minimum value of the entered image.
		#	- MinGaussian : 입력된 이미지 가운데 가장 앞 쪽 인덱스에 위치한 최소 값을 기준으로 가우시안 값을 출력합니다. // MinGaussian : Outputs the Gaussian value based on the minimum value located in the leading index of the entered image.
		#	- Mean : 입력된 이미지들의 평균 값을 출력합니다. (최대 16843009 장 까지 지원됩니다.) // Mean: Outputs the average value of the entered images. (Up to 16843009 pages are supported.)
		PagePooling.SetSamplingMethod(CPagePooling.ESamplingMethod.Max);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := PagePooling.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSource.GetLayer(0)
		layerIndex= viewImageIndex.GetLayer(0)
		layerDestination = viewImageDestination.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerIndex.Clear()
		layerDestination.Clear()
		flpZero = CFLPoint[Double](0, 0)

		if(res := layerSource.DrawTextCanvas(flpZero , 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerIndex.DrawTextCanvas(flpZero , 'Index Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpZero , 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 // Update image view
		viewImageSource.Invalidate(True)
		viewImageIndex.Invalidate(True)
		viewImageDestination.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSource.IsAvailable() and viewImageIndex.IsAvailable() and viewImageDestination.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()