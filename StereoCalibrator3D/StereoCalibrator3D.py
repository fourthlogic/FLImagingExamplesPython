# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()

# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliLearnImage = CFLImage()
	fliLearnImage2 = CFLImage()
	fliDestinationImage = CFLImage()
	fliDestinationImage2 = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageLearn2 = CGUIViewImage()
	viewImageDestination = CGUIViewImage()
	viewImageDestination2 = CGUIViewImage()

	while True:
		
		# Learn 이미지 로드 # Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/StereoCalibrator3D/Left.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Learn 2 이미지 로드 # Load the learn 2 image
		if (res := fliLearnImage2.Load('../../ExampleImages/StereoCalibrator3D/Right.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Page 0 선택 # Select page 0
		fliLearnImage.SelectPage(0)
		fliLearnImage2.SelectPage(0)
		
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
		if (res := viewImageLearn.SynchronizePointOfView(viewImageLearn2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizePointOfView(viewImageDestination)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizePointOfView(viewImageDestination2)[0]).IsFail():
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
		
		# Stereo Calibrator 3D 객체 생성 # Create Stereo Calibrator 3D object
		stereoCalibrator = CStereoCalibrator3D()
		
		# Learn 이미지 설정 # Set learn image
		stereoCalibrator.SetLearnImage(fliLearnImage)
		
		# Learn 2 이미지 설정 # Set learn 2 image
		stereoCalibrator.SetLearnImage2(fliLearnImage2)
		
		# Source 이미지 설정 # Set source image
		stereoCalibrator.SetSourceImage(fliLearnImage)
		
		# Source 2 이미지 설정 # Set source 2 image
		stereoCalibrator.SetSourceImage2(fliLearnImage2)
		
		# Destination 이미지 설정 # Set destination image
		stereoCalibrator.SetDestinationImage(fliDestinationImage)

		# Destination 2 이미지 설정 # Set destination 2 image
		stereoCalibrator.SetDestinationImage2(fliDestinationImage2)
		
		# Optimal Solution Accuracy 설정 # Set the optical solution accuracy
		stereoCalibrator.SetOptimalSolutionAccuracy(0.000001)
		
		# Grid Type 설정 # Set the grid type
		stereoCalibrator.SetGridType(CStereoCalibrator3D.EGridType.ChessBoard)
		
		# 앞서 설정된 파라미터 대로 알고리즘 Calibration 수행 # Calibration algorithm according to previously set parameters
		if (res := stereoCalibrator.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Stereo Calibrator 3D.')
			break
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := stereoCalibrator.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Stereo Calibrator 3D.')
			break
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDestination.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDestination2.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLearn = viewImageLearn.GetLayer(0)
		layerLearn2 = viewImageLearn2.GetLayer(0)
		layerDestination = viewImageDestination.GetLayer(0)
		layerDestination2 = viewImageDestination2.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLearn.Clear()
		layerLearn2.Clear()
		layerDestination.Clear()
		layerDestination2.Clear()

		# 이미지 뷰를 갱신 # Update image view
		viewImageLearn.Invalidate(True)
		viewImageLearn2.Invalidate(True)
		viewImageDestination.Invalidate(True)
		viewImageDestination2.Invalidate(True)

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageLearn.IsAvailable() and viewImageLearn2.IsAvailable() and viewImageDestination.IsAvailable() and viewImageDestination2.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()
