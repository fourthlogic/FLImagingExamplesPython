# FLImagingClrPy 선언 // Declare FLImagingClrPy
from asyncio.windows_events import NULL
from FLImagingClrPy import *

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

def Calibration(sCC, fliLearnImage):
	bResult = False
	res = CResult()

	while True:
		# Learn 이미지 설정 // Learn image settings
		if (res := sCC.SetCalibrationImage(fliLearnImage))[0].IsFail():
			ErrorPrint(res, 'Failed to set image')
			break

		# Calibator할 대상 종류를 설정합니다. // Set the target type for Calibator.
		sCC.SetGridType(CCameraCalibrator.EGridType.GridOfDots)
		# 결과에 대한 학습률을 설정합니다.
		sCC.SetOptimalSolutionAccuracy(1e-5)

		# Calibration 실행 // Execute Calibration
		if (res := sCC.Calibrate()).IsFail():
			ErrorPrint(res, 'Calibration failed')
			break

		bResult = True
		break

	return bResult

def Undistortion(sCC, fliSourceImage, fliDestinationImage):
	bResult = False
	res = CResult()

	while True:
		# Source 이미지 설정 // Set Source image
		if (res := sCC.SetSourceImage(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image')
			break

		# Destination 이미지 설정 // Set Destination image
		if (res := sCC.SetDestinationImage(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image')
			break

		# Interpolation 알고리즘 설정 // Set the Interpolation Algorithm
		if (res := sCC.SetInterpolationMethod(EInterpolationMethod.Bilinear)).IsFail():
			ErrorPrint(res, 'Failed to set interpolation method')
			break

		# Undistortion 실행 // Execute Undistortion
		if (res := sCC.Execute()).IsFail():
			ErrorPrint(res, 'Undistortion failed')
			break

		bResult = True
		break

	return bResult

# 메인 함수 // Main function
def main():
	# 이미지 객체 선언 // Declare the image object
	fliLearnImage = CFLImage()
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()
	fliLearnImageCopy = CFLImage()
	fliDisplay = CFLImage()
	arrFliDisplay = [CFLImage(), CFLImage(), CFLImage()]

	# 이미지 뷰 선언 // Declare the image view
	viewImageLearn = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]
	viewImageSource = CGUIViewImage()
	viewImageDestination = CGUIViewImage()

	# Camera Calibrator 객체 생성 // Create Camera Calibrator object
	sCC = CCameraCalibrator()
	res = CResult()

	while True:
		# Learn 이미지 로드 // Load the Learn image
		if (res := fliLearnImage.Load('../../ExampleImages/CameraCalibrator/GridOfDots/GridOfDots.flif')).IsFail():
			ErrorPrint(res, 'Failed to set image')
			break

		print('Processing....')

		fliLearnImageCopy.Assign(fliLearnImage, True)
		fliDisplay.Assign(fliLearnImageCopy, True)
		arrFliDisplay[0].SwapPage(fliDisplay, 0)
		arrFliDisplay[1].SwapPage(fliDisplay, 1)
		arrFliDisplay[2].SwapPage(fliDisplay, 2)

		for i in range(3):
			# Learn 이미지 뷰 생성 // Create the Learn image view
			if (res := viewImageLearn[i].Create(300 + 480 * i, 0, 300 + 480 * (i + 1), 360)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				break

			# Learn 이미지 뷰에 이미지를 디스플레이 // Display the image in the Learn image view
			if (res := viewImageLearn[i].SetImagePtr(arrFliDisplay[i]))[0].IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				break

		if not Calibration(sCC, fliLearnImage):
			break
		
		# Source 이미지 로드 // Load the Source image
		if (res := fliSourceImage.Load('../../ExampleImages/CameraCalibrator/GridOfDots/GridOfDots (1).flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		mvBlank = CMultiVar[Int64](0)

		# Destination 이미지 생성 // Create the Destination image
		if (res := fliDestinationImage.Create(fliSourceImage.GetWidth(), fliSourceImage.GetHeight(), mvBlank, fliSourceImage.GetPixelFormat())).IsFail():
			ErrorPrint(res, 'Failed to create the image file.')
			break

		if not Undistortion(sCC, fliSourceImage, fliDestinationImage):
			break

		sArrGridDisplay = [dict(), dict(), dict()]

		for i in range(3):
			sArrGridDisplay[i]['i64ImageIdx'] = 0
			sArrGridDisplay[i]['i64ObjectIdx'] = 0
			sArrGridDisplay[i]['sGridData'] = CCameraCalibrator.CCalibratorGridResult()

		for i64ImgIdx in range(fliLearnImage.GetPageCount()):
			i64ObjectCount = sCC.GetResultGridPointsObjectCnt(i64ImgIdx)

			for i64ObjectIdx in range(i64ObjectCount):
				sCC.GetResultGridPoints(i64ObjectIdx, i64ImgIdx, sArrGridDisplay[i64ImgIdx]['sGridData'])
				sArrGridDisplay[i64ImgIdx]['i64ImageIdx'] = i64ImgIdx
				sArrGridDisplay[i64ImgIdx]['i64ObjectIdx'] = sArrGridDisplay[i64ImgIdx]['sGridData'].i64ID

		for i in range(3):
			layerLearn = viewImageLearn[i].GetLayer(0)

			layerLearn.Clear()

			colorPool = [EColor.RED, EColor.LIME, EColor.CYAN]
			i64GridRow = int(sArrGridDisplay[i]['sGridData'].i64Rows)
			i64GridCol = int(sArrGridDisplay[i]['sGridData'].i64Columns)

			for i64Row in range(i64GridRow):
				for i64Col in range(i64GridCol - 1):
					i64GridIdx = i64Row * i64GridCol + i64Col

					pFlpGridPoint1 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(i64Col))
					pFlpGridPoint2 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(i64Col + 1))
					fllDrawLine = CFLLine[Double](pFlpGridPoint1, pFlpGridPoint2)

					if (res := layerLearn.DrawFigureImage(fllDrawLine, EColor.BLACK, 5)).IsFail():
						ErrorPrint(res, 'Failed to draw figure')
						break

					if (res := layerLearn.DrawFigureImage(fllDrawLine, colorPool[i64GridIdx % 3], 3)).IsFail():
						ErrorPrint(res, 'Failed to draw figure')
						break

				if i64Row < i64GridRow - 1:
					pFlpGridPoint1 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(i64GridCol - 1))
					pFlpGridPoint2 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row + 1)).GetAt(0))
					fllDrawLine = CFLLine[Double](pFlpGridPoint1, pFlpGridPoint2)

					if (res := layerLearn.DrawFigureImage(fllDrawLine, EColor.BLACK, 5)).IsFail():
						ErrorPrint(res, 'Failed to draw figure')
						break

					if (res := layerLearn.DrawFigureImage(fllDrawLine, EColor.YELLOW, 3)).IsFail():
						ErrorPrint(res, 'Failed to draw figure')
						break

			colorText = EColor.YELLOW
			colorPool[2] = EColor.CYAN

			for i64Row in range(i64GridRow):
				tpGridPoint1 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(0))
				tpGridPoint2 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(1))
				flpGridPoint1 = CFLPoint[Double](tpGridPoint1.x, tpGridPoint1.y)
				flpGridPoint2 = CFLPoint[Double](tpGridPoint2.x, tpGridPoint2.y)
				f64AngleIner = flpGridPoint1.GetAngle(flpGridPoint2)

				for i64Col in range(i64GridCol):
					i64GridIdx = i64Row * i64GridCol + i64Col

					if i64Col < i64GridCol - 1:
						tpGridPoint1 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(i64Col))
						tpGridPoint2 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(i64Col + 1))

						f64Dx = tpGridPoint2.x - tpGridPoint1.x
						f64Dy = tpGridPoint2.y - tpGridPoint1.y
						f64PointDist = (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5

					if i64Row > 0:
						tpGridPoint1 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row)).GetAt(i64Col))
						tpGridPoint2 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(i64Row - 1)).GetAt(i64Col))

						f64Dx = tpGridPoint2.x - tpGridPoint1.x
						f64Dy = tpGridPoint2.y - tpGridPoint1.y
						f64PointDist = min(f64PointDist, (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5)
					else:
						tpGridPoint1 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(0)).GetAt(i64Col))
						tpGridPoint2 = CFLPoint[Double](CFLFigureArray(sArrGridDisplay[i]['sGridData'].flfaGridData.GetAt(1)).GetAt(i64Col))

						f64Dx = tpGridPoint2.x - tpGridPoint1.x
						f64Dy = tpGridPoint2.y - tpGridPoint1.y
						f64PointDist = min(f64PointDist, (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5)

					wstrGridIdx = "{0}".format(i64GridIdx)
					colorText = colorPool[i64GridIdx % 3]

					if i64Col == i64GridCol - 1:
						colorText = EColor.YELLOW

					if (res := layerLearn.DrawTextImage(tpGridPoint1, wstrGridIdx, colorText, EColor.BLACK, int(f64PointDist / 2), True, f64AngleIner)).IsFail():
						ErrorPrint(res, 'Failed to draw text')
						break

			flqBoardRegion = sArrGridDisplay[i]['sGridData'].pFlqBoardRegion
			flpPoint1 = CFLPoint[Double](flqBoardRegion.flpPoints[0])
			flpPoint2 = CFLPoint[Double](flqBoardRegion.flpPoints[1])
			f64Angle = flpPoint1.GetAngle(flpPoint2)
			wstringData = "[{0}] ({1} X {2})".format(sArrGridDisplay[i]['sGridData'].i64ID, sArrGridDisplay[i]['sGridData'].i64Columns, sArrGridDisplay[i]['sGridData'].i64Rows)

			if (res := layerLearn.DrawFigureImage(flqBoardRegion, EColor.YELLOW, 3)).IsFail():
				ErrorPrint(res, 'Failed to draw figure')
				break

			if (res := layerLearn.DrawTextImage(flpPoint1, wstringData, EColor.YELLOW, EColor.BLACK, 15, False, f64Angle, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw text')
				break

			viewImageLearn[i].Invalidate()

		# Source 이미지 뷰 생성 // Create the Source image view
		if (res := viewImageSource.Create(300, 360, 780, 720)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the Destination image view
		if (res := viewImageDestination.Create(780, 360, 1260, 720)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the Source ImageView
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the Destination image view
		if (res := viewImageDestination.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		for i in range(3):
			# 두 이미지 뷰의 시점을 동기화 한다. // Synchronize the viewpoints of the two image views.
			if (res := viewImageLearn[i].SynchronizePointOfView(viewImageSource)[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view')
				break

			# 두 이미지 뷰의 시점을 동기화 한다. // Synchronize the viewpoints of the two image views.
			if (res := viewImageLearn[i].SynchronizePointOfView(viewImageDestination)[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view')
				break

			# 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
			if (res := viewImageLearn[i].SynchronizeWindow(viewImageSource)[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				break

			# 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
			if (res := viewImageLearn[i].SynchronizeWindow(viewImageDestination)[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				break

		layerSource = viewImageSource.GetLayer(0)
		sIntrinsicParam = sCC.GetResultIntrinsicParameters()
		sDistortCoeef = sCC.GetResultDistortionCoefficients()
		strMatrix = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}".format(sIntrinsicParam.f64FocalLengthX, sIntrinsicParam.f64Skew, sIntrinsicParam.f64PrincipalPointX, 0, sIntrinsicParam.f64FocalLengthY, sIntrinsicParam.f64PrincipalPointY, 0, 0, 1)
		strDistVal = "{0}, {1}, {2}, {3}, {4}".format(sDistortCoeef.f64K1, sDistortCoeef.f64K2, sDistortCoeef.f64P1, sDistortCoeef.f64P2, sDistortCoeef.f64K3)

		print("Intrinsic parameters")
		print(strMatrix)
		print("Distortion Coefficients")
		print(strDistVal)

		tpScreen = TPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(tpScreen, "Intrinsic Parameters: ", EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		tpScreen.y += 20

		if (res := layerSource.DrawTextCanvas(tpScreen, strMatrix, EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		tpScreen.y += 20

		if (res := layerSource.DrawTextCanvas(tpScreen, "Distortion Coefficients: ", EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		tpScreen.y += 20

		if (res := layerSource.DrawTextCanvas(tpScreen, strDistVal, EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		layerDestination = viewImageDestination.GetLayer(0)

		layerDestination.Clear()

		ptTop = TPoint[Double](20, 20)

		if (res := layerDestination.DrawTextImage(ptTop, "Undistortion - Bilinear method", EColor.GREEN, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		viewImageSource.Invalidate()
		viewImageDestination.Invalidate()

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the imageview to close
		while viewImageLearn[0].IsAvailable() and viewImageLearn[1].IsAvailable() and viewImageLearn[2].IsAvailable() and viewImageSource.IsAvailable() and viewImageDestination.IsAvailable():
			CThreadUtilities.Sleep(1)

		break

if __name__ == '__main__':
    main()

