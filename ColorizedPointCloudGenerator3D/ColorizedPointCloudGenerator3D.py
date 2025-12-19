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
	fliCaliSrcXYZVImage = CFLImage()
	fliCaliSrcColorImage = CFLImage()
	fliExecSrcXYZVImage = CFLImage()
	fliExecSrcColorImage = CFLImage()
	fliExecDstColorImage = CFLImage()
	fliSampDstColorImage = CFLImage()

	# 이미지 뷰 선언 # Declare image view
	viewCaliSrcXYZVImage = CGUIViewImage()
	viewCaliSrcColorImage = CGUIViewImage()
	viewExecSrcXYZVImage = CGUIViewImage()
	viewExecSrcColorImage = CGUIViewImage()
	viewExecDstColorImage = CGUIViewImage()
	viewSampDstColorImage = CGUIViewImage()

	# 3D 뷰 선언 # Declare 3D view
	view3DDst = CGUIView3D()

	while True:

		# 수행 결과 객체 선언 # Declare execution result object
		res = CResult(EResult.UnknownError)

		# Calibration Source XYZV 이미지 로드 # Load Calibration Source XYZV image
		if (res := fliCaliSrcXYZVImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/CalibXYZV.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break

		# Calibration Source XYZV 이미지 뷰 생성 # Create Calibration Source XYZV image view
		if (res := viewCaliSrcXYZVImage.Create(100, 0, 400, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break

		# Calibration Source XYZV 이미지 뷰에 이미지를 디스플레이 # Display image in Calibration Source XYZV image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SetImagePtr(fliCaliSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break


		# Calibration Source Color 이미지 로드 # Load Calibration Source Color image
		if (res := fliCaliSrcColorImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/CalibRGB.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break

		# Calibration Source Color 이미지 뷰 생성 # Create Calibration Source Color image view
		if (res := viewCaliSrcColorImage.Create(100, 300, 400, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break

		# Calibration Source Color 이미지 뷰에 이미지를 디스플레이 # Display image in Calibration Source Color image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcColorImage.SetImagePtr(fliCaliSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break


		# Execution Source XYZV 이미지 로드 # Load Execution Source XYZV image
		if (res := fliExecSrcXYZVImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/ExecXYZV.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break

		# Execution Source XYZV 이미지 뷰 생성 # Create Execution Source XYZV image view
		if (res := viewExecSrcXYZVImage.Create(400, 0, 700, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break

		# Execution Source XYZV 이미지 뷰에 이미지를 디스플레이 # Display image in Execution Source XYZV image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewExecSrcXYZVImage.SetImagePtr(fliExecSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break


		# Execution Source Color 이미지 로드 # Load Execution Source Color image
		if (res := fliExecSrcColorImage.Load('../../ExampleImages/ColorizedPointCloudGenerator3D/ExecRGB.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break

		# Execution Source Color 이미지 뷰 생성 # Create Execution Source Color image view
		if (res := viewExecSrcColorImage.Create(400, 300, 700, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break

		# Execution Source Color 이미지 뷰에 이미지를 디스플레이 # Display image in Execution Source Color image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewExecSrcColorImage.SetImagePtr(fliExecSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break


		# Execution Destination Color 이미지 뷰 생성 # Create Execution Destination Color image view
		if (res := viewExecDstColorImage.Create(700, 0, 1000, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break

		# Execution Destination Color 이미지 뷰에 이미지를 디스플레이 # Display image in Execution Destination Color image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewExecDstColorImage.SetImagePtr(fliExecDstColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		

		# Execution Sampled Destination 이미지 뷰 생성 # Create Execution Sampled Destination image view
		if (res := viewSampDstColorImage.Create(700, 300, 1000, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Execution Sampled Destination 이미지 뷰에 이미지를 디스플레이 # Display image in Execution Sampled Destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSampDstColorImage.SetImagePtr(fliSampDstColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		

		# Destination 3D 뷰 생성 # Create Destination 3D view
		if (res := view3DDst.Create(1000, 0, 1600, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the 3D view.\n')
			break
		

		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizeWindow(viewCaliSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizeWindow(viewExecSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizeWindow(viewExecSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizeWindow(viewExecDstColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizeWindow(viewSampDstColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizeWindow(view3DDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		

		# 두 이미지 뷰 윈도우의 Page를 동기화 한다 # Synchronize pages of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewCaliSrcXYZVImage.SynchronizePageIndex(viewCaliSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize page index between image views.\n')
			break
		

		# Colorized Point Cloud Generator 3D 객체 생성 # Create Colorized Point Cloud Generator 3D object
		colorizedPointCloudGenerator3D = CColorizedPointCloudGenerator3D()

		# Calibration Source XYZV 이미지 설정 # Set Calibration Source XYZV image
		if (res := colorizedPointCloudGenerator3D.SetCalibrationXYZVImage(fliCaliSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Calibration Source XYZV image.\n')
			break
		
		# Calibration Source Color 이미지 설정 # Set Calibration Source Color image
		if (res := colorizedPointCloudGenerator3D.SetCalibrationColorImage(fliCaliSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Calibration Source Color image.\n')
			break
		
		# Calibration에 사용되는 Grid Type 설정 # Set grid type used in calibration
		if (res := colorizedPointCloudGenerator3D.SetGridType(CCameraCalibrator.EGridType.ChessBoard)).IsFail():
			ErrorPrint(res, 'Failed to set calibration grid type.\n')
			break
		
		# Calibration의 최적해 정확도 값 설정 # Set optimal solution accuracy of calibration
		if (res := colorizedPointCloudGenerator3D.SetOptimalSolutionAccuracy(0.00001)).IsFail():
			ErrorPrint(res, 'Failed to set calibration optimal solution accuracy.\n')
			break
		
		# 자동 Coordinate Adjustment 사용 여부 설정 # Set auto coordinate adjustment flag
		if (res := colorizedPointCloudGenerator3D.EnableAutoCoordinateAdjustment(True)).IsFail():
			ErrorPrint(res, 'Failed to set coordinate adjustment flag.\n')
			break
		
		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibration algorithm according to previously set parameters
		if (res := colorizedPointCloudGenerator3D.Calibrate()).IsFail():
			ErrorPrint(res, 'Failed to calibrate Colorized Point Cloud Generator 3D.\n')
			break
		

		# Calibration 결과 출력 # Print calibration results
		print(f' < Calibration Result >\n')

		# Color 카메라의 Intrinsic Parameter 출력 # Print intrinsic parameters of color camera
		calibIntrinsic = colorizedPointCloudGenerator3D.GetResultIntrinsicParameters()

		print(f' < Intrinsic Parameters >')

		print(f'Focal Length X ->\t{calibIntrinsic.f64FocalLengthX:.7}')
		print(f'Focal Length Y ->\t{calibIntrinsic.f64FocalLengthY:.7}')
		print(f'Principal Point X ->\t{calibIntrinsic.f64PrincipalPointX:.7}')
		print(f'Principal Point Y ->\t{calibIntrinsic.f64PrincipalPointY:.7}')
		print(f'Skew ->\t{calibIntrinsic.f64Skew:.7}')

		print(f'')

		# Color 카메라의 Distortion Coefficient 출력 # Print distortion coefficients of color camera
		calibDistortion = colorizedPointCloudGenerator3D.GetResultDistortionCoefficients()

		print(f' < Distortion Coefficients >')

		print(f'K1 ->\t{calibDistortion.f64K1:.7}')
		print(f'K2 ->\t{calibDistortion.f64K2:.7}')
		print(f'P1 ->\t{calibDistortion.f64P1:.7}')
		print(f'P2 ->\t{calibDistortion.f64P2:.7}')
		print(f'K3 ->\t{calibDistortion.f64K3:.7}')

		print(f'')

		# 두 카메라 간의 회전 행렬 출력 # Print relative rotation matrix between both cameras
		matRotation = CMatrix[Double]()

		if (res := colorizedPointCloudGenerator3D.GetResultRelativeRotation(matRotation)[0]).IsFail():
			ErrorPrint(res, 'Failed to get relative rotation.\n')
			break
		
		print(f' < Relative Rotation >')

		print(f'R00 ->\t{matRotation.GetValue(0, 0):.7}')
		print(f'R01 ->\t{matRotation.GetValue(0, 1):.7}')
		print(f'R02 ->\t{matRotation.GetValue(0, 2):.7}')
		print(f'R10 ->\t{matRotation.GetValue(1, 0):.7}')
		print(f'R11 ->\t{matRotation.GetValue(1, 1):.7}')
		print(f'R12 ->\t{matRotation.GetValue(1, 2):.7}')
		print(f'R20 ->\t{matRotation.GetValue(2, 0):.7}')
		print(f'R21 ->\t{matRotation.GetValue(2, 1):.7}')
		print(f'R22 ->\t{matRotation.GetValue(2, 2):.7}')

		print(f'')

		# 두 카메라 간의 변환 행렬 출력 # Print relative translation matrix between both cameras
		matTranslation = CMatrix[Double]()

		if (res := colorizedPointCloudGenerator3D.GetResultRelativeTranslation(matTranslation)[0]).IsFail():
			ErrorPrint(res, 'Failed to get relative translation.\n')
			break
		
		print(f' < Relative Translation >\n')

		print(f'TX ->\t{matTranslation.GetValue(0, 0):.7}')
		print(f'TY ->\t{matTranslation.GetValue(1, 0):.7}')
		print(f'TZ ->\t{matTranslation.GetValue(2, 0):.7}')

		print(f'')


		# 출력에 사용되는 3D 객채 생성 # Create 3D object used as output
		fl3DDstObj = CFL3DObject()

		# Execution Source XYZV 이미지 설정 # Set Execution Source XYZV image
		if (res := colorizedPointCloudGenerator3D.SetSourceXYZVImage(fliExecSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Execution Source XYZV image.\n')
			break
		
		# Execution Source Color 이미지 설정 # Set Execution Source Color image
		if (res := colorizedPointCloudGenerator3D.SetSourceColorImage(fliExecSrcColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Execution Source Color image.\n')
			break
		
		# Execution Destination Color 이미지 설정 # Set Execution Destination Color image
		if (res := colorizedPointCloudGenerator3D.SetDestinationColorImage(fliExecDstColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Execution Destination Color image.\n')
			break
		
		# Execution Destination Sampled Color 이미지 설정 # Set Execution Destination Sampled Color image
		if (res := colorizedPointCloudGenerator3D.SetDestinationSampledColorImage(fliSampDstColorImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Execution Destination Sampled Color image.\n')
			break
		
		# Sampled 픽셀 표시 Color 설정 # Set color of the sampled pixels in BGR
		if (res := colorizedPointCloudGenerator3D.SetSampledBGRValue(255, 255, 0)).IsFail():
			ErrorPrint(res, 'Failed to set sampled pixel BGR value.\n')
			break
		
		# Execution Destination 3D Object 설정 # Set Execution Destination 3D Object
		if (res := colorizedPointCloudGenerator3D.SetDestination3DObject(fl3DDstObj)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Execution Destination 3D Object.\n')
			break
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := colorizedPointCloudGenerator3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Colorized Point Cloud Generator 3D.\n')
			break
		

		# 결과 3D 객체 출력 # Print resulting 3D Object
		if (res := view3DDst.PushObject(fl3DDstObj)).IsFail():
			ErrorPrint(res, 'Failed to display the 3D Object.\n')
			break
		
		# 3D View 카메라 설정 # Set 3D view camera
		fl3DCam = CFL3DCamera()

		fl3DCam.SetDirection(CFLPoint3[Single](0, 0, 1))
		fl3DCam.SetDirectionUp(CFLPoint3[Single](0, -1, 0))
		fl3DCam.SetPosition(CFLPoint3[Single](0, 0, -1000))

		view3DDst.SetCamera(fl3DCam)

		# 화면에 출력하기 위해 이미지 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
	    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released
		layerImageCaliSrcXYZV = viewCaliSrcXYZVImage.GetLayer(0)
		layerImageCaliSrcColor = viewCaliSrcColorImage.GetLayer(0)
		layerImageExecSrcXYZV = viewExecSrcXYZVImage.GetLayer(0)
		layerImageExecSrcColor = viewExecSrcColorImage.GetLayer(0)
		layerImageExecDstColor = viewExecDstColorImage.GetLayer(0)
		layerImageSampDstColor = viewSampDstColorImage.GetLayer(0)

		# 화면에 출력하기 위해 3D 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from 3D view for display
		# 이 객체는 3D 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an 3D view and does not need to be released
		layer3DDst = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear figures drawn on existing layer
		layerImageCaliSrcXYZV.Clear()
		layerImageCaliSrcColor.Clear()
		layerImageExecSrcXYZV.Clear()
		layerImageExecSrcColor.Clear()
		layerImageExecDstColor.Clear()
		layerImageSampDstColor.Clear()
		layer3DDst.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerImageCaliSrcXYZV.DrawTextCanvas(CFLPoint[Double](0, 0), 'Calibration Source XYZV Image', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerImageCaliSrcColor.DrawTextCanvas(CFLPoint[Double](0, 0), 'Calibration Source Color Image', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerImageExecSrcXYZV.DrawTextCanvas(CFLPoint[Double](0, 0), 'Execution Source XYZV Image', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerImageExecSrcColor.DrawTextCanvas(CFLPoint[Double](0, 0), 'Execution Source Color Image', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerImageExecDstColor.DrawTextCanvas(CFLPoint[Double](0, 0), 'Destination Color Image', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerImageSampDstColor.DrawTextCanvas(CFLPoint[Double](0, 0), 'Destination Sampled Color Image', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		# 3D 뷰 정보 표시 # Display 3D view information
		if (res := layer3DDst.DrawTextCanvas(CFLPoint[Double](0, 0), '3D Destination Colored Point Cloud', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		

		# 새로 생성한 이미지를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created image
		if (res := viewExecDstColorImage.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to zoom fit image view.\n')
			break
		
		# 새로 생성한 이미지를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created image
		if (res := viewSampDstColorImage.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to zoom fit image view.\n')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewCaliSrcXYZVImage.Invalidate(True)
		viewCaliSrcColorImage.Invalidate(True)
		viewExecSrcXYZVImage.Invalidate(True)
		viewExecSrcColorImage.Invalidate(True)
		viewExecDstColorImage.Invalidate(True)
		viewSampDstColorImage.Invalidate(True)

		# 3D 뷰를 갱신 # Update 3D view
		view3DDst.Invalidate(True)
		

		# 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until a view is closed before exiting
		while viewCaliSrcXYZVImage.IsAvailable() and viewCaliSrcColorImage.IsAvailable() and viewExecSrcXYZVImage.IsAvailable() and viewExecSrcColorImage.IsAvailable() and viewExecDstColorImage.IsAvailable() and viewSampDstColorImage.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
	main()
