# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare image object
	fliDistortionChessBoard = CFLImage()
	fliUndistortedChessBoard = CFLImage()
	fliDistortedMeasurementImage = CFLImage()
	fliUndistortedMeasurementImage = CFLImage()

	# 이미지 뷰 선언 // Declare image view
	viewImageDistortionChessBoard = CGUIViewImage()
	viewImageUndistortionChessBoard = CGUIViewImage()
	viewImageDistortionMeasurement = CGUIViewImage()
	viewImageUndistortionMeasurement = CGUIViewImage()

	while True:
		
		# Image View 생성 // Create image view
		if(res := viewImageDistortionChessBoard.Create(0, 0, 500, 500)).IsFail() :		
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Image View 생성 // Create image view
		if(res := viewImageUndistortionChessBoard.Create(500, 0, 1000, 500)).IsFail() :		
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Image View 생성 // Create image view
		if(res := viewImageDistortionMeasurement.Create(0, 500, 500, 1000)).IsFail() :		
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Image View 생성 // Create image view
		if(res := viewImageUndistortionMeasurement.Create(500, 500, 1000, 1000)).IsFail() :		
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if(res := viewImageDistortionChessBoard.SetImagePtr(fliDistortionChessBoard))[0].IsFail() :
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if(res := viewImageUndistortionChessBoard.SetImagePtr(fliUndistortedChessBoard))[0].IsFail() :
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if(res := viewImageDistortionMeasurement.SetImagePtr(fliDistortedMeasurementImage))[0].IsFail() :
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if(res := viewImageUndistortionMeasurement.SetImagePtr(fliUndistortedMeasurementImage))[0].IsFail() :
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Orthogonal Calibrator 클래스 선언 // Declare COrthogonal Calibrator class instance.
		orthogonalCalibrator = COrthogonalCalibrator()

		# Learn 이미지 로드 // Load the Learn image
		if(res := fliDistortionChessBoard.Load('C:\\Users\\Public\\Documents\\FLImaging\\ExampleImages\\Measurement\\ChessBoard.flif')).IsFail() :		
			ErrorPrint(res, 'Failed to load the image file.')
			break
		

		if not Calibration(orthogonalCalibrator, fliDistortionChessBoard) :
			break

		if not Undistortion(orthogonalCalibrator, fliDistortionChessBoard, fliUndistortedChessBoard) :
			break

		# Board cell pitch 설정 // Board cell pitch settings
		f64BoardCellPitch = 15
		f64PixelAccuracy = [0]

		if not CalculatePixelAccuracy(orthogonalCalibrator, f64BoardCellPitch, f64PixelAccuracy) :
			break

		# 측정 이미지 로드 // Load the measurement image
		if(res := fliDistortedMeasurementImage.Load('C:\\Users\\Public\\Documents\\FLImaging\\ExampleImages\\Measurement\\Measurement.flif')).IsFail() :		
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		if not Undistortion(orthogonalCalibrator, fliDistortedMeasurementImage, fliUndistortedMeasurementImage):
			break

		# Rectangle Gauge 클래스 선언 // Declare Rectangle Gauge class instance.
		rectangleGauge = CRectangleGauge()

		# Source 이미지 설정 // Set Source image			
		rectangleGauge.SetSourceImage(fliUndistortedMeasurementImage)

		# 측정할 영역을 설정합니다. // Set the area to measure.
		flrMeasureRegion = CFLRect[Double](1095.69367959050714, 1337.99846331160370, 1970.73350513123319, 1924.77041713468020, -8.06731650598383)
		rectangleGauge.SetMeasurementRegion(flrMeasureRegion, 20.000000)

		# 알고리즘 수행 // Execute the algorithm
		if(res := rectangleGauge.Execute()).IsFail() :		
			ErrorPrint(res, 'Failed to execute Rectangle gauge.')
			break
		

		# 실행 결과를 가져옵니다. // Get the execution result.
		flrResult = CFLRect[Double]()
		res, flrResult = rectangleGauge.GetMeasuredObject(flrResult, 0)

		flpLeftTop = CFLPoint[Double](flrResult.left, flrResult.top)
		flpRightTop = CFLPoint[Double](flrResult.right, flrResult.top)
		flpLeftBottom = CFLPoint[Double](flrResult.left, flrResult.bottom)
		flpRightBottom = CFLPoint[Double](flrResult.right, flrResult.bottom)

		fliTop = CFLLine[Double](flpLeftTop, flpRightTop)
		fliRight = CFLLine[Double](flpRightTop, flpRightBottom)
		fliBottom = CFLLine[Double](flpLeftBottom, flpRightBottom)
		fliLeft = CFLLine[Double](flpLeftTop, flpLeftBottom)

		# 측정된 사각형의 실제 길이를 계산합니다. // Calculate the actual length of the measured rectangle.
		f64LeftLength = fliLeft.GetLength() * f64PixelAccuracy[0]
		f64TopLength = fliTop.GetLength() * f64PixelAccuracy[0]
		f64RightLength = fliRight.GetLength() * f64PixelAccuracy[0]
		f64BottomLength = fliBottom.GetLength() * f64PixelAccuracy[0]

		# 이미지 뷰 정보 표시 // Display image view information		
		layerDistortionChessBoard = viewImageDistortionChessBoard.GetLayer(0)
		layerUndistortionChessBoard = viewImageUndistortionChessBoard.GetLayer(0)
		layerDistortionMeasurement = viewImageDistortionMeasurement.GetLayer(0)
		layerUndistortionMeasurement = viewImageUndistortionMeasurement.GetLayer(0)
		flpPoint = CFLPoint[Double](0, 0)
				
		if(res := layerDistortionChessBoard.DrawTextImage(flpPoint, 'Distortion ChessBoard', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerUndistortionChessBoard.DrawTextImage(flpPoint, String.Format('Undistortion ChessBoard \nBoard Cell Pitch : {0} \nPixel Accuracy : {1}', f64BoardCellPitch, f64PixelAccuracy[0]), EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerDistortionMeasurement.DrawTextImage(flpPoint, 'Distortion Measurement', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerUndistortionMeasurement.DrawTextImage(flpPoint, 'Undistortion & Measurement Result', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerUndistortionMeasurement.DrawTextImage(fliLeft.GetCenter(), String.Format('{0} (mm)', f64LeftLength), EColor.YELLOW, EColor.BLACK, 12)).IsFail() or \
			(res := layerUndistortionMeasurement.DrawTextImage(fliTop.GetCenter(), String.Format('{0} (mm)', f64TopLength), EColor.YELLOW, EColor.BLACK, 12)).IsFail() or \
			(res := layerUndistortionMeasurement.DrawTextImage(fliRight.GetCenter(), String.Format('{0} (mm)', f64RightLength), EColor.YELLOW, EColor.BLACK, 12)).IsFail() or \
			(res := layerUndistortionMeasurement.DrawTextImage(fliBottom.GetCenter(), String.Format('{0} (mm)', f64BottomLength), EColor.YELLOW, EColor.BLACK, 12)).IsFail() or \
			(res := layerUndistortionMeasurement.DrawFigureImage(flrResult, EColor.CYAN, 5)).IsFail() :
			ErrorPrint(res, 'Failed to draw text\n')
			break
		

		# 이미지 뷰를 갱신 합니다.
		viewImageDistortionChessBoard.Invalidate(True)
		viewImageDistortionMeasurement.Invalidate(True)
		viewImageUndistortionChessBoard.Invalidate(True)
		viewImageUndistortionMeasurement.Invalidate(True)

		viewImageDistortionChessBoard.ZoomFit()
		viewImageDistortionMeasurement.ZoomFit()
		viewImageUndistortionChessBoard.ZoomFit()
		viewImageUndistortionMeasurement.ZoomFit()

		# 이미지 뷰가 꺼지면 종료로 간주
		while viewImageDistortionChessBoard.IsAvailable() and viewImageUndistortionChessBoard.IsAvailable() and viewImageDistortionMeasurement.IsAvailable() and viewImageUndistortionMeasurement.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()')

def Calibration(orthogonalCalibrator, fliBoardImage):
	bResult = False
	
	while(True):	
		# Learn 이미지 설정 // Learn image settings
		if(res := orthogonalCalibrator.SetCalibrationImage(fliBoardImage))[0].IsFail() :	
			ErrorPrint(res, 'Failed to set image')
			break

		# 직교 보정 계산을 할 Learn 이미지 설정 // Learn image settings for orthogonal correction
		if(res := orthogonalCalibrator.SetOrthogonalCorrectionImage(fliBoardImage))[0].IsFail() :	
			ErrorPrint(res, 'Failed to set image\n')
			break
	

		# Calibator할 대상 종류를 설정합니다. // Set the target type for Calibator.
		orthogonalCalibrator.SetGridType(CCameraCalibrator.EGridType.ChessBoard)
		# 결과에 대한 학습률을 설정합니다. // Set the learning rate for the result.
		orthogonalCalibrator.SetOptimalSolutionAccuracy(1e-5)

		# Calibration 실행 // Execute Calibration
		if(res := orthogonalCalibrator.Calibrate()).IsFail() :
			ErrorPrint(res, 'Calibration failed\n')
			break

		bResult = True
		break

	return bResult


def Undistortion(orthogonalCalibrator, fliSourceImage, fliDestinationImage):
	bResult = False
	
	while True:	
		# Source 이미지 설정 // Set Source image
		orthogonalCalibrator.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set destination image
		orthogonalCalibrator.SetDestinationImage(fliDestinationImage)

		# Interpolation 알고리즘 설정 // Set the Interpolation Algorithm
		if(res := orthogonalCalibrator.SetInterpolationMethod(EInterpolationMethod.Bilinear)).IsFail() :		
			ErrorPrint(res, 'Failed to set interpolation method\n')
			break
		

		# Undistortion 실행 // Execute Undistortion
		if(res := orthogonalCalibrator.Execute()).IsFail() :
		
			ErrorPrint(res, 'Undistortion failed\n')
			break
		

		bResult = True
	
		break

	return bResult


def CalculatePixelAccuracy(orthogonalCalibrator, f64BoardCellPitch, f64PixelAccuracy):

	bResult = False

	while True:	
		gridResult = COrthogonalCalibrator.CCalibratorGridResult()

		res, gridResult = orthogonalCalibrator.GetResultGridPoints(orthogonalCalibrator.GetSourceImage().GetSelectedPageIndex(), 0, gridResult)
				
		if gridResult.flfaGridData.GetCount() > 0 :
		
			flfaGrid = gridResult.flfaGridData.GetAt(0)

			flp1 = CFLPoint[Double]()
			flp2 = CFLPoint[Double]()
			orthogonalCalibrator.ConvertCoordinate(flfaGrid.Front(), flp1)
			orthogonalCalibrator.ConvertCoordinate(flfaGrid.Back(), flp2)

			fliLine2 = CFLLine[Double](flp1, flp2)

			pFliDst = orthogonalCalibrator.GetDestinationImage()

			pFliDst.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(fliLine2))
			f64PixelAccuracy[0] = f64BoardCellPitch / (fliLine2.GetLength() / (flfaGrid.GetCount() - 1.0))
			bResult = True		
		else :
			bResult = False
	
		break

	return bResult


if __name__ == '__main__':
    main()