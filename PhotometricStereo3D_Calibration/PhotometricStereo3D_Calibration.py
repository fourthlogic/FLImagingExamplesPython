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


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare image object
	fliSourceImage = CFLImage()
	fliCalibrationImage = CFLImage()
	fliDestinationImage = CFLImage()
	fliCurvatureImage = CFLImage()
	fliTextureImage = CFLImage()

	# 이미지 뷰 선언 # Declare image view
	viewSourceImage = CGUIViewImage()
	viewCalibrationImage = CGUIViewImage()
	viewTextureImage = CGUIViewImage()
	viewCurvatureImage = CGUIViewImage()

	# 3D 뷰 선언 # Declare 3D view
	view3DDst = CGUIView3D()

	while True:

		# 수행 결과 객체 선언 # Declare execution result object
		res = CResult(EResult.UnknownError)

		# Source 이미지 로드 # Load Source image
		if (res := fliSourceImage.Load('../../ExampleImages/PhotometricStereo3D/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break
		
		# Source 이미지 뷰 생성 # Create Source image view
		if (res := viewSourceImage.Create(100, 0, 498, 398)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Source 이미지 뷰에 이미지를 디스플레이 # Display image in Source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# Calibration 이미지 로드 # Load Calibration image
		if (res := fliCalibrationImage.Load('../../ExampleImages/PhotometricStereo3D/Calibrate.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break
		
		# Calibration 이미지 뷰 생성 # Create Calibration image view
		if (res := viewCalibrationImage.Create(498, 0, 896, 398)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Calibration 이미지 뷰에 이미지를 디스플레이 # Display image in Calibration image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCalibrationImage.SetImagePtr(fliCalibrationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# Texture 이미지 뷰 생성 # Create Texture image view
		if (res := viewTextureImage.Create(100, 398, 498, 796)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Texture 이미지 뷰에 이미지를 디스플레이 # Display image in Texture image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewTextureImage.SetImagePtr(fliTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# Curvature 이미지 뷰 생성 # Create Curvature image view
		if (res := viewCurvatureImage.Create(498, 398, 896, 796)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Curvature 이미지 뷰에 이미지를 디스플레이 # Display image in Curvature image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCurvatureImage.SetImagePtr(fliCurvatureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# Destination 3D 뷰 생성 # Create Destination 3D view
		if (res := view3DDst.Create(896, 0, 1692, 796)).IsFail():
			ErrorPrint(res, 'Failed to create the 3D view.\n')
			break
		
		# 두 이미지 뷰의 시점을 동기화 # Synchronize viewpoints of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizePointOfView(viewTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize point of view between image views.\n')
			break
		
		# 두 이미지 뷰의 시점을 동기화 # Synchronize viewpoints of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizePointOfView(viewCurvatureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize point of view between image views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizeWindow(viewCalibrationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizeWindow(viewCurvatureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizeWindow(viewTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizeWindow(view3DDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# Photometric Stereo 3D 객체 생성 # Create Photometric Stereo 3D object
		photometricStereo3D = CPhotometricStereo3D()

		# 출력에 사용되는 3D Height Map 객채 생성 # Create 3D height map used as output
		fl3DOHM = CFL3DObjectHeightMap()

		# Source 이미지 설정 # Set Source image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := photometricStereo3D.SetSourceImage(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Source image.\n')
			break
		
		# Calibration 이미지 설정 # Set Calibration image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := photometricStereo3D.SetCalibrationImage(fliCalibrationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Calibration image.\n')
			break
		
		# Destination Height Map 이미지 설정 # Set Destination Height Map image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := photometricStereo3D.SetDestinationHeightMapImage(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Destination Height Map image.\n')
			break
		
		# Destination Texture 이미지 설정 # Set Destination Texture image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := photometricStereo3D.SetDestinationTextureImage(fliTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Destination Texture image.\n')
			break
		
		# Destination Curvature 이미지 설정 # Set Destination Curvature image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := photometricStereo3D.SetCurvatureImage(fliCurvatureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Destination Curvature image.\n')
			break
		
		# Destination 3D Object 설정 # Set Destination 3D Object 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := photometricStereo3D.SetDestinationObject(fl3DOHM)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Destination 3D Object.\n')
			break
		
		# Calibration Circle ROI 설정 # Set calibration circle ROI settings
		if (res := photometricStereo3D.SetCalibrationCircleROI(CFLCircle[Double](117.210526, 104.842105, 78.736842, 0.000000, 0.000000, 360.000000, EArcClosingMethod.EachOther))).IsFail():
			ErrorPrint(res, 'Failed to set Calibration Circle ROI.\n')
			break
		
		# 동작 방식 설정 # Set reconstruction mode
		if (res := photometricStereo3D.SetReconstructionMode(CPhotometricStereo3D.EReconstructionMode.Poisson_FP32)).IsFail():
			ErrorPrint(res, 'Failed to set reconstruction mode.\n')
			break
		
		# Valid 픽셀의 기준 설정 # Set valid pixel ratio
		if (res := photometricStereo3D.SetValidPixelThreshold(0.25)).IsFail():
			ErrorPrint(res, 'Failed to set valid pixel threshold.\n')
			break
		
		# Curvature 이미지 Normalization 여부 설정 # Set curvature image normalization option
		if (res := photometricStereo3D.EnableCurvatureNormalization(True)).IsFail():
			ErrorPrint(res, 'Failed to set curvature normalization flag.\n')
			break
		
		# Angle Degrees 동작 방식으로 설정 # Set operation method as angle degrees
		if (res := photometricStereo3D.SetCalibrationMode(CPhotometricStereo3D.ECalibrationMode.Angle_Degrees)).IsFail():
			ErrorPrint(res, 'Failed to set light angle in degrees.\n')
			break
		
		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibration algorithm according to previously set parameters
		if (res := photometricStereo3D.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Photometric Stereo 3D.\n')
			break
		
		# Calibrate 된 Angle Degree 데이터 # Calibrated angle degree data
		mvdSlant = CMultiVar[Double]()
		mvdTilt = CMultiVar[Double]()

		# Calibrate 된 Angle Degree 데이터 저장 # Save calibrated angle degree data
		if (res := photometricStereo3D.GetLightAngleDegrees(mvdSlant, mvdTilt)[0]).IsFail():
			ErrorPrint(res, 'Failed to get light angle in degrees.\n')
			break
		
		# 위치 데이터 동작 방식으로 설정 # Set operation method as positions
		if (res := photometricStereo3D.SetCalibrationMode(CPhotometricStereo3D.ECalibrationMode.Positions)).IsFail():
			ErrorPrint(res, 'Failed to set light positions.\n')
			break
		
		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibration algorithm according to previously set parameters
		if (res := photometricStereo3D.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Photometric Stereo 3D.\n')
			break
		
		# Calibrate 된 위치 데이터 # Calibrated position data
		matPosition = CMatrix[Double]()

		# Calibrate 된 위치 데이터 저장 # Save calibrated position data
		if (res := photometricStereo3D.GetLightPositions(matPosition)[0]).IsFail():
			ErrorPrint(res, 'Failed to get light positions.\n')
			break
		
		# Calibrate를 실행한 결과를 Console창에 출력 # Output calibration result to console window
		i32CalibPageNum = fliCalibrationImage.GetPageCount()
		
		# Angle Degrees 데이터 출력
		print(" < Calibration Angle - Degrees >")

		for i in range(i32CalibPageNum):
			print(f"Image {i} ->\tSlant: {mvdSlant.GetAt(i):.5}\tTilt: {mvdTilt.GetAt(i):.5}")

		print("\n")

		# Positions 데이터 출력
		print(" < Calibration Positions >")

		for i in range(i32CalibPageNum):
			print(f"Image {i} ->\tX: {matPosition.GetValue(i, 0):.5}\tY: {matPosition.GetValue(i, 1):.5} \tZ: {matPosition.GetValue(i, 2):.5}")
			
		# Pixel Accuracy 설정 # Set pixel accuracy
		if (res := photometricStereo3D.SetPixelAccuracy(70)).IsFail():
			ErrorPrint(res, "Failed to set valid pixel accuracy.\n")
			break

		if (res := photometricStereo3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Photometric Stereo 3D.\n')
			break
		
		# 화면에 출력하기 위해 이미지 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released
		layerSource = viewSourceImage.GetLayer(0)
		layerCalibration = viewCalibrationImage.GetLayer(0)
		layerCurvature = viewCurvatureImage.GetLayer(0)
		layerTexture = viewTextureImage.GetLayer(0)

		# 화면에 출력하기 위해 3D 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from 3D view for display
		# 이 객체는 3D 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an 3D view and does not need to be released
		layer3DDestination = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear figures drawn on existing layer
		layerSource.Clear()
		layerCalibration.Clear()
		layerCurvature.Clear()
		layerTexture.Clear()
		layer3DDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(CFLPoint[Double](0, 0), 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerCalibration.DrawTextCanvas(CFLPoint[Double](0, 0), 'Calibration Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerTexture.DrawTextCanvas(CFLPoint[Double](0, 0), 'Destination Texture Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerCurvature.DrawTextCanvas(CFLPoint[Double](0, 0), 'Destination Curvature Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		# 3D View 정보 디스플레이 # Display 3D view information
		f32CenterX = fliSourceImage.GetWidth() / 2
		f32CenterY = fliSourceImage.GetHeight() / 2
		f32CenterZ = fliDestinationImage.GetBuffer()[int(f32CenterY * fliSourceImage.GetWidth() + f32CenterX)]

		f32CenterX *= 70;
		f32CenterY *= 70;
		f32CenterZ *= 70;

		tp3dFrom = TPoint3[Single](f32CenterX, f32CenterY, f32CenterZ)
		
		f64MulNum = 30000

		for i in range(i32CalibPageNum):
			strText = ""

			strText += f"X: {matPosition.GetValue(i, 0):.5}    \nY: {matPosition.GetValue(i, 1):.5}    \nZ: {matPosition.GetValue(i, 2):.5}\n"

			tp3dTo = TPoint3[Single](f64MulNum * matPosition.GetValue(i, 0) + f32CenterX, f64MulNum * matPosition.GetValue(i, 1) + f32CenterY, f64MulNum * matPosition.GetValue(i, 2) + f32CenterZ)

			tp3dTod = TPoint3[Double](f64MulNum * matPosition.GetValue(i, 0) + f32CenterX, f64MulNum * matPosition.GetValue(i, 1) + f32CenterY, f64MulNum * matPosition.GetValue(i, 2) + f32CenterZ)

			cgui3dlineTemp = CGUIView3DObjectLine(tp3dFrom, tp3dTo, EColor.YELLOW, 1)

			layer3DDestination.DrawText3D(tp3dTod, strText, EColor.BLACK, EColor.YELLOW)

			view3DDst.PushObject(cgui3dlineTemp)
		
		# 3D Height Map에 Texture 적용 # Apply texture to 3D height map
		if (res := fl3DOHM.SetTextureImage(fliTextureImage)).IsFail():
			ErrorPrint(res, "Failed to apply texture to height map.\n")
			break

		res = fl3DOHM.ActivateVertexColorTexture(True)

		# 결과 3D 객체 출력 # Print resulting 3D Object
		if (res := view3DDst.PushObject(fl3DOHM)).IsFail():
			ErrorPrint(res, 'Failed to display the 3D Object.\n')
			break
		
		# 새로 생성한 이미지를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created image
		if (res := viewTextureImage.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to zoom fit image view.\n')
			break
		
		# 새로 생성한 이미지를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created image
		if (res := viewCurvatureImage.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to zoom fit image view.\n')
			break
		
		# 새로 생성한 3D Object를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created 3D object
		if (res := view3DDst.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to zoom fit 3D view.\n')
			break
		
		# 이미지 뷰를 갱신 합니다. # Update image view
		viewSourceImage.Invalidate(True)
		viewTextureImage.Invalidate(True)
		viewCalibrationImage.Invalidate(True)
		viewCurvatureImage.Invalidate(True)

		# 3D 뷰를 갱신 # Update 3D view
		view3DDst.Invalidate(True)

		# 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until a view is closed before exiting
		while viewSourceImage.IsAvailable() and viewTextureImage.IsAvailable() and viewCalibrationImage.IsAvailable() and viewCurvatureImage.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)
		
		break
	
	# End of main function



if __name__ == '__main__':
    main()
