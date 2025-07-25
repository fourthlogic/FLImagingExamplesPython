# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliCropImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageCrop = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Crop/bacteria.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Crop 이미지를 Source 이미지와 동일한 이미지로 생성 // Create crop image as same as source image
		if (res := fliCropImage.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Crop 이미지 뷰 생성 // Create the crop image view
		if (res := viewImageCrop.Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageCrop)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Crop 이미지 뷰에 이미지를 디스플레이 // Display the image in the crop image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCrop.SetImagePtr(fliCropImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageCrop)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Crop 객체 생성 // Create Crop object
		crop = CCrop()


		# Source 이미지 설정 // Set the source image
		crop.SetSourceImage(fliCropImage)

		# Crop ROI 지정 // Create ROI
		flrCropROI = CFLRect[Int32](161, 181, 293, 302)

		crop.SetSourceROI(flrCropROI)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := crop.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Crop.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerCrop = viewImageCrop.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerCrop.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)
		
		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerCrop.DrawTextCanvas(flpPoint, 'Crop Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# Crop 영역 표기 // Draw crop area
		if (res := layerSource.DrawFigureImage(flrCropROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.ZoomFit()
		viewImageSrc.Invalidate(True)
		viewImageCrop.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageCrop.IsAvailable():
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