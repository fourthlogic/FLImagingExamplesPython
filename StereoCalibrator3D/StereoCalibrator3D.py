# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


class SGridDisplay:
	def __init__(self, i64ImageIdx, sGridData):
		self.i64ImageIdx = i64ImageIdx
		self.sGridData = sGridData

def DrawGridPoints(SGridDisplay, layer):
	bOK = False

	# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
	layer.Clear()

	# 그리기 색상 설정 # Set drawing color
	colorPool = [EColor.RED, EColor.LIME, EColor.CYAN]

	i64GridRow = SGridDisplay.sGridData.i64Rows
	i64GridCol = SGridDisplay.sGridData.i64Columns

	# Grid 그리기 # Draw grid
	for i64Row in range(i64GridRow):
		for i64Col in range(i64GridCol - 1):
			i64GridIdx = i64Row * i64GridCol + i64Col
			flpGridPoint1 = SGridDisplay.sGridData.arrGridData[i64Row][i64Col]
			flpGridPoint2 = SGridDisplay.sGridData.arrGridData[i64Row][i64Col + 1]
			fllDrawLine = CFLLine[Double](flpGridPoint1, flpGridPoint2)

			if (res := layer.DrawFigureImage(fllDrawLine, EColor.BLACK, 5)).IsFail():
				ErrorPrint(res, "Failed to draw figure.\n")
				break
			
			if (res := layer.DrawFigureImage(fllDrawLine, colorPool[i64GridIdx % 3], 3)).IsFail():
				ErrorPrint(res, "Failed to draw figure.\n")
				break

		if i64Row < i64GridRow - 1:
			flpGridPoint1 = SGridDisplay.sGridData.arrGridData[i64Row][i64GridCol - 1]
			flpGridPoint2 = SGridDisplay.sGridData.arrGridData[i64Row + 1][0]
			fllDrawLine = CFLLine[Double]()
			fllDrawLine.Set(flpGridPoint1, flpGridPoint2)
			
			if (res := layer.DrawFigureImage(fllDrawLine, EColor.BLACK, 5)).IsFail():
				ErrorPrint(res, "Failed to draw figure.\n")
				break
			
			if (res := layer.DrawFigureImage(fllDrawLine, EColor.YELLOW, 3)).IsFail():
				ErrorPrint(res, "Failed to draw figure.\n")
				break

	colorText = EColor.YELLOW
	colorPool[2] = EColor.CYAN
	f64PointDist = 0
	f64Dx = 0
	f64Dy = 0

	# Grid Point 인덱싱 # Index Grid Point
	for i64Row in range(i64GridRow):
		tpGridPoint1 = SGridDisplay.sGridData.arrGridData[i64Row][0]
		tpGridPoint2 = SGridDisplay.sGridData.arrGridData[i64Row][1]
		flpGridPoint1 = CFLPoint[Double](tpGridPoint1.x, tpGridPoint1.y)
		flpGridPoint2 = CFLPoint[Double](tpGridPoint2.x, tpGridPoint2.y)

		f64AngleIner = flpGridPoint1.GetAngle(flpGridPoint2)

		for i64Col in range(i64GridCol):
			i64GridIdx = i64Row * i64GridCol + i64Col

			if i64Col < i64GridCol - 1:
				tpGridPoint1 = SGridDisplay.sGridData.arrGridData[i64Row][i64Col]
				tpGridPoint2 = SGridDisplay.sGridData.arrGridData[i64Row][i64Col + 1]

				f64Dx = tpGridPoint2.x - tpGridPoint1.x
				f64Dy = tpGridPoint2.y - tpGridPoint1.y
				f64PointDist = (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5

			if i64Row > 0:
				tpGridPoint1 = SGridDisplay.sGridData.arrGridData[i64Row][i64Col]
				tpGridPoint2 = SGridDisplay.sGridData.arrGridData[i64Row - 1][i64Col]

				f64Dx = tpGridPoint2.x - tpGridPoint1.x
				f64Dy = tpGridPoint2.y - tpGridPoint1.y
				f64PointDist = min(f64PointDist, Math.Sqrt(f64Dx * f64Dx + f64Dy * f64Dy))
			else:
				tpGridPoint1 = SGridDisplay.sGridData.arrGridData[0][i64Col]
				tpGridPoint2 = SGridDisplay.sGridData.arrGridData[1][i64Col]

				f64Dx = tpGridPoint2.x - tpGridPoint1.x
				f64Dy = tpGridPoint2.y - tpGridPoint1.y
				f64PointDist = min(f64PointDist, Math.Sqrt(f64Dx * f64Dx + f64Dy * f64Dy))

			wstrGridIdx = f"{i64GridIdx}"
			colorText = colorPool[i64GridIdx % 3]

			if i64Col == i64GridCol - 1:
				colorText = EColor.YELLOW

			if (res := layer.DrawTextImage(tpGridPoint1, wstrGridIdx, colorText, EColor.BLACK, int(f64PointDist / 2), True, f64AngleIner)).IsFail():
				ErrorPrint(res, "Failed to draw figure.\n")
				break

	# Board Region 그리기 # Draw Board Region
	flqBoardRegion = SGridDisplay.sGridData.pFlqBoardRegion
	flpPoint1 = CFLPoint[Double](flqBoardRegion.flpPoints[0])
	flpPoint2 = CFLPoint[Double](flqBoardRegion.flpPoints[1])
	f64Angle = flpPoint1.GetAngle(flpPoint2)
	wstringData = f"({SGridDisplay.sGridData.i64Columns} X {SGridDisplay.sGridData.i64Rows})"

	if (res := layer.DrawFigureImage(flqBoardRegion, EColor.YELLOW, 3)).IsFail():
		ErrorPrint(res, "Failed to draw figure.\n")

	if (res := layer.DrawTextImage(flpPoint1, wstringData, EColor.YELLOW, EColor.BLACK, 15, False, f64Angle, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
		ErrorPrint(res, "Failed to draw text.\n")

	return bOK

class CMessageReceiver(CFLBase):
	# CMessageReceiver 생성자 # CMessageReceiver constructor
	def __init__(self, viewImage):
		super().__init__()

		self.m_viewImage = viewImage

		self.m_vctGridDisplay = SGridDisplay(0, CStereoCalibrator3D.SGridResult())

		# 메세지를 전달 받기 위해 CBroadcastManager 에 구독 등록 #Subscribe to CBroadcast Manager to receive messages
		CBroadcastManager.Subscribe(self, CBroadcastManager.Delegate_OnReceiveBroadcast(self.OnReceiveBroadcast))
		#CBroadcastManager.Subscribe(self)
		
	def __del__(self):
		# CMessageReceiver destructor
		# Unsubscribe to stop receiving messages when the object is deleted
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
				layer = viewImage.GetLayer(int(i64CurPage % 10))

				for i in range(10):
					viewImage.GetLayer(int(i)).Clear()

				for i64Idx in range(fliTmp.GetPageCount()):
					if self.m_vctGridDisplay[int(i64Idx)].i64ImageIdx == i64CurPage:
						DrawGridPoints(self.m_vctGridDisplay[int(i64Idx)], layer)

				# 이미지뷰를 갱신 # Update the image view.
				viewImage.Invalidate()

			break

def Calibration(sSC, fliLearnImage, fliLearnImage2):
	bResult = False

	while(True):
		# Learn 이미지 설정 # Set learn image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := sSC.SetLearnImage(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image.\n")
			break

		# Learn 이미지 설정 # Set learn image 2
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := sSC.SetLearnImage2(fliLearnImage2)[0]).IsFail():
			ErrorPrint(res, "Failed to set image.\n")
			break

		# Optimal Solution Accuracy 설정 # Set the optical solution accuracy
		if (res := sSC.SetOptimalSolutionAccuracy(1e-5)).IsFail():
			ErrorPrint(res, "Failed to set Optimal Solution Accuracy.\n")
			break

		# Grid Type 설정 # Set the grid type
		if (res := sSC.SetGridType(CStereoCalibrator3D.EGridType.ChessBoard)).IsFail():
			ErrorPrint(res, "Failed to set Grid Type.\n")
			break

		# Calibration 실행 # Execute calibration
		if (res := sSC.Calibrate()).IsFail():
			ErrorPrint(res, "Calibration failed.\n")
			break

		bResult = True

		break

	return bResult

def Undistortion(sSC, fliSourceImage, fliSourceImage2, fliDestinationImage, fliDestinationImage2):
	bResult = False

	while(True):
		# Source 이미지 설정 # Set source image
		if (res := sSC.SetSourceImage(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, "Failed to load image.\n")
			break

		# Source 이미지 2 설정 # Set source image 2
		if (res := sSC.SetSourceImage2(fliSourceImage2)[0]).IsFail():
			ErrorPrint(res, "Failed to load image.\n")
			break

		# Destination 이미지 설정 # Set the destination image
		if (res := sSC.SetDestinationImage(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, "Failed to load image.\n")
			break

		# Destination 이미지 2 설정 # Set destination image 2
		if(res := sSC.SetDestinationImage2(fliDestinationImage2)[0]).IsFail():
			ErrorPrint(res, "Failed to load image.\n")
			break

		# Interpolation 알고리즘 설정 # Set interpolation algorithm
		if(res := sSC.SetInterpolationMethod(EInterpolationMethod.Bilinear)).IsFail():
			ErrorPrint(res, "Failed to set interpolation method.\n")
			break

		# Undistortion 실행 # Execute undistortion
		if (res := sSC.Execute()).IsFail():
			ErrorPrint(res, "Undistortion failed.\n")
			break

		bResult = True

		break

	return bResult

# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliLearnImage = CFLImage()
	fliLearnImage2 = CFLImage()
	fliSourceImage = CFLImage()
	fliSourceImage2 = CFLImage()
	fliDestinationImage = CFLImage()
	fliDestinationImage2 = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageLearn2 = CGUIViewImage()
	viewImageDestination = CGUIViewImage()
	viewImageDestination2 = CGUIViewImage()
	
	# Stereo Calibrator 3D 객체 생성 # Create Stereo Calibrator 3D object
	stereoCalibrator = CStereoCalibrator3D()
	
	# MessageReceiver 객체 생성 # Create MessageReceiver object
	msgReceiver = CMessageReceiver(viewImageLearn)
	msgReceiver2 = CMessageReceiver(viewImageLearn2)

	while True:
		
		# Learn 이미지 로드 # Load the learn image
		if (res := fliLearnImage.Load('C:/Users/junhy/source/repos/fourthlogic/ExampleImages/StereoCalibrator3D/Left.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Learn 2 이미지 로드 # Load the learn 2 image
		if (res := fliLearnImage2.Load('C:/Users/junhy/source/repos/fourthlogic/ExampleImages/StereoCalibrator3D/Right.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Page 0 선택 # Select page 0
		fliLearnImage.SelectPage(0)
		fliLearnImage2.SelectPage(0)
		
		print("Processing....")

		if not Calibration(stereoCalibrator, fliLearnImage, fliLearnImage2):
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliSourceImage.Assign(fliLearnImage, False)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliSourceImage2.Assign(fliLearnImage2, False)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		mvBlank = CMultiVar[int](0)

		# Destination 이미지 생성 # Create destination image
		if (res := fliDestinationImage.Create(fliSourceImage.GetWidth(), fliSourceImage.GetHeight(), mvBlank, fliSourceImage.GetPixelFormat())).IsFail():
			ErrorPrint(res, "Failed to create the image file.\n")
			break

		# Destination 2 이미지 생성 # Create destination 2 image
		if (res := fliDestinationImage2.Create(fliSourceImage.GetWidth(), fliSourceImage.GetHeight(), mvBlank, fliSourceImage.GetPixelFormat())).IsFail():
			ErrorPrint(res, "Failed to create the image file.\n")
			break

		# Undistortion 수행 # Execute undistortion
		if not Undistortion(stereoCalibrator, fliSourceImage, fliSourceImage2, fliDestinationImage, fliDestinationImage2):
			break

		
		# 화면에 격자 탐지 결과 출력 # Display the result of grid detection
		sArrGridDisplay = [SGridDisplay(0, CStereoCalibrator3D.SGridResult()) for i in range(5)]
		sArrGridDisplay2 = [SGridDisplay(0, CStereoCalibrator3D.SGridResult()) for i in range(5)]

		for i64ImgIdx in range(fliLearnImage.GetPageCount()):
			sArrGridDisplay[i64ImgIdx].sGridData = CStereoCalibrator3D.SGridResult()
			stereoCalibrator.GetResultGridPoints(sArrGridDisplay[i64ImgIdx].sGridData, i64ImgIdx)
			sArrGridDisplay[i64ImgIdx].i64ImageIdx = i64ImgIdx
			
		for i64ImgIdx in range(fliLearnImage2.GetPageCount()):
			sArrGridDisplay2[i64ImgIdx].sGridData = CStereoCalibrator3D.SGridResult()
			stereoCalibrator.GetResultGridPoints2(sArrGridDisplay2[i64ImgIdx].sGridData, i64ImgIdx)
			sArrGridDisplay2[i64ImgIdx].i64ImageIdx = i64ImgIdx

		msgReceiver.SetGrid(sArrGridDisplay)
		msgReceiver2.SetGrid(sArrGridDisplay2)

		# Learn 이미지 뷰 생성 # Create learn image view
		if (res := viewImageLearn.Create(300, 0, 300 + 480 * 1, 360)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Learn 2 이미지 뷰 생성 # Create learn 2 image view
		if (res := viewImageLearn2.Create(300 + 480, 0, 300 + 480 * 2, 360)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Learn 이미지 뷰에 이미지를 디스플레이 # Display the image in the learn image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Learn 2 이미지 뷰에 이미지를 디스플레이 # Display the image in the learn 2 image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn2.SetImagePtr(fliLearnImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLearn = viewImageLearn.GetLayer(0)
		layerLearn2 = viewImageLearn2.GetLayer(0)
		
		DrawGridPoints(sArrGridDisplay[0], layerLearn)
		DrawGridPoints(sArrGridDisplay2[0], layerLearn2)

		# Destination 이미지 뷰 생성 # Create destination image view
		if (res := viewImageDestination.Create(300, 360, 300 + 480 * 1, 720)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 2 이미지 뷰 생성 # Create destination 2 image view
		if (res := viewImageDestination2.Create(300 + 480, 360, 300 + 480 * 2, 720)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDestination.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 2 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination 2 image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDestination2.SetImagePtr(fliDestinationImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizePointOfView(viewImageDestination)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn2.SynchronizePointOfView(viewImageDestination2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageLearn2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageDestination)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageDestination2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizePageIndex(viewImageLearn2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizePageIndex(viewImageDestination)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizePageIndex(viewImageDestination2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# calibration data 출력 # Display the calibration data
		sIntrinsicParam = stereoCalibrator.GetResultIntrinsicParameters()
		sDistortCoeef = stereoCalibrator.GetResultDistortionCoefficients()

		sIntrinsicParam2 = stereoCalibrator.GetResultIntrinsicParameters2()
		sDistortCoeef2 = stereoCalibrator.GetResultDistortionCoefficients2()

		sRotationParam = stereoCalibrator.GetResultRotationParameters()
		sRotationParam2 = stereoCalibrator.GetResultRotationParameters2()

		sTranslationParam = stereoCalibrator.GetResultTranslationParameters()
		sTranslationParam2 = stereoCalibrator.GetResultTranslationParameters2()

		f64ReprojError = stereoCalibrator.GetResultReProjectionError()
		
		print(f"Intrinsic Parameters")
		print(f"\tFocal Length X: {sIntrinsicParam.f64FocalLengthX}")
		print(f"\tFocal Length Y: {sIntrinsicParam.f64FocalLengthY}")
		print(f"\tPrincipal Point X: {sIntrinsicParam.f64PrincipalPointX}")
		print(f"\tPrincipal Point Y: {sIntrinsicParam.f64PrincipalPointY}")
		print("")
		print(f"Distortion Coefficients")
		print(f"\tK1: {sDistortCoeef.f64K1}")
		print(f"\tK2: {sDistortCoeef.f64K2}")
		print(f"\tP1: {sDistortCoeef.f64P1}")
		print(f"\tP2: {sDistortCoeef.f64P2}")
		print(f"\tK3: {sDistortCoeef.f64K3}")
		print(f"Rotation Parameters")
		print(f"\t{sRotationParam.f64R0:3}\t{sRotationParam.f64R1:3}\t{sRotationParam.f64R2:3}")
		print(f"\t{sRotationParam.f64R3:3}\t{sRotationParam.f64R4:3}\t{sRotationParam.f64R5:3}")
		print(f"\t{sRotationParam.f64R6:3}\t{sRotationParam.f64R7:3}\t{sRotationParam.f64R8:3}")
		print("")
		print(f"Translation Parameters")
		print(f"\t{sTranslationParam.f64T3:3}\t{sTranslationParam.f64T7:3}\t{sTranslationParam.f64T11:3}")
		print("")
		print(f"Intrinsic Parameters 2")
		print(f"\tFocal Length X: {sIntrinsicParam2.f64FocalLengthX}")
		print(f"\tFocal Length Y: {sIntrinsicParam2.f64FocalLengthY}")
		print(f"\tPrincipal Point X: {sIntrinsicParam2.f64PrincipalPointX}")
		print(f"\tPrincipal Point Y: {sIntrinsicParam2.f64PrincipalPointY}")
		print("")
		print(f"Distortion Coefficients 2")
		print(f"\tK1: {sDistortCoeef2.f64K1}")
		print(f"\tK2: {sDistortCoeef2.f64K2}")
		print(f"\tP1: {sDistortCoeef2.f64P1}")
		print(f"\tP2: {sDistortCoeef2.f64P2}")
		print(f"\tK3: {sDistortCoeef2.f64K3}")
		print("")
		print(f"Rotation Parameters 2")
		print(f"\t{sRotationParam2.f64R0:3}\t{sRotationParam2.f64R1:3}\t{sRotationParam2.f64R2:3}")
		print(f"\t{sRotationParam2.f64R3:3}\t{sRotationParam2.f64R4:3}\t{sRotationParam2.f64R5:3}")
		print(f"\t{sRotationParam2.f64R6:3}\t{sRotationParam2.f64R7:3}\t{sRotationParam2.f64R8:3}")
		print("")
		print(f"Translation Parameters 2")
		print(f"\t{sTranslationParam2.f64T3:3}\t{sTranslationParam2.f64T7:3}\t{sTranslationParam2.f64T11:3}")
		print("")
		print(f"Re-Projection Error: {f64ReprojError}")

		i64Height = fliDestinationImage.GetHeight()
		i64Width = fliDestinationImage.GetWidth()

		for i32Iter in range(2):
			for i32Index in range(20):
				fllHorizonLine = CFLLine[Double](0, i64Height / 20 * i32Index, i64Width, i64Height / 20 * i32Index)

				layerDst = viewImageDestination.GetLayer(0) if i32Iter == 0 else viewImageDestination2.GetLayer(0)
				layerDst.DrawFigureImage(fllHorizonLine, EColor.LIME, 1)

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDestination.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDestination2.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageLearn.Invalidate(True)
		viewImageLearn2.Invalidate(True)
		viewImageDestination.Invalidate(True)
		viewImageDestination2.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageLearn.IsAvailable() and viewImageLearn2.IsAvailable() and viewImageDestination.IsAvailable() and viewImageDestination2.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()
