# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


class CGridDisplay:
	def __init__(self, i64ImageIdx, gridData):
		self.i64ImageIdx = i64ImageIdx
		self.gridData = gridData

def DrawGridPoints(sGridDisplay, layer):

	res = CResult(EResult.UnknownError)

	while True:

		if sGridDisplay.gridResult.flaGridData.Count == 0:
			res = CResult(EResult.NoData)
			break
		
		# 그리기 색상 설정 # Set drawing color
		u32ArrColor = [ EColor.RED, EColor.LIME, EColor.CYAN ]
		i64GridRow = sGridDisplay.gridResult.i64Rows
		i64GridCol = sGridDisplay.gridResult.i64Columns
		f64AvgDistance = sGridDisplay.gridResult.f64AvgDistance
		flqBoardRegion = sGridDisplay.gridResult.pFlqBoardRegion
		f64Angle = flqBoardRegion.flpPoints[0].GetAngle(flqBoardRegion.flpPoints[1])
		f64Width = flqBoardRegion.flpPoints[0].GetDistance(flqBoardRegion.flpPoints[1])

		# Grid 그리기 # Draw grid
		for i64Row in range(i64GridRow):
			for i64Col in range(i64GridCol - 1):
				i64GridIdx = i64Row * i64GridCol + i64Col

				flpGridPoint1 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][i64Col])
				flpGridPoint2 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][i64Col + 1])
				fllDrawLine = CFLLine[Double](flpGridPoint1, flpGridPoint2)
				layer.DrawFigureImage(fllDrawLine, EColor.BLACK, 5)
				layer.DrawFigureImage(fllDrawLine, u32ArrColor[i64GridIdx % 3], 3)
			
			if i64Row < i64GridRow - 1:
				flpGridPoint1 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][i64GridCol - 1])
				flpGridPoint2 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row + 1][0])
				fllDrawLine = CFLLine[Double](flpGridPoint1, flpGridPoint2)
				layer.DrawFigureImage(fllDrawLine, EColor.BLACK, 5)
				layer.DrawFigureImage(fllDrawLine, EColor.YELLOW, 3)
					
		u32ColorText = EColor.YELLOW
		f64PointDist = 0
		f64Dx = 0
		f64Dy = 0

		# Grid Point 인덱싱 # Index Grid Point
		for i64Row in range(i64GridRow):
			flpGridPoint1 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][0])
			flpGridPoint2 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][1])
			f64TempAngle = flpGridPoint1.GetAngle(flpGridPoint2)

			for i64Col in range(i64GridCol):
				i64GridIdx = i64Row * i64GridCol + i64Col

				if i64Col < i64GridCol - 1:
					flpGridPoint1 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][i64Col])
					flpGridPoint2 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][i64Col + 1])

					f64Dx = flpGridPoint2.x - flpGridPoint1.x
					f64Dy = flpGridPoint2.y - flpGridPoint1.y
					f64PointDist = Math.Sqrt(f64Dx * f64Dx + f64Dy * f64Dy)
				
				if i64Row != 0:
					flpGridPoint1 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row][i64Col])
					flpGridPoint2 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[i64Row - 1][i64Col])

					f64Dx = flpGridPoint2.x - flpGridPoint1.x
					f64Dy = flpGridPoint2.y - flpGridPoint1.y
					f64PointDist = Math.Min(f64PointDist, Math.Sqrt(f64Dx * f64Dx + f64Dy * f64Dy))
				else:
					flpGridPoint1 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[0][i64Col])
					flpGridPoint2 = CFLPoint[Double](sGridDisplay.gridResult.flaGridData[1][i64Col])

					f64Dx = flpGridPoint2.x - flpGridPoint1.x
					f64Dy = flpGridPoint2.y - flpGridPoint1.y
					f64PointDist = Math.Min(f64PointDist, Math.Sqrt(f64Dx * f64Dx + f64Dy * f64Dy))
				
				strGridIdx = "{0}".format(i64GridIdx)
				u32ColorText = u32ArrColor[i64GridIdx % 3]
				if i64Col == i64GridCol - 1:
					u32ColorText = EColor.YELLOW

				layer.DrawTextImage(flpGridPoint1, strGridIdx, u32ColorText, EColor.BLACK, (int)(f64PointDist / 2), True, f64TempAngle)
					
		# Board Region 그리기 # Draw Board Region
		stringData = "({0} X {1})".format(i64GridCol, i64GridRow)
		layer.DrawFigureImage(flqBoardRegion, EColor.BLACK, 3)
		layer.DrawFigureImage(flqBoardRegion, EColor.YELLOW, 1)
		layer.DrawTextImage(flqBoardRegion.flpPoints[0], stringData, EColor.YELLOW, EColor.BLACK, (int)(f64Width / 16), True, f64Angle, EGUIViewImageTextAlignment.LEFT_BOTTOM, None, 1, 1, EGUIViewImageFontWeight.EXTRABOLD)

		res = CResult(EResult.OK)

		break

	return res

