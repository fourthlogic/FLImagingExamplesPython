# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliLearnImage = CFLImage()
	fliRecognitionImage = CFLImage()
	fliRecognitionImageUnicode = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageRec = CGUIViewImage()
	viewImageRecUnicode = CGUIViewImage()

	while True:

		# Learn 이미지 로드 // Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/OCR/FourthLogic Inc_Learn.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Recognition 이미지 로드 // Load the recognition image
		if (res := fliRecognitionImage.Load('../../ExampleImages/OCR/OCR_Recognition.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Recognition 이미지를 로드 // Load the recognition image
		if (res := fliRecognitionImageUnicode.Load("../../ExampleImages/OCR/OCR_Recognition_Unicode2.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Recognition 이미지 뷰 생성 // Create the recognition image view
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

		# 학습을 진행할 OCR 객체 생성 // Create OCR object to Learn
		ocrLearn = COCR()

		# 문자를 학습할 이미지 설정
		if (res := ocrLearn.SetLearnImage(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Learn Image.')
			break

		# 학습할 이미지에 저장되어있는 Figure 학습
		if (res := ocrLearn.Learn()).IsFail():
			ErrorPrint(res, 'Failed to learn.')
			break

		# 인식할 문자의 각도 범위를 설정
		if (res := ocrLearn.SetRecognizingAngleTolerance(9.0)).IsFail():
			ErrorPrint(res, 'Failed to set recognizing angle tolerance.')
			break

		# 인식할 문자의 색상을 설정
		if (res := ocrLearn.SetRecognizingCharacterColorType(ECharacterColorType.All)).IsFail():
			ErrorPrint(res, 'Failed to set recognizing character color.')
			break

		# 인식할 최소 점수를 설정
		if (res := ocrLearn.SetRecognizingMinimumScore(0.7)).IsFail():
			ErrorPrint(res, 'Failed to set minimum score.')
			break

		# 인식할 최대 개수를 설정
		if (res := ocrLearn.SetRecognizingMaximumCharacterCount(20)).IsFail():
			ErrorPrint(res, 'Failed to set maximum character count.')
			break

		# 인식할 문자의 유니코드 여부를 설정
		if (res := ocrLearn.EnableRecognizingUnicodeByteCharacter(True)).IsFail():
			ErrorPrint(res, 'Failed to Enable unicode byte character.')
			break

		# 학습 정보 파일 및 입력 파라미터를 저장
		if (res := ocrLearn.Save('../../ExampleImages/OCR/OCR_FourthLogic.flocr')).IsFail():
			ErrorPrint(res, 'Failed to save learned file.')
			break

		# 객체 생성 // Create object
		ocrLoad = COCR()

		# 학습 정보 파일을 로드
		ocrLoad.Load("../../ExampleImages/OCR/OCR_FourthLogic.flocr")

		# Recognition 이미지 설정 // Set the recognition image
		ocrLoad.SetSourceImage(fliRecognitionImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := ocrLoad.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 찾은 문자의 개수를 받아오는 함수
		i64ResultCount = ocrLoad.GetResultCount()

		# 찾은 문자의 정보를 받아올 컨테이너
		resultChar = COCR.COCRRecognitionCharacterInfo()

		for i in range(i64ResultCount):
			ocrLoad.GetResultRecognizedCharactersInfo(i, resultChar)
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
		ocrLoad.SetSourceImage(fliRecognitionImageUnicode)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := ocrLoad.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 찾은 문자의 개수를 받아오는 함수
		i64ResultCount = ocrLoad.GetResultCount()

		# 찾은 문자의 정보를 받아올 컨테이너
		resultChar = COCR.COCRRecognitionCharacterInfo()

		for i in range(i64ResultCount):
			ocrLoad.GetResultRecognizedCharactersInfo(i, resultChar)
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




