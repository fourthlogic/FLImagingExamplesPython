# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliLearnImage = CFLImage()
	fliImage1 = CFLImage()
	fliImage2 = CFLImage()

	# ROI 선언 # Declare the ROI
	flfaROI1 = CFLFigureArray()
	flfaROI2 = CFLFigureArray()

	# 이미지 뷰 선언 # Declare the image view
	viewImage1 = CGUIViewImage()
	viewImage2 = CGUIViewImage()

	while True:
		
		# 이미지 로드 # Load the image
		if (res := fliLearnImage.Load('../../ExampleImages/OCV/FourthLogic Inc_Learn.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliImage1.Load('../../ExampleImages/OCV/FourthLogic Inc.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliImage2.Load("../../ExampleImages/OCV/FourthLogic Inc 2.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# ROI 로드 # Load ROI
		if (res := flfaROI1.Load('../../ExampleImages/OCV/FourthLogic Inc_ROI 1.fig')).IsFail():
			ErrorPrint(res, 'Failed to load the ROI file.')
			break

		if (res := flfaROI2.Load("../../ExampleImages/OCV/FourthLogic Inc_ROI 2.fig")).IsFail():
			ErrorPrint(res, 'Failed to load the ROI file.')
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImage1.Create(100, 0, 550, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImage2.Create(550, 0, 1050, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage1.SetImagePtr(fliImage1)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImage2.SetImagePtr(fliImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer1 = viewImage1.GetLayer(0)
		layer2 = viewImage2.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer1.Clear()
		layer2.Clear()

		# 학습을 진행할 OCR 객체 생성 # Create OCR object to Learn
		ocr = COCR()

		# 문자를 학습할 이미지 설정
		if (res := ocr.SetLearnImage(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Learn Image.')
			break

		# 학습할 이미지에 저장되어있는 Figure 학습
		if (res := ocr.Learn()).IsFail():
			ErrorPrint(res, 'Failed to learn.')
			break

		# 인식할 문자의 각도 범위를 설정
		if (res := ocr.SetRecognizingAngleTolerance(9.0)).IsFail():
			ErrorPrint(res, 'Failed to set recognizing angle tolerance.')
			break

		# 인식할 문자의 유니코드 여부를 설정
		if (res := ocr.EnableRecognizingUnicodeByteCharacter(True)).IsFail():
			ErrorPrint(res, 'Failed to Enable unicode byte character.')
			break

		# 학습 정보 파일 및 입력 파라미터를 저장
		if (res := ocr.Save('../../ExampleImages/OCV/OCR_FourthLogic.flocr')).IsFail():
			ErrorPrint(res, 'Failed to save learned file.')
			break
		
		# 객체 생성 # Create object
		ocv = COCV()

		# 학습 정보 파일을 로드
		ocv.LoadFontData("../../ExampleImages/OCV/OCR_FourthLogic.flocr")

		# 정규표현식 사용 여부 설정
		ocv.EnableRegularExpression(True)

		# 인트루전 검증 여부를 설정 (해당 예제에서는 퀄리티 검증을 배제함)
		ocv.EnableIntrusionInspection(False)

		# 익스트루전 검증 여부를 설정 (해당 예제에서는 퀄리티 검증을 배제함)
		ocv.EnableExtrusionInspection(False)

		# 문자를 검증할 이미지 설정
		ocv.SetSourceImage(fliImage1)

		# ROI 설정
		ocv.SetSourceROI(flfaROI1)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := ocv.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		if (res := layer1.DrawFigureImage(flfaROI1, EColor.LIME, 5)).IsFail():
			ErrorPrint(res, 'Failed to draw Source ROI')
			break

		for i in range(flfaROI1.GetCount()):
			flqROI = CFLQuad[float](flfaROI1.GetAt(i))

			if (res := layer1.DrawTextImage(flqROI.flpPoints[0], flqROI.GetName(), EColor.LIME, EColor.BLACK, 20, False, 0.0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw text')
				break

		if (res := layer1.DrawTextCanvas(CFLPoint[float](0, 0), "Verify" if ocv.GetResultVerificationState() == COCV.EVerificationState.OK else "Fail", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
			break

		# 찾은 문자의 개수를 받아오는 함수
		i64ResultCount = ocv.GetResultCount()

		# 찾은 문자의 정보를 받아올 컨테이너
		resultChar = COCV.COCVVerificationCharacterInfo()

		for i in range(i64ResultCount):
			ocv.GetResultVerificationCharactersInfo(i, resultChar)
			flsResultName = resultChar.flfaCharacter.GetName()
			i32Quality = int(resultChar.f64Quality * 100.0)
			f64Scale = resultChar.f64ScaleWidth * resultChar.f64ScaleHeight
			flrBoundary = resultChar.flrBoundary
			fllBlankSpaceWidth = resultChar.fllBlankSpaceWidthLine

			flsResultString = "[" + flsResultName + "]" + "Quality: {0}%\nScale: {1:.2f}\nAngle: {2}\nLighting: {3:.2f}\nContrast: {4:.2f}".format(i32Quality, (resultChar.f64ScaleWidth * resultChar.f64ScaleHeight), resultChar.f64Rotation, resultChar.f64Lighting, resultChar.f64Contrast)
			flsResultString2 = "Space Width: {0:.2f}".format(resultChar.f64BlankSpaceWidth)

			if (res := layer1.DrawTextImage(CFLPoint[float](flrBoundary.left, flrBoundary.top), flsResultString, EColor.YELLOW, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layer1.DrawFigureImage(resultChar.flfaCharacter, EColor.LIME, 1, EColor.LIME, EGUIViewImagePenStyle.Solid, 1.0, 0.35)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layer1.DrawFigureImage(flrBoundary, EColor.GREEN if resultChar.bVerified else EColor.RED, 3, EColor.GREEN if resultChar.bVerified else EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, 0.0)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			layer1.DrawFigureImage(resultChar.flfaIntrusion, EColor.YELLOW, 1, EColor.YELLOW, EGUIViewImagePenStyle.Solid, 1.0, 0.3)
			layer1.DrawFigureImage(resultChar.flfaExtrusion, EColor.BLUE, 1, EColor.BLUE, EGUIViewImagePenStyle.Solid, 1.0, 0.3)

			if (res := layer1.DrawFigureImage(fllBlankSpaceWidth, EColor.BLACK, 3, EColor.BLACK, EGUIViewImagePenStyle.Solid, 1.0, 0.35)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layer1.DrawTextImage(CFLPointArray(fllBlankSpaceWidth).GetAt(0), flsResultString2, EColor.YELLOW, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

		# 문자를 검증할 이미지 설정
		ocv.SetSourceImage(fliImage2)

		# ROI 설정
		ocv.SetSourceROI(flfaROI2)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := ocv.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		if (res := layer2.DrawFigureImage(flfaROI2, EColor.LIME, 5)).IsFail():
			ErrorPrint(res, 'Failed to draw Source ROI')
			break

		for i in range(flfaROI2.GetCount()):
			flqROI = CFLQuad[float](flfaROI2.GetAt(i))

			if (res := layer2.DrawTextImage(flqROI.flpPoints[0], flqROI.GetName(), EColor.LIME, EColor.BLACK, 20, False, 0.0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw text')
				break

		if (res := layer2.DrawTextCanvas(CFLPoint[float](0, 0), "Verify" if ocv.GetResultVerificationState() == COCV.EVerificationState.OK else "Fail", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
			break

		# 찾은 문자의 개수를 받아오는 함수
		i64ResultCount = ocv.GetResultCount()

		# 찾은 문자의 정보를 받아올 컨테이너
		resultChar = COCV.COCVVerificationCharacterInfo()

		for i in range(i64ResultCount):
			ocv.GetResultVerificationCharactersInfo(i, resultChar)
			flsResultName = resultChar.flfaCharacter.GetName()
			i32Quality = int(resultChar.f64Quality * 100.0)
			f64Scale = resultChar.f64ScaleWidth * resultChar.f64ScaleHeight
			flrBoundary = resultChar.flrBoundary
			fllBlankSpaceWidth = resultChar.fllBlankSpaceWidthLine

			flsResultString = "[" + flsResultName + "]" + "Quality: {0}%\nScale: {1:.2f}\nAngle: {2}\nLighting: {3:.2f}\nContrast: {4:.2f}".format(i32Quality, (resultChar.f64ScaleWidth * resultChar.f64ScaleHeight), resultChar.f64Rotation, resultChar.f64Lighting, resultChar.f64Contrast)
			flsResultString2 = "Space Width: {0:.2f}".format(resultChar.f64BlankSpaceWidth)

			if (res := layer2.DrawTextImage(CFLPoint[float](flrBoundary.left, flrBoundary.top), flsResultString, EColor.YELLOW, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layer2.DrawFigureImage(resultChar.flfaCharacter, EColor.LIME, 1, EColor.LIME, EGUIViewImagePenStyle.Solid, 1.0, 0.35)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layer2.DrawFigureImage(flrBoundary, EColor.GREEN if resultChar.bVerified else EColor.RED, 3, EColor.GREEN if resultChar.bVerified else EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, 0.0)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			layer2.DrawFigureImage(resultChar.flfaIntrusion, EColor.YELLOW, 1, EColor.YELLOW, EGUIViewImagePenStyle.Solid, 1.0, 0.3)
			layer2.DrawFigureImage(resultChar.flfaExtrusion, EColor.BLUE, 1, EColor.BLUE, EGUIViewImagePenStyle.Solid, 1.0, 0.3)

			if (res := layer2.DrawFigureImage(fllBlankSpaceWidth, EColor.BLACK, 3, EColor.BLACK, EGUIViewImagePenStyle.Solid, 1.0, 0.35)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

			if (res := layer2.DrawTextImage(CFLPointArray(fllBlankSpaceWidth).GetAt(0), flsResultString2, EColor.YELLOW, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw recognized character : {0}'.format(i))
				break

		# 이미지 뷰를 갱신 # Update image view
		viewImage1.Invalidate(True)
		viewImage2.Invalidate(True)
		
		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImage1.IsAvailable() and viewImage2.IsAvailable():
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