class CMessageReceiver(CFLBase):

	# CMessageReceiver 생성자 # CMessageReceiver constructor
	def __init__(self, viewImage):
		super().__init__()

		self.m_viewImage = viewImage

		self.m_vctGridDisplay = [CGridDisplay(0, CStereoCalibrator3D.CGridResult())]

		# 메세지를 전달 받기 위해 CBroadcastManager 에 구독 등록 # Subscribe to CBroadcast Manager to receive messages
		CBroadcastManager.Subscribe(self, CBroadcastManager.Delegate_OnReceiveBroadcast(self.OnReceiveBroadcast))
		
	def __del__(self):

		# CMessageReceiver 소멸자 # CMessageReceiver destructor
		# 메시지를 그만 받도록 객체가 소멸시 Unsubscribe 실행 # Unsubscribe to stop receiving messages when the object is deleted
		CBroadcastManager.Unsubscribe(self)
	
	def SetGrid(self, sGridDisplay):

		self.m_vctGridDisplay = sGridDisplay

	# 메세지가 들어오면 호출되는 함수 OnReceiveBroadcast 오버라이드하여 구현 # Implemented by overriding the function OnReceive Broadcast that is invoked when a message is received
	def OnReceiveBroadcast(self, message):

		while(True):

			# message 가 null 인지 확인 # Verify message is null
			if message is None:
				break

			# GetCaller() 가 등록한 이미지뷰인지 확인 # Verify that GetCaller() is a registered image view
			if message.GetCaller() != self.m_viewImage:
				break

			# 메세지의 채널을 확인 # Check the channel of the message
			if message.GetChannel() == int(EGUIBroadcast.ViewImage_PostPageChange):

				# 메세지를 호출한 객체를 CGUIViewImage 로 캐스팅 # Casting the object that called the message as CGUIViewImage
				viewImage = message.GetCaller()

				# viewImage 가 null 인지 확인 # Verify viewImage is null
				if viewImage is None:
					break

				fliTmp = viewImage.GetImage()

				if fliTmp is None:
					break

				i64CurPage = fliTmp.GetSelectedPageIndex()

				# 이미지뷰의 0번 레이어 가져오기 # Get layer 0th of image view
				layer = viewImage.GetLayer(i64CurPage % 10)

				for i in range(10):
					viewImage.GetLayer(i).Clear()

				for i64Idx in range(fliTmp.GetPageCount()):
					if self.m_vctGridDisplay[i64Idx].i64ImageIdx == i64CurPage:
						DrawGridPoints(self.m_vctGridDisplay[i64Idx], layer)

				# 이미지뷰를 갱신 # Update the image view.
				viewImage.Invalidate(True)

			break

def Calibration(stereoCalibrator3D, fliLearnImage, fliLearn2Image):

	# 수행 결과 객체 선언 # Declare execution result object
	res = CResult(EResult.UnknownError)

	while True:

		# Learn 이미지 설정 # Set Learn image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := stereoCalibrator3D.SetLearnImage(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set Learn image.\n")
			break
		
		# Learn 2 이미지 설정 # Set Learn 2 image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := stereoCalibrator3D.SetLearnImage2(fliLearn2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to set Learn 2 image.\n")
			break
		
		# Calibration의 최적해 정확도 값 설정 # Set optimal solution accuracy of calibration
		if (res := stereoCalibrator3D.SetOptimalSolutionAccuracy(1e-5)).IsFail():
			ErrorPrint(res, "Failed to set calibration optimal solution accuracy.\n")
			break
		
		# Calibration에 사용되는 Grid Type 설정 # Set grid type used in calibration
		if (res := stereoCalibrator3D.SetGridType(CStereoCalibrator3D.EGridType.ChessBoard)).IsFail():
			ErrorPrint(res, "Failed to set calibration grid type.\n")
			break
		
		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibration algorithm according to previously set parameters
		if (res := stereoCalibrator3D.Calibrate()).IsFail():
			ErrorPrint(res, "Failed to calibrate Stereo Calibrator 3D.\n")
			break

		break

	return res

