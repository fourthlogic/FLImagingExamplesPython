# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliRecognitionImage = CFLImage()
	fliRecognitionImageUnicode = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageRec = CGUIViewImage()
	viewImageRecUnicode = CGUIViewImage()

	while True:
		
		# Recognition 이미지 로드 // Load the learn image
		if (res := fliRecognitionImage.Load('../../ExampleImages/OCR/OCR_Recognition.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Recognition 이미지를 로드 // Load the recognition image
		if (res := fliRecognitionImageUnicode.Load("../../ExampleImages/OCR/OCR_Recognition_Unicode2.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Recognition 이미지 뷰 생성 // Create learn image view
		if (res := viewImageRec.Create(100, 0, 550, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Recognition 이미지 뷰 생성 // Create the recognition image view
		if (res := viewImageRecUnicode.Create(550, 0, 1050, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Recognition 이미지 뷰에 이미지를 디스플레이 // Display the image in the learn image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageRec.SetImagePtr(fliRecognitionImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Recognition 이미지 뷰에 이미지를 디스플레이 // Display the image in the recognition image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageRecUnicode.SetImagePtr(fliRecognitionImageUnicode)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerRecognition = viewImageRec.GetLayer(0)
		layerRecognitionUnicode = viewImageRecUnicode.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerRecognition.Clear()
		layerRecognitionUnicode.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerRecognition.DrawTextCanvas(flpPoint, 'Recognition Image 1', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerRecognitionUnicode.DrawTextCanvas(flpPoint, 'Recognition Image 2', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 객체 생성 // Create object
		ocr = COCR()

		# 학습 정보 파일을 로드
		ocr.Load("../../ExampleImages/OCR/OCR_FourthLogic.flocr")

		# Recognition 이미지 설정 // Set the recognition image
		ocr.SetSourceImage(fliRecognitionImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := ocr.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 찾은 문자의 개수를 받아오는 함수
		i64ResultCount = ocr.GetResultCount()

		# 찾은 문자의 정보를 받아올 컨테이너
		resultChar = COCR.COCRRecognitionCharacterInfo()

		for i in range(i64ResultCount):
			ocr.GetResultRecognizedCharactersInfo(i, resultChar)
			flsResultString = ''
			flsResultName = resultChar.flfaCharacter.GetName()
			i32Score = int(resultChar.f64Score * 100.0)
			f64Scale = resultChar.f64ScaleWidth * resultChar.f64ScaleHeight
			flsResultString = "[" + flsResultName + "]" + "Score: {0}%\nScale: {1:.2f}\nRotation: {2}".format(i32Score, f64Scale, resultChar.f64Rotation)
			flrBoundary = CFLRect[float]()
			resultChar.flfaCharacter.GetBoundaryRect(flrBoundary)

			if (res := layerRecognition.DrawTextImage(CFLPoint[float](flrBoundary.left, flrBoundary.top), flsResultString, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layerRecognition.DrawFigureImage(resultChar.flfaCharacter, EColor.LIME, 1, EColor.LIME, EGUIViewImagePenStyle.Solid, 1.0, 0.35)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

		# Recognition 이미지 설정 // Set the recognition image
		ocr.SetSourceImage(fliRecognitionImageUnicode)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := ocr.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 찾은 문자의 개수를 받아오는 함수
		i64ResultCount = ocr.GetResultCount()

		# 찾은 문자의 정보를 받아올 컨테이너
		resultChar = COCR.COCRRecognitionCharacterInfo()

		for i in range(i64ResultCount):
			ocr.GetResultRecognizedCharactersInfo(i, resultChar)
			flsResultString = ''
			flsResultName = resultChar.flfaCharacter.GetName()
			i32Score = int(resultChar.f64Score * 100.0)
			f64Scale = resultChar.f64ScaleWidth * resultChar.f64ScaleHeight
			flsResultString = "[" + flsResultName + "]" + "Score: {0}%\nScale: {1:.2f}\nRotation: {2}".format(i32Score, f64Scale, resultChar.f64Rotation)
			flrBoundary = CFLRect[float]()
			resultChar.flfaCharacter.GetBoundaryRect(flrBoundary)

			if (res := layerRecognitionUnicode.DrawTextImage(CFLPoint[float](flrBoundary.left, flrBoundary.top), flsResultString, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layerRecognitionUnicode.DrawFigureImage(resultChar.flfaCharacter, EColor.LIME, 1, EColor.LIME, EGUIViewImagePenStyle.Solid, 1.0, 0.35)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

		# 이미지 뷰를 갱신 // Update image view
		viewImageRec.Invalidate(True)
		viewImageRecUnicode.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageRec.IsAvailable() and viewImageRecUnicode.IsAvailable():
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




