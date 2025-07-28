# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliCalibrationImage = CFLImage()
	fliDestinationImage = CFLImage()
	fliTextureImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageCalibration = CGUIViewImage()
	viewImageTexture = CGUIViewImage()
	viewImage3D = CGUIView3D()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/PhotometricStereo3D/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Page 0 선택 # Select page 0
		fliSourceImage.SelectPage(0)
		
		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSource.Create(100, 0, 498, 398)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Calibration 이미지 로드 # Load the calibration image
		if (res := fliCalibrationImage.Load('../../ExampleImages/PhotometricStereo3D/Calibrate.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Page 0 선택 # Select page 0
		fliCalibrationImage.SelectPage(0)
		
		# Calibration 이미지 뷰 생성 # Create calibration image view
		if (res := viewImageCalibration.Create(498, 0, 896, 398)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Calibration 이미지 뷰에 이미지를 디스플레이 # Display the image in the calibration image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCalibration.SetImagePtr(fliCalibrationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Texture 이미지 뷰 생성 # Create texture image view
		if (res := viewImageTexture.Create(100, 398, 498, 796)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Texture 이미지 뷰에 이미지를 디스플레이 # Display the image in the texture image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageTexture.SetImagePtr(fliTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 3D 이미지 뷰 생성 # Create destination 3D image view
		if (res := viewImage3D.Create(896, 0, 1692, 769)).IsFail():
			ErrorPrint(res, 'Failed to create the 3D view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizePointOfView(viewImageTexture)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizeWindow(viewImageCalibration)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizeWindow(viewImageTexture)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizeWindow(viewImage3D)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Photometric Stereo 3D 객체 생성 # Create Photometric Stereo 3D object
		photometricStereo = CPhotometricStereo3D()
		
		# Calibration 이미지 설정 # Set the calibration image
		photometricStereo.SetCalibrationImage(fliCalibrationImage)

		# Calibration 데이터 설정 # Set Calibration Settings
		cFLCircle = CFLCircle[Double](386.439657, 346.491239, 259.998140, 0.000000, 0.000000, 360.000000, EArcClosingMethod.EachOther)

		photometricStereo.SetCalibrationCircleROI(cFLCircle)

		# Source 이미지 설정 # Set source image
		photometricStereo.SetSourceImage(fliSourceImage)
		
		# Destination 이미지 설정 # Set destination image
		photometricStereo.SetDestinationHeightMapImage(fliDestinationImage)
		
		# Texture 이미지 설정 # Set texture image
		photometricStereo.SetDestinationTextureImage(fliTextureImage)
		
		# 동작 방식 설정 # Set Operation Mode
		photometricStereo.SetReconstructionMode(CPhotometricStereo3D.EReconstructionMode.Poisson_FP32)

		# Valid 픽셀의 기준 설정 # Set valid pixel ratio
		photometricStereo.SetValidPixelThreshold(0.125)
		
		# Angle Degrees 동작 방식으로 설정 # Set operation method as angle degrees
		cMatTemp = CMatrix[Double](3, 3)

		photometricStereo.SetLightAngleDegrees(cMatTemp)
		
		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibrate algorithm according to previously set parameters
		if (res := photometricStereo.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Photometric Stereo 3D.')
			break

		# Calibrate 된 Angle Degree 데이터 저장 # Save calibrated angle degree data
		cMulVarSlant = CMultiVar[Double]()
		cMulVarTilt = CMultiVar[Double]()

		res, cMulVarSlant, cMulVarTilt = photometricStereo.GetLightAngleDegrees(cMulVarSlant, cMulVarTilt)

		# 위치 데이터 동작 방식으로 설정 # Set operation method as positions
		photometricStereo.SetLightPositions(cMatTemp)
		
		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibrate algorithm according to previously set parameters
		if (res := photometricStereo.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Photometric Stereo 3D.')
			break

		# Calibrate 된 위치 데이터 저장 # Save calibrated position data
		cMatdPosition = CMatrix[Double]()

		photometricStereo.GetLightPositions(cMatdPosition)

		# Calibrate를 실행한 결과를 Console창에 출력합니다. # Output the calibration result to the console window.
		i32CalibPageNum = fliCalibrationImage.GetPageCount()

		# Angle Degrees 데이터 출력
		print(" < Calibration Angle - Degrees >")

		for i in range(i32CalibPageNum):
			print(f"Image {i} ->\tSlant: {cMulVarSlant.GetAt(i):.5}\tTilt: {cMulVarTilt.GetAt(i):.5}")

		print("\n")

		# Positions 데이터 출력
		print(" < Calibration Positions >")

		for i in range(i32CalibPageNum):
			print(f"Image {i} ->\tX: {cMatdPosition.GetValue(i, 0):.5}\tY: {cMatdPosition.GetValue(i, 1):.5} \tZ: {cMatdPosition.GetValue(i, 2):.5}")

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := photometricStereo.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Photometric Stereo 3D.')
			break

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageTexture.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSource.GetLayer(0)
		layerCalibration = viewImageCalibration.GetLayer(0)
		layerTexture = viewImageTexture.GetLayer(0)
		layer3D = viewImage3D.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerCalibration.Clear()
		layerTexture.Clear()
		layer3D.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerCalibration.DrawTextCanvas(flpPoint, 'Calibration Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerTexture.DrawTextCanvas(flpPoint, 'Destination Texture Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 3D 뷰 결과 출력 # Display 3D view result
		
		f64CenterX = fliSourceImage.GetWidth() / 2
		f64CenterY = fliSourceImage.GetHeight() / 2
		f64CenterZ = fliDestinationImage.GetBuffer()[int(f64CenterY * fliSourceImage.GetWidth() + f64CenterX)]

		tp3dFrom = TPoint3[Single](f64CenterX, f64CenterY, f64CenterZ)

		f64MulNum = 2000

		for i in range(i32CalibPageNum):
			strText = ""

			strText += f"X: {cMatdPosition.GetValue(i, 0):.5}    \nY: {cMatdPosition.GetValue(i, 1):.5}    \nZ: {cMatdPosition.GetValue(i, 2):.5}\n"

			tp3dTo = TPoint3[Single](f64MulNum * cMatdPosition.GetValue(i, 0) + f64CenterX, f64MulNum * cMatdPosition.GetValue(i, 1) + f64CenterY, f64MulNum * cMatdPosition.GetValue(i, 2) + f64CenterZ)

			tp3dTod = TPoint3[Double](f64MulNum * cMatdPosition.GetValue(i, 0) + f64CenterX, f64MulNum * cMatdPosition.GetValue(i, 1) + f64CenterY, f64MulNum * cMatdPosition.GetValue(i, 2) + f64CenterZ)

			cgui3dlineTemp = CGUIView3DObjectLine(tp3dFrom, tp3dTo, EColor.YELLOW, 1)

			layer3D.DrawText3D(tp3dTod, strText, EColor.BLACK, EColor.YELLOW)
			
			if (res := viewImage3D.PushObject(cgui3dlineTemp)).IsFail():
				ErrorPrint(res, 'Failed to display the 3D object.')
				break

		fl3DObject = CFL3DObjectHeightMap(fliDestinationImage)
		fl3DObject.SetTextureImage(fliTextureImage)
		
		if (res := viewImage3D.PushObject(fl3DObject)).IsFail():
			ErrorPrint(res, 'Failed to display the 3D object.')
			break

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImage3D.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageSource.Invalidate(True)
		viewImageCalibration.Invalidate(True)
		viewImageTexture.Invalidate(True)
		viewImage3D.Invalidate(True)

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSource.IsAvailable() and viewImageCalibration.IsAvailable() and viewImageTexture.IsAvailable() and viewImage3D.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()