def Undistortion(stereoCalibrator3D, fliSourceImage, fliSource2Image, fliDestinationImage, fliDestination2Image):

	# 수행 결과 객체 선언 # Declare execution result object
	res = CResult(EResult.UnknownError)

	while True:

		# Source 이미지 설정 # Set Source image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := stereoCalibrator3D.SetSourceImage(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set Source image.\n")
			break
		
		# Source 이미지 2 설정 # Set Source 2 image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := stereoCalibrator3D.SetSourceImage2(fliSource2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to set Source 2 image.\n")
			break
		
		# Destination 이미지 설정 # Set Destination image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := stereoCalibrator3D.SetDestinationImage(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set Destination image.\n")
			break
		
		# Destination 이미지 2 설정 # Set Destination 2 image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := stereoCalibrator3D.SetDestinationImage2(fliDestination2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to set Destination 2 image.\n")
			break
		
		# Interpolation 메소드 설정 # Set interpolation method
		if (res := stereoCalibrator3D.SetInterpolationMethod(EInterpolationMethod.Bilinear)).IsFail():
			ErrorPrint(res, "Failed to set interpolation method.\n")
			break
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := stereoCalibrator3D.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute Stereo Calibrator 3D.\n")
			break
		
		break

	return res

# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare image object
	fliLearnImage = CFLImage()
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()
	fliLearn2Image = CFLImage()
	fliSource2Image = CFLImage()
	fliDestination2Image = CFLImage()

	# 이미지 뷰 선언 # Declare image view
	viewLearnImage = CGUIViewImage()
	viewDestinationImage = CGUIViewImage()
	viewLearn2Image = CGUIViewImage()
	viewDestination2Image = CGUIViewImage()

	# 수행 결과 객체 선언 # Declare execution result object
	res = CResult(EResult.UnknownError)

	while True:

		# Learn 이미지 로드 # Load Learn image
		if (res := fliLearnImage.Load("../../ExampleImages/StereoCalibrator3D/Left.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		
		# Learn2 이미지 로드 # Load Learn2 image
		if (res := fliLearn2Image.Load("../../ExampleImages/StereoCalibrator3D/Right.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		
		# Learn 이미지 뷰 생성 # Create Learn image view
		if (res := viewLearnImage.Create(300, 0, 300 + 480 * 1, 360)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# Learn 2 이미지 뷰 생성 # Create Learn 2 image view
		if (res := viewLearn2Image.Create(300 + 480, 0, 300 + 480 * 2, 360)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# Destination 이미지 뷰 생성 # Create Destination image view
		if (res := viewDestinationImage.Create(300, 360, 780, 720)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# Destination 2 이미지 뷰 생성 # Create Destination 2 image view
		if (res := viewDestination2Image.Create(780, 360, 1260, 720)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# Learn 이미지 뷰에 이미지를 디스플레이 # Display image in Learn image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SetImagePtr(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# Learn 2 이미지 뷰에 이미지를 디스플레이 # Display image in Learn 2 image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearn2Image.SetImagePtr(fliLearn2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# Destination 이미지 뷰에 이미지를 디스플레이 # Display image in Destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewDestinationImage.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# Destination 2 이미지 뷰에 이미지를 디스플레이 # Display image in Destination 2 image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewDestination2Image.SetImagePtr(fliDestination2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SynchronizeWindow(viewLearn2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window between views.\n")
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SynchronizeWindow(viewDestinationImage)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window between views.\n")
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SynchronizeWindow(viewDestination2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window between views.\n")
			break
		
		# 두 이미지 뷰 윈도우의 Page를 동기화 한다 # Synchronize pages of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SynchronizePageIndex(viewLearn2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize page index between image views.\n")
			break
		
		# 두 이미지 뷰 윈도우의 Page를 동기화 한다 # Synchronize pages of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SynchronizePageIndex(viewDestinationImage)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize page index between image views.\n")
			break
		
		# 두 이미지 뷰 윈도우의 Page를 동기화 한다 # Synchronize pages of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewLearnImage.SynchronizePageIndex(viewDestination2Image)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize page index between image views.\n")
			break
		
		Console.WriteLine("Processing.....\n")

		# Stereo Calibrator 3D 객체 생성 # Create Stereo Calibrator 3D object
		stereoCalibrator3D = CStereoCalibrator3D()

		# Stereo Calibrator 3D Calibration 수행 # Calibrate Stereo Calibrator 3D
		if Calibration(stereoCalibrator3D, fliLearnImage, fliLearn2Image).IsFail():
			break

		# Source 이미지를 Learn 이미지와 동일하도록 설정 (얕은 복사) # Assign Learn image to Source image (Shallow Copy)
		if (res := fliSourceImage.Assign(fliLearnImage, False)).IsFail():
			ErrorPrint(res, "Failed to assign the image.\n")
			break
		
		# Source 2 이미지를 Learn 2 이미지와 동일하도록 설정 (얕은 복사) # Assign Learn 2 image to Source 2 image (Shallow Copy)
		if (res := fliSource2Image.Assign(fliLearn2Image, False)).IsFail():
			ErrorPrint(res, "Failed to assign the image.\n")
			break
		
		# Stereo Calibrator 3D Undistortion 수행 # Undistort Stereo Calibrator 3D
		if Undistortion(stereoCalibrator3D, fliSourceImage, fliSource2Image, fliDestinationImage, fliDestination2Image).IsFail():
			break

		# 뷰에 격자 탐지 결과 출력 # Display grid detection result in view
		arrGridDisplay = [CGridDisplay(0, CStereoCalibrator3D.CGridResult()) for i in range(5)]

		for i64ImgIdx in range(fliLearnImage.GetPageCount()):
			arrGridDisplay[i64ImgIdx].gridResult = CStereoCalibrator3D.CGridResult()
			stereoCalibrator3D.GetResultGridPoints(arrGridDisplay[i64ImgIdx].gridResult, i64ImgIdx)
			arrGridDisplay[i64ImgIdx].i64ImageIdx = i64ImgIdx

		arrGridDisplay2 = [CGridDisplay(0, CStereoCalibrator3D.CGridResult()) for i in range(5)]

		for i64ImgIdx in range(fliLearn2Image.GetPageCount()):
			arrGridDisplay2[i64ImgIdx].gridResult = CStereoCalibrator3D.CGridResult()
			stereoCalibrator3D.GetResultGridPoints2(arrGridDisplay2[i64ImgIdx].gridResult, i64ImgIdx)
			arrGridDisplay2[i64ImgIdx].i64ImageIdx = i64ImgIdx
		
		# Message Receiver 객체 생성 # Create Message Receiver object
		msgReceiver = CMessageReceiver(viewLearnImage)
		msgReceiver2 = CMessageReceiver(viewLearn2Image)

		msgReceiver.m_vctGridDisplay = arrGridDisplay
		msgReceiver2.m_vctGridDisplay = arrGridDisplay2

		# 화면에 출력하기 위해 이미지 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released
		layerLearn = viewLearnImage.GetLayer(0)
		layerLearn2 = viewLearn2Image.GetLayer(0)
		layerDestination = viewDestinationImage.GetLayer(0)
		layerDestination2 = viewDestination2Image.GetLayer(0)

		# Chess Board Grid 출력 # Display chess board grid
		DrawGridPoints(arrGridDisplay[0], layerLearn)
		DrawGridPoints(arrGridDisplay2[0], layerLearn2)

		# Calibration data 출력 # Display calibration data
		intrinsicOptimizedParam = stereoCalibrator3D.GetResultCalibratedIntrinsicParameters();
		intrinsicOptimizedParam2 = stereoCalibrator3D.GetResultCalibratedIntrinsicParameters2();

		distortOptimizedCoeef = stereoCalibrator3D.GetResultCalibratedDistortionCoefficients();
		distortOptimizedCoeef2 = stereoCalibrator3D.GetResultCalibratedDistortionCoefficients2();

		rotationOptimizedParam = stereoCalibrator3D.GetResultCalibratedRotationParameters();

		translationOptimizedParam = stereoCalibrator3D.GetResultCalibratedTranslationParameters();


		intrinsicRectifiedParam = stereoCalibrator3D.GetResultRectifiedIntrinsicParameters();
		intrinsicRectifiedParam2 = stereoCalibrator3D.GetResultRectifiedIntrinsicParameters2();

		rotationRectifiedParam = stereoCalibrator3D.GetResultRectifiedRotationParameters();
		rotationRectifiedParam2 = stereoCalibrator3D.GetResultRectifiedRotationParameters2();

		translationRectifiedParam = stereoCalibrator3D.GetResultRectifiedTranslationParameters();
		translationRectifiedParam2 = stereoCalibrator3D.GetResultRectifiedTranslationParameters2();

		f64ReprojError = stereoCalibrator3D.GetResultReProjectionError();

		strFocalLengthX = "";
		strFocalLengthY = "";
		strPrincipalPointX = "";
		strPrincipalPointY = "";
		strDistortionK1 = "";
		strDistortionK2 = "";
		strDistortionP1 = "";
		strDistortionP2 = "";
		strDistortionK3 = "";
		strRotation0 = "";
		strRotation1 = "";
		strRotation2 = "";
		strTranslationX = "";
		strTranslationY = "";
		strTranslationZ = "";


		print("\n\n", end='');

		print("**************************** Calibration ****************************", end='');

		print("\n\n\n", end='');

		print("---------------------------- Camera 0 ----------------------------", end='');

		print("\n\n", end='');

		strFocalLengthX = "{0:.13f}".format(intrinsicOptimizedParam.f64FocalLengthX)
		strFocalLengthY = "{0:.13f}".format(intrinsicOptimizedParam.f64FocalLengthY)
		strPrincipalPointX = "{0:.13f}".format(intrinsicOptimizedParam.f64PrincipalPointX)
		strPrincipalPointY = "{0:.13f}".format(intrinsicOptimizedParam.f64PrincipalPointY)

		print("Calibrated Intrinsic Parameters:\n", end='');
		print("\tFocal Length X: " + strFocalLengthX + "\n", end='');
		print("\tFocal Length Y: " + strFocalLengthY + "\n", end='');
		print("\tPrincipal Point X: " + strPrincipalPointX + "\n", end='');
		print("\tPrincipal Point Y: " + strPrincipalPointY + "\n", end='');

		print("\n", end='');

		strDistortionK1 = "{0:.13f}".format(distortOptimizedCoeef.f64K1)
		strDistortionK2 = "{0:.13f}".format(distortOptimizedCoeef.f64K2)
		strDistortionP1 = "{0:.13f}".format(distortOptimizedCoeef.f64P1)
		strDistortionP2 = "{0:.13f}".format(distortOptimizedCoeef.f64P2)
		strDistortionK3 = "{0:.13f}".format(distortOptimizedCoeef.f64K3)

		print("Calibrated Distortion Coefficients:\n", end='');
		print("\tK1: " + strDistortionK1 + "\n", end='');
		print("\tK2: " + strDistortionK2 + "\n", end='');
		print("\tP1: " + strDistortionP1 + "\n", end='');
		print("\tP2: " + strDistortionP2 + "\n", end='');
		print("\tK3: " + strDistortionK3 + "\n", end='');

		print("\n", end='');


		print("---------------------------- Camera 1 ----------------------------", end='');

		print("\n\n", end='');

		strFocalLengthX = "{0:.13f}".format(intrinsicOptimizedParam2.f64FocalLengthX)
		strFocalLengthY = "{0:.13f}".format(intrinsicOptimizedParam2.f64FocalLengthY)
		strPrincipalPointX = "{0:.13f}".format(intrinsicOptimizedParam2.f64PrincipalPointX)
		strPrincipalPointY = "{0:.13f}".format(intrinsicOptimizedParam2.f64PrincipalPointY)

		print("Calibrated Intrinsic Parameters:\n", end='');
		print("\tFocal Length X: " + strFocalLengthX + "\n", end='');
		print("\tFocal Length Y: " + strFocalLengthY + "\n", end='');
		print("\tPrincipal Point X: " + strPrincipalPointX + "\n", end='');
		print("\tPrincipal Point Y: " + strPrincipalPointY + "\n", end='');

		print("\n", end='');

		strDistortionK1 = "{0:.13f}".format(distortOptimizedCoeef2.f64K1)
		strDistortionK2 = "{0:.13f}".format(distortOptimizedCoeef2.f64K2)
		strDistortionP1 = "{0:.13f}".format(distortOptimizedCoeef2.f64P1)
		strDistortionP2 = "{0:.13f}".format(distortOptimizedCoeef2.f64P2)
		strDistortionK3 = "{0:.13f}".format(distortOptimizedCoeef2.f64K3)

		print("Calibrated Distortion Coefficients:\n", end='');
		print("\tK1: " + strDistortionK1 + "\n", end='');
		print("\tK2: " + strDistortionK2 + "\n", end='');
		print("\tP1: " + strDistortionP1 + "\n", end='');
		print("\tP2: " + strDistortionP2 + "\n", end='');
		print("\tK3: " + strDistortionK3 + "\n", end='');

		print("\n", end='');


		print("---------------------------- Common ----------------------------", end='');

		print("\n\n", end='');

		strRotation0 = "{0:.13f}, ".format(rotationOptimizedParam.f64R0)
		strRotation0 += "{0:.13f}, ".format(rotationOptimizedParam.f64R1)
		strRotation0 += "{0:.13f}".format(rotationOptimizedParam.f64R2)
		strRotation1 = "{0:.13f}, ".format(rotationOptimizedParam.f64R3)
		strRotation1 += "{0:.13f}, ".format(rotationOptimizedParam.f64R4)
		strRotation1 += "{0:.13f}".format(rotationOptimizedParam.f64R5)
		strRotation2 = "{0:.13f}, ".format(rotationOptimizedParam.f64R6)
		strRotation2 += "{0:.13f}, ".format(rotationOptimizedParam.f64R7)
		strRotation2 += "{0:.13f}".format(rotationOptimizedParam.f64R8)

		print("Relative Rotation Parameters:\n", end='');
		print("\t" + strRotation0 + "\n", end='');
		print("\t" + strRotation1 + "\n", end='');
		print("\t" + strRotation2 + "\n", end='');

		print("\n", end='');

		strTranslationX = "{0:.13f}".format(translationOptimizedParam.f64X)
		strTranslationY = "{0:.13f}".format(translationOptimizedParam.f64Y)
		strTranslationZ = "{0:.13f}".format(translationOptimizedParam.f64Z)

		print("Relative Translation Parameters:\n", end='');
		print("\tX: " + strTranslationX + "\n", end='');
		print("\tY: " + strTranslationY + "\n", end='');
		print("\tZ: " + strTranslationZ + "\n", end='');

		print("\n\n", end='');


		print("**************************** Rectification ****************************", end='');

		print("\n\n\n", end='');

		print("---------------------------- Camera 0 ----------------------------", end='');

		print("\n\n", end='');

		strFocalLengthX = "{0:.13f}".format(intrinsicRectifiedParam.f64FocalLengthX)
		strFocalLengthY = "{0:.13f}".format(intrinsicRectifiedParam.f64FocalLengthY)
		strPrincipalPointX = "{0:.13f}".format(intrinsicRectifiedParam.f64PrincipalPointX)
		strPrincipalPointY = "{0:.13f}".format(intrinsicRectifiedParam.f64PrincipalPointY)

		print("Rectified Intrinsic Parameters:\n", end='');
		print("\tFocal Length X: " + strFocalLengthX + "\n", end='');
		print("\tFocal Length Y: " + strFocalLengthY + "\n", end='');
		print("\tPrincipal Point X: " + strPrincipalPointX + "\n", end='');
		print("\tPrincipal Point Y: " + strPrincipalPointY + "\n", end='');

		print("\n", end='');

		strRotation0 = "{0:.13f}, ".format(rotationRectifiedParam.f64R0)
		strRotation0 += "{0:.13f}, ".format(rotationRectifiedParam.f64R1)
		strRotation0 += "{0:.13f}".format(rotationRectifiedParam.f64R2)
		strRotation1 = "{0:.13f}, ".format(rotationRectifiedParam.f64R3)
		strRotation1 += "{0:.13f}, ".format(rotationRectifiedParam.f64R4)
		strRotation1 += "{0:.13f}".format(rotationRectifiedParam.f64R5)
		strRotation2 = "{0:.13f}, ".format(rotationRectifiedParam.f64R6)
		strRotation2 += "{0:.13f}, ".format(rotationRectifiedParam.f64R7)
		strRotation2 += "{0:.13f}".format(rotationRectifiedParam.f64R8)

		print("Rectified Rotation Parameters:\n", end='');
		print("\t" + strRotation0 + "\n", end='');
		print("\t" + strRotation1 + "\n", end='');
		print("\t" + strRotation2 + "\n", end='');

		print("\n", end='');

		strTranslationX = "{0:.13f}".format(translationRectifiedParam.f64X)
		strTranslationY = "{0:.13f}".format(translationRectifiedParam.f64Y)
		strTranslationZ = "{0:.13f}".format(translationRectifiedParam.f64Z)

		print("Rectified Translation Parameters:\n", end='');
		print("\tX: " + strTranslationX + "\n", end='');
		print("\tY: " + strTranslationY + "\n", end='');
		print("\tZ: " + strTranslationZ + "\n", end='');

		print("\n", end='');


		print("---------------------------- Camera 1 ----------------------------", end='');

		print("\n\n", end='');

		strFocalLengthX = "{0:.13f}".format(intrinsicRectifiedParam2.f64FocalLengthX)
		strFocalLengthY = "{0:.13f}".format(intrinsicRectifiedParam2.f64FocalLengthY)
		strPrincipalPointX = "{0:.13f}".format(intrinsicRectifiedParam2.f64PrincipalPointX)
		strPrincipalPointY = "{0:.13f}".format(intrinsicRectifiedParam2.f64PrincipalPointY)

		print("Rectified Intrinsic Parameters:\n", end='');
		print("\tFocal Length X: " + strFocalLengthX + "\n", end='');
		print("\tFocal Length Y: " + strFocalLengthY + "\n", end='');
		print("\tPrincipal Point X: " + strPrincipalPointX + "\n", end='');
		print("\tPrincipal Point Y: " + strPrincipalPointY + "\n", end='');

		print("\n", end='');

		strRotation0 = "{0:.13f}, ".format(rotationRectifiedParam2.f64R0)
		strRotation0 += "{0:.13f}, ".format(rotationRectifiedParam2.f64R1)
		strRotation0 += "{0:.13f}".format(rotationRectifiedParam2.f64R2)
		strRotation1 = "{0:.13f}, ".format(rotationRectifiedParam2.f64R3)
		strRotation1 += "{0:.13f}, ".format(rotationRectifiedParam2.f64R4)
		strRotation1 += "{0:.13f}".format(rotationRectifiedParam2.f64R5)
		strRotation2 = "{0:.13f}, ".format(rotationRectifiedParam2.f64R6)
		strRotation2 += "{0:.13f}, ".format(rotationRectifiedParam2.f64R7)
		strRotation2 += "{0:.13f}".format(rotationRectifiedParam2.f64R8)

		print("Rectified Rotation Parameters:\n", end='');
		print("\t" + strRotation0 + "\n", end='');
		print("\t" + strRotation1 + "\n", end='');
		print("\t" + strRotation2 + "\n", end='');

		print("\n", end='');

		strTranslationX = "{0:.13f}".format(translationRectifiedParam2.f64X)
		strTranslationY = "{0:.13f}".format(translationRectifiedParam2.f64Y)
		strTranslationZ = "{0:.13f}".format(translationRectifiedParam2.f64Z)

		print("Rectified Translation Parameters:\n", end='');
		print("\tX: " + strTranslationX + "\n", end='');
		print("\tY: " + strTranslationY + "\n", end='');
		print("\tZ: " + strTranslationZ + "\n", end='');

		print("\n", end='');

		print("Re-Projection Error : {0:.13f}\n".format(f64ReprojError), end='');

		print("\n", end='');

		if (res := layerLearn.DrawTextCanvas(CFLPoint[Double](0, 0), "Learn Image", EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerLearn2.DrawTextCanvas(CFLPoint[Double](0, 0), "Learn 2 Image", EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		if (res := layerDestination.DrawTextCanvas(CFLPoint[Double](0, 0), "Destination Image", EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		if (res := layerDestination2.DrawTextCanvas(CFLPoint[Double](0, 0), "Destination 2 Image", EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		# 새로 생성한 이미지를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created image
		if (res := viewDestinationImage.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit image view.\n")
			break
		
		# 새로 생성한 이미지를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created image
		if (res := viewDestination2Image.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit image view.\n")
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewLearnImage.Invalidate(True)
		viewLearn2Image.Invalidate(True)
		viewDestinationImage.Invalidate(True)
		viewDestination2Image.Invalidate(True)

		# 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until a view is closed before exiting
		while viewLearnImage.IsAvailable() and viewLearn2Image.IsAvailable() and viewDestinationImage.IsAvailable() and viewDestination2Image.IsAvailable():
			CThreadUtilities.Sleep(1)
		
		break
	
	# End of main function


if __name__ == '__main__':
    main()
