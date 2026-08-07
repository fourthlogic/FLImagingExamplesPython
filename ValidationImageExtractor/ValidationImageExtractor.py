# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliResultLearnImage = CFLImage()
	fliResultValidationImage = CFLImage()
	
	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImagesLearn = CGUIViewImage()
	viewImagesValidation = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/SemanticSegmentation/Train.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Operand 이미지 로드 # Load the operand image
		if (res := fliResultLearnImage.Load('../../ExampleImages/SemanticSegmentation/Validation.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

	
		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 600, 500)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Operand 이미지 뷰 생성 # Create operand image view
		if (res := viewImagesLearn.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImagesValidation.Create(1100, 0, 1700, 500)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Operand 이미지 뷰에 이미지를 디스플레이 # Display the image in the operand image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImagesLearn.SetImagePtr(fliResultLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImagesValidation.SetImagePtr(fliResultValidationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 세 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the three image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImagesLearn)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageSrc.SynchronizePointOfView(viewImagesValidation)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImagesLearn)[0]).IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break

		if (res := viewImageSrc.SynchronizeWindow(viewImagesValidation)[0]).IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerOprand = viewImagesLearn.GetLayer(0)
		layerDestination = viewImagesValidation.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerOprand.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'SOURCE', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerOprand.DrawTextCanvas(flpPoint, 'TRAIN(EXTRACTED (3/4))', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpPoint, 'VALIDATION(EXTRACTED (1/4))', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# Validation Image Extractor DL 객체 생성 # Create Validation Image Extractor DL
		validationImageExtractorDL = CValidationImageExtractorDL()

		# Source 이미지 설정 # Set the source image
		validationImageExtractorDL.SetSourceImage(fliSourceImage)
		validationImageExtractorDL.SetResultLearningImage(fliResultLearnImage)
		# 결과 검증 이미지 설정 # Set the result validation image
		validationImageExtractorDL.SetResultValidationImage(fliResultValidationImage)
		# 데이터 유닛 설정 # Set the unit of data
		validationImageExtractorDL.SetDataUnit(CValidationImageExtractorDL.EDataUnit.Image);
		# 클래스 비율 보장 여부 설정 # Set whether to apply class ratio preservation
		validationImageExtractorDL.EnableClassRatioPreservation(True);
		# Validation Image 비율 설정 # Set ratio of validation image
		validationImageExtractorDL.SetValidationRatio(0.4)
	
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := validationImageExtractorDL.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Validation Image Extractor DL.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImagesLearn.ZoomFit()
		viewImagesValidation.ZoomFit()
		viewImageSrc.RedrawWindow()
		viewImagesLearn.RedrawWindow()
		viewImagesValidation.RedrawWindow()

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImagesValidation.IsAvailable() and viewImagesLearn.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()