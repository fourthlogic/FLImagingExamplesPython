# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Gradation/House.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := fliDestinationImage.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst.Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Gradation 객체 생성 // Create Gradation object
		gradation = CGradation()

		# Source 이미지 설정 // Set the source image
		gradation.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set the destination image
		gradation.SetDestinationImage(fliDestinationImage)

		# 시작 Alpha 값 설정 // Set start alpha value
		mvStartAlpha = CMultiVar[Double](0, 0, 0)
		gradation.SetStartAlpha(mvStartAlpha)

		# 끝 Alpha 값 설정 // Set end alpha value
		mvEndAlpha = CMultiVar[Double](0.1, 0.6, 0.9)
		gradation.SetEndAlpha(mvEndAlpha)

		# Gradation Start Value 설정(3Ch) // Set Gradation Start Value(3Ch)
		mvStartValue = CMultiVar[Double](255, 0, 0)
		gradation.SetStartValue(mvStartValue)

		# Gradation End Value 설정(3Ch) // Set Gradation End Value(3Ch)
		mvEndValue = CMultiVar[Double](0, 0, 255)
		gradation.SetEndValue(mvEndValue)

		# Gradation Vector Figure 객체 // Gradation Vector Figure object
		fllVector = CFLLine[Double]()
		fllVector.Load('../../ExampleImages/Gradation/Vector.fig')
		gradation.SetVector(fllVector)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := gradation.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Gradation.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# Draw Figure 객체 // Gradation Vector Figure object
		fllDrawVector = CFLFigureArray()
		fllDrawVector.Load('../../ExampleImages/Gradation/DrawVector.fig')

		fllRect1 = CFLRect[Double]()
		fllRect2 = CFLRect[Double]()

		fllRect1.left = fllVector.flpPoints[0].x - 15
		fllRect1.top = fllVector.flpPoints[0].y - 15
		fllRect1.right = fllVector.flpPoints[0].x + 15
		fllRect1.bottom = fllVector.flpPoints[0].y + 15

		fllRect2.left = fllVector.flpPoints[1].x - 15
		fllRect2.top = fllVector.flpPoints[1].y - 15
		fllRect2.right = fllVector.flpPoints[1].x + 15
		fllRect2.bottom = fllVector.flpPoints[1].y + 15

		if (res := layerSource.DrawFigureImage(fllRect1, EColor.BLUE, 5, EColor.BLUE, EGUIViewImagePenStyle.Solid)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		if (res := layerSource.DrawFigureImage(fllRect2, EColor.RED, 5, EColor.RED, EGUIViewImagePenStyle.Solid)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# Gradation Vector 출력 // Draw gradation vector
		if (res := layerSource.DrawFigureImage(fllDrawVector, EColor.BLACK, 5)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		if (res := layerSource.DrawFigureImage(fllDrawVector, EColor.LIME, 3)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# text를 출력합니다. // Display text.
		if (res := layerSource.DrawTextImage(fllVector.flpPoints[0], 'Start Value(255, 0, 0)/Start Alpha(0, 0, 0)', EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.RIGHT)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# View 정보를 디스플레이 합니다. // Display View information.
		if(res := layerSource.DrawTextImage(fllVector.flpPoints[1], 'End(0, 0, 255)/Start Alpha(0.1, 0.6, 0.9)', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)
		
		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()