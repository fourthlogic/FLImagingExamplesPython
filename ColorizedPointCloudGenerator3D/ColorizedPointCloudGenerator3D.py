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
	fliCaliSrcXYZVImage = CFLImage()
	fliCaliSrcRGBImage = CFLImage()
	fliExecSrcXYZVImage = CFLImage()
	fliExecSrcRGBImage = CFLImage()
	fliExecDstRGBImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageCaliSrcXYZV = CGUIViewImage()
	viewImageCaliSrcRGB = CGUIViewImage()
	viewImageExecSrcXYZV = CGUIViewImage()
	viewImageExecSrcRGB = CGUIViewImage()
	viewImageExecDstRGB = CGUIViewImage()
	view3DDst = CGUIView3D()

	while True:
		
		# Calibrate XYZV 이미지 로드 # Load the calibrate XYZV image
		if (res := fliCaliSrcXYZVImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/CalibXYZV.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Calibrate XYZV 이미지 뷰 생성 # Create calibrate XYZV image view
		if (res := viewImageCaliSrcXYZV.Create(100, 0, 400, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Calibrate XYZV 이미지 뷰에 이미지를 디스플레이 # Display the image in the calibrate XYZV image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SetImagePtr(fliCaliSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Calibrate RGB 이미지 로드 # Load the calibrate RGB image
		if (res := fliCaliSrcRGBImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/CalibRGB.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Calibrate RGB 이미지 뷰 생성 # Create calibrate RGB image view
		if (res := viewImageCaliSrcRGB.Create(100, 300, 400, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Calibrate RGB 이미지 뷰에 이미지를 디스플레이 # Display the image in the calibrate RGB image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcRGB.SetImagePtr(fliCaliSrcRGBImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Execute XYZV 이미지 로드 # Load the execute XYZV image
		if (res := fliExecSrcXYZVImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/ExecXYZV.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Execute XYZV 이미지 뷰 생성 # Create execute XYZV image view
		if (res := viewImageExecSrcXYZV.Create(400, 0, 700, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Execute XYZV 이미지 뷰에 이미지를 디스플레이 # Display the image in the execute XYZV image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageExecSrcXYZV.SetImagePtr(fliExecSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Execute RGB 이미지 로드 # Load the execute RGB image
		if (res := fliExecSrcRGBImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/ExecRGB.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Execute RGB 이미지 뷰 생성 # Create execute RGB image view
		if (res := viewImageExecSrcRGB.Create(400, 300, 700, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Execute RGB 이미지 뷰에 이미지를 디스플레이 # Display the image in the execute RGB image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageExecSrcRGB.SetImagePtr(fliExecSrcRGBImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰 생성 # Create destination image view
		if (res := viewImageExecDstRGB.Create(700, 0, 1000, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageExecDstRGB.SetImagePtr(fliExecDstRGBImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 3D 이미지 뷰 생성 # Create destination 3D image view
		if (res := view3DDst.Create(700, 300, 1300, 900)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SynchronizeWindow(viewImageCaliSrcRGB)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SynchronizeWindow(viewImageExecSrcRGB)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SynchronizeWindow(viewImageExecSrcXYZV)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SynchronizeWindow(viewImageExecDstRGB)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SynchronizeWindow(view3DDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageCaliSrcXYZV.SynchronizePageIndex(viewImageCaliSrcRGB)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Colorized Point Cloud Generator 3D 객체 생성 # Colorized Point Cloud Generator 3D object
		colorizedPointCloudGenerator3D = CColorizedPointCloudGenerator3D()
		
		# Calibration XYZV 이미지 설정 # Set calibration XYZV image
		colorizedPointCloudGenerator3D.SetCalibrationImageXYZV(fliCaliSrcXYZVImage)
		
		# Calibration RGB 이미지 설정 # Set calibration RGB image
		colorizedPointCloudGenerator3D.SetCalibrationImageRGB(fliCaliSrcRGBImage)
		
		# Calibration의 Grid Type 설정 # Set the grid type of the calibration
		colorizedPointCloudGenerator3D.SetGridType(CCameraCalibrator.EGridType.ChessBoard)
		
		# Calibration의 최적해 정확도 값 설정 # Set the optimal solution accuracy of the calibration
		colorizedPointCloudGenerator3D.SetOptimalSolutionAccuracy(0.00001)
		
		# Coordinate Adjustment 자동 설정 # Coordinate Adjustment Auto Set Flag
		colorizedPointCloudGenerator3D.EnableAutoCoordinateAdjustment(True)
		
		# 앞서 설정된 파라미터 대로 Calibration 동작 # Calibrate algorithm according to previously set parameters
		if (res := colorizedPointCloudGenerator3D.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Colorized Point Cloud Generator 3D.')
			break

		
		# Calibration 결과 출력 # Print calibration results
		print(f' < Calibration Result >\n')

		# RGB 카메라의 Intrinsic Parameter 출력 # Print the intrinsic parameters of the RGB camera
		cCalibIntrinsic = colorizedPointCloudGenerator3D.GetIntrinsicParameters()

		print(f' < Intrinsic Parameters >\n')

		print(f'Focal Length X ->\t{cCalibIntrinsic.f64FocalLengthX:.7}')
		print(f'Focal Length Y ->\t{cCalibIntrinsic.f64FocalLengthY:.7}')
		print(f'Principal Point X ->\t{cCalibIntrinsic.f64PrincipalPointX:.7}')
		print(f'Principal Point Y ->\t{cCalibIntrinsic.f64PrincipalPointY:.7}')
		print(f'Skew ->\t{cCalibIntrinsic.f64Skew:.7}')

		print()

		# RGB 카메라의 Distortion Coefficient 출력 # Print the distortion coefficients of the RGB camera
		cCalibDistortion = colorizedPointCloudGenerator3D.GetDistortionCoefficients()

		print(f' < Distortion Coefficients >\n')

		print(f'K1 ->\t{cCalibDistortion.f64K1:.7}')
		print(f'K2 ->\t{cCalibDistortion.f64K2:.7}')
		print(f'P1 ->\t{cCalibDistortion.f64P1:.7}')
		print(f'P2 ->\t{cCalibDistortion.f64P2:.7}')
		print(f'K3 ->\t{cCalibDistortion.f64K3:.7}')
		
		print()

		# 두 카메라 간의 회전 행렬 출력 # Print the relative rotation matrix between both cameras
		cMatRotation = CMatrix[Double]()

		colorizedPointCloudGenerator3D.GetRelativeRotation(cMatRotation)

		print(f' < Relative Rotation >\n')

		print(f'R00 ->\t%{cMatRotation.GetValue(0, 0):.7}')
		print(f'R01 ->\t%{cMatRotation.GetValue(0, 1):.7}')
		print(f'R02 ->\t%{cMatRotation.GetValue(0, 2):.7}')
		print(f'R10 ->\t%{cMatRotation.GetValue(1, 0):.7}')
		print(f'R11 ->\t%{cMatRotation.GetValue(1, 1):.7}')
		print(f'R12 ->\t%{cMatRotation.GetValue(1, 2):.7}')
		print(f'R20 ->\t%{cMatRotation.GetValue(2, 0):.7}')
		print(f'R21 ->\t%{cMatRotation.GetValue(2, 1):.7}')
		print(f'R22 ->\t%{cMatRotation.GetValue(2, 2):.7}')
		
		print()

		# 두 카메라 간의 변환 행렬 출력 # Print the relative translation matrix between both cameras
		cMatTranslation = CMatrix[Double]()

		colorizedPointCloudGenerator3D.GetRelativeTranslation(cMatTranslation)

		print(f' < Relative Translation >\n')

		print(f'TX ->\t{cMatTranslation.GetValue(0, 0):.7}', )
		print(f'TY ->\t{cMatTranslation.GetValue(1, 0):.7}', )
		print(f'TZ ->\t{cMatTranslation.GetValue(2, 0):.7}', )
		
		print()


		# 출력에 사용되는 3D 객채 생성 # Create 3D object used as output
		fli3DDstObj = CFL3DObject()

		# Execution XYZV 이미지 설정 # Set execution XYZV image
		colorizedPointCloudGenerator3D.SetSourceImageXYZV(fliExecSrcXYZVImage)
		
		# Execution RGB 이미지 설정 # Set execution RGB image
		colorizedPointCloudGenerator3D.SetSourceImageRGB(fliExecSrcRGBImage)
		
		# Destination 이미지 설정 # Set destination image
		colorizedPointCloudGenerator3D.SetDestinationImageRGB(fliExecDstRGBImage)
		
		# Destination 3D Object 설정 # Set the destination 3D object
		colorizedPointCloudGenerator3D.SetDestination3DObject(fli3DDstObj)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := colorizedPointCloudGenerator3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Colorized Point Cloud Generator 3D.')
			break

		# 결과 3D 객체 출력 # Print 3D Object
		if (res := view3DDst.PushObject(fli3DDstObj)).IsFail():
			ErrorPrint(res, 'Failed to display the 3D object.')
			break

		# 3D View 카메라 설정 # Set 3D view camera
		fli3DCam = CFL3DCamera()

		flP3Dir = CFLPoint3[Single](0, 0, 1)
		flP3DirUp = CFLPoint3[Single](0, -1, 0)
		flP3Pos = CFLPoint3[Single](0, 0, -1000)
		
		fli3DCam.SetDirection(flP3Dir)
		fli3DCam.SetDirectionUp(flP3DirUp)
		fli3DCam.SetPosition(flP3Pos)

		view3DDst.SetCamera(fli3DCam)

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageExecDstRGB.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageCaliSrcXYZV.Invalidate(True)
		viewImageCaliSrcRGB.Invalidate(True)
		viewImageExecSrcXYZV.Invalidate(True)
		viewImageExecSrcRGB.Invalidate(True)
		viewImageExecDstRGB.Invalidate(True)
		view3DDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageCaliSrcXYZV.IsAvailable() and viewImageCaliSrcRGB.IsAvailable() and viewImageExecSrcXYZV.IsAvailable() and viewImageExecSrcRGB.IsAvailable() and viewImageExecDstRGB.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()
