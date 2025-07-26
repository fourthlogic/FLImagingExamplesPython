# FLImagingClrPy 선언 // Declare FLImagingClrPy
from tokenize import Double
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliSourceImage1 = CFLImage()
	fliSourceImage2 = CFLImage()
	fliSourceImage3 = CFLImage()
	fliSourceImage4 = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc1 = CGUIViewImage()
	viewImageSrc2 = CGUIViewImage()
	viewImageSrc3 = CGUIViewImage()
	viewImageSrc4 = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage1.Load('../../ExampleImages/Tiling/TilingSourceImage0.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliSourceImage2.Load('../../ExampleImages/Tiling/TilingSourceImage1.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliSourceImage3.Load('../../ExampleImages/Tiling/TilingSourceImage2.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliSourceImage4.Load('../../ExampleImages/Tiling/TilingSourceImage3.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지에 ROI 추가 // Add ROI to the source image
		flRect = CFLRect[Double]()

		flRect.Set(30, 68, 200, 235);
		flRect.SetName('0')
		fliSourceImage1.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flRect))

		flRect.Set(260,135, 415, 440)
		flRect.SetName('1')
		fliSourceImage1.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flRect))

		flRect.Set(280, 250, 480, 480)
		flRect.SetName('0')
		fliSourceImage2.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flRect))

		flRect.Set(110, 150, 350, 440)
		flRect.SetName('0')
		fliSourceImage3.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flRect))

		flRect.Set(220, 230, 470, 450)
		flRect.SetName('0')
		fliSourceImage4.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flRect))

		# 여러 장의 이미지를 하나의 FLImage로 생성 // Create multiple images into one FLImage
		fliSourceImage.Assign(fliSourceImage1)
		fliSourceImage.PushBackPage(fliSourceImage2)
		fliSourceImage.PushBackPage(fliSourceImage3)
		fliSourceImage.PushBackPage(fliSourceImage4)

		# Destination 이미지 로드 // Load the destination image
		if (res := fliDestinationImage.Load('../../ExampleImages/Tiling/TilingDestinationImage.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지에 ROI 추가 // Add ROI to the destination image
		fliDestinationImage.PushBackFigure('D(79.292035, 67.964602, 292.247788, 267.327434, INFO[NAME(0_0)])')
		fliDestinationImage.PushBackFigure('D(296.778761, 271.858407, 459.893805, 444.035398, INFO[NAME(0_1)])')
		fliDestinationImage.PushBackFigure('D(88.353982, 738.548673, 337.557522, 956.035398, INFO[NAME(1_0)])')
		fliDestinationImage.PushBackFigure('D(482.548673, 457.628319, 659.256637, 675.115044, INFO[NAME(2_0)])')
		fliDestinationImage.PushBackFigure('D(659.256638, 222.017700, 835.964602, 439.504425, INFO[NAME(3_0)])')

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc1.Create(100, 0, 400, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSrc2.Create(400, 0, 700, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSrc3.Create(100, 300, 400, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSrc4.Create(400, 300, 700, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst.Create(700, 0, 1300, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SetImagePtr(fliSourceImage1)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc2.SetImagePtr(fliSourceImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc3.SetImagePtr(fliSourceImage3)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc4.SetImagePtr(fliSourceImage4)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizeWindow(viewImageSrc2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		if (res := viewImageSrc1.SynchronizeWindow(viewImageSrc3)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		if (res := viewImageSrc1.SynchronizeWindow(viewImageSrc4)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		if (res := viewImageSrc1.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Tiling 객체 생성 // Create Tiling object
		tiling = CTiling()

		# Source 이미지 설정 // Set the source image
		tiling.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set the destination image
		tiling.SetDestinationImage(fliDestinationImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := tiling.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Tiling.')
			break

		# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춤 // With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen
		if (res := viewImageDst.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to zoom fit the image view.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource1 = viewImageSrc1.GetLayer(0)
		layerSource2 = viewImageSrc2.GetLayer(0)
		layerSource3 = viewImageSrc3.GetLayer(0)
		layerSource4 = viewImageSrc4.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource1.Clear()
		layerSource2.Clear()
		layerSource3.Clear()
		layerSource4.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource1.DrawTextCanvas(flpPoint, 'Source Image 1', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerSource2.DrawTextCanvas(flpPoint, 'Source Image 2', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerSource3.DrawTextCanvas(flpPoint, 'Source Image 3', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerSource4.DrawTextCanvas(flpPoint, 'Source Image 4', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc1.Invalidate(True)
		viewImageSrc2.Invalidate(True)
		viewImageSrc3.Invalidate(True)
		viewImageSrc4.Invalidate(True)
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc1.IsAvailable() and viewImageSrc2.IsAvailable() and viewImageSrc3.IsAvailable() and viewImageSrc4.IsAvailable() and viewImageDst.IsAvailable():
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