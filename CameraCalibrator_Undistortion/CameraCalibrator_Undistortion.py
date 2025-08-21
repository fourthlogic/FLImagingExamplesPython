# FLImagingClrPy 선언 # Declare FLImagingClrPy
from asyncio.windows_events import NULL
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

def Undistortion(cameraCalibrator, fliSourceImage, fliDestinationImage, viewImageSource, viewImageDestination):
	bResult = False
	res = CResult()

	while True:
		# Source 이미지 로드 # Load the Source image
		if (res := fliSourceImage.Load('../../ExampleImages/CameraCalibrator/Undistortion.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		mvBlank = CMultiVar[Int64](0)

		# Destination 이미지 생성 # Create the Destination image
		if (res := fliDestinationImage.Create(fliSourceImage.GetWidth(), fliSourceImage.GetHeight(), mvBlank, fliSourceImage.GetPixelFormat())).IsFail():
			ErrorPrint(res, 'Failed to create the image file.')
			break

		# Source 이미지 뷰 생성 # Create the Source image view
		if (res := viewImageSource.Create(400, 480, 1040, 960)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the Destination image view
		if (res := viewImageDestination.Create(1040, 480, 1680, 960)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the Source ImageView
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the Destination image view
		if (res := viewImageDestination.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		if (res := viewImageSource.SynchronizeWindow(viewImageDestination)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Source 이미지 설정 # Set Source image
		if (res := cameraCalibrator.SetSourceImage(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image')
			break

		# Destination 이미지 설정 # Set Destination image
		if (res := cameraCalibrator.SetDestinationImage(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image')
			break

		# Interpolation 알고리즘 설정 # Set the Interpolation Algorithm
		if (res := cameraCalibrator.SetInterpolationMethod(EInterpolationMethod.Bilinear)).IsFail():
			ErrorPrint(res, 'Failed to set interpolation method')
			break

		sPC = CPerformanceCounter()
		sPC.Start()

		# Undistortion 실행 # Execute Undistortion
		if (res := cameraCalibrator.Execute()).IsFail():
			ErrorPrint(res, 'Undistortion failed')
			break

		sPC.CheckPoint()

		layerSource = viewImageSource.GetLayer(0)
		layerSource.Clear()
		
		layerDestination = viewImageDestination.GetLayer(0)
		layerDestination.Clear()

		ptTop = CFLPoint[Double](20,20)

		if (res := layerDestination.DrawTextImage(ptTop, "Undistortion - Bilinear method", EColor.GREEN, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text")
			break

		f64ElapsedMS = sPC.GetCheckPointInMilliSecond()
		strMS = "elapsed time: {0} ms".format(f64ElapsedMS)
		
		ptMS = CFLPoint[Double](20, 50)

		if (res := layerDestination.DrawTextImage(ptMS, strMS, EColor.GREEN, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text")
			break

		viewImageDestination.Invalidate(False)

		bResult = True
		break

	return bResult

# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageDestination = CGUIViewImage()

	# Camera Calibrator 객체 생성 # Create Camera Calibrator object
	cameraCalibrator = CCameraCalibrator()

	res = CResult()

	while True:
		arrF64Intrinc = [605.9413643192689, 0., 325.9133439121233, 0., 605.3834974915350, 234.0647625697701, 0., 0., 1.]
		arrF64Dist = [0.1748895907714, -1.4909467274276, -0.0070404809103, 0.0017880490098, 5.9363069879613]

		uIntrinc = CCameraCalibrator.CCalibratorIntrinsicParameters()
		uDist = CCameraCalibrator.CCalibratorDistortionCoefficients()

		uIntrinc.f64FocalLengthX = arrF64Intrinc[0]
		uIntrinc.f64Skew = arrF64Intrinc[1]
		uIntrinc.f64PrincipalPointX = arrF64Intrinc[2]
		uIntrinc.f64FocalLengthY = arrF64Intrinc[4]
		uIntrinc.f64PrincipalPointY = arrF64Intrinc[5]

		uDist.f64K1 = arrF64Dist[0]
		uDist.f64K2 = arrF64Dist[1]
		uDist.f64P1 = arrF64Dist[2]
		uDist.f64P2 = arrF64Dist[3]
		uDist.f64K3 = arrF64Dist[4]

		if (res := cameraCalibrator.SetIntrinsicParameters(uIntrinc)).IsFail():
			ErrorPrint(res, "Failed to set intrinsic parameters")
			break

		if (res := cameraCalibrator.SetDistortionCoefficients(uDist)).IsFail():
			ErrorPrint(res, "Failed to set distortion coefficients")
			break

		if (res := cameraCalibrator.EnableAutoCalibration(False)).IsFail():
			ErrorPrint(res, "Failed to auto calibration\n")
			break

		if (res := cameraCalibrator.Calibrate()).IsFail():
			ErrorPrint(res, "Failed to calibration\n")
			break

		if not Undistortion(cameraCalibrator, fliSourceImage, fliDestinationImage, viewImageSource, viewImageDestination):
			break

		layerSource = viewImageSource.GetLayer(0)
		strMatrix = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}".format(uIntrinc.f64FocalLengthX, uIntrinc.f64Skew, uIntrinc.f64PrincipalPointX, 0, uIntrinc.f64FocalLengthY, uIntrinc.f64PrincipalPointY, 0, 0, 1)
		strDistVal = "{0}, {1}, {2}, {3}, {4}".format(uDist.f64K1, uDist.f64K2, uDist.f64P1, uDist.f64P2, uDist.f64K3)
		tpPosition = TPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(tpPosition, "Intrinsic Parameters: ", EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		tpPosition.y += 20

		if (res := layerSource.DrawTextCanvas(tpPosition, strMatrix, EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		tpPosition.y += 20

		if (res := layerSource.DrawTextCanvas(tpPosition, "Distortion Coefficients: ", EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		tpPosition.y += 20

		if (res := layerSource.DrawTextCanvas(tpPosition, strDistVal, EColor.YELLOW, EColor.BLACK, 13)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		viewImageSource.Invalidate()

		print("Intrinsic parameters :", strMatrix)
		print("Distortion Coefficients :", strDistVal)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the imageview to close
		while viewImageSource.IsAvailable() and viewImageDestination.IsAvailable():
			CThreadUtilities.Sleep(1)

		break

if __name__ == '__main__':
    main()


