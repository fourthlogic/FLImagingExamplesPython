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
	fliSrcXYZVImage = CFLImage()
	fliSrcTextureImage = CFLImage()

	# 3D 객체 선언 # Declare 3D object
	floDestination = CFL3DObject()

	# 이미지 뷰 선언 # Declare image view
	viewSrcXYZVImage = CGUIViewImage()
	viewSrcTextureImage = CGUIViewImage()

	# 3D 뷰 선언 # Declare 3D view
	view3DDst = CGUIView3D()

	while True:

		# 수행 결과 객체 선언 # Declare execution result object
		res = CResult(EResult.UnknownError)

		# Source XYZV 이미지 로드 # Load Source XYZV image
		if (res := fliSrcXYZVImage.Load('../../ExampleImages/XYZImageToPointCloudConverter3D/XYZV.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break
		
		# Source Texture 이미지 로드 # Load Source Texture image
		if (res := fliSrcTextureImage.Load('../../ExampleImages/XYZImageToPointCloudConverter3D/Texture.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break
		
		# Source XYZV 이미지 뷰 생성 # Create Source XYZV image view
		if (res := viewSrcXYZVImage.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Source Texture 이미지 뷰 생성 # Create Source Texture image view
		if (res := viewSrcTextureImage.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Destination 3D 뷰 생성 # Create Destination 3D view
		if (res := view3DDst.Create(100, 512, 612, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the 3D view.\n')
			break
		
		# Source XYZV 이미지 뷰에 이미지를 디스플레이 # Display image in Source XYZV image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcXYZVImage.SetImagePtr(fliSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# Source Texture 이미지 뷰에 이미지를 디스플레이 # Display image in Source Texture image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcTextureImage.SetImagePtr(fliSrcTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# 두 이미지 뷰의 시점을 동기화 # Synchronize viewpoints of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcXYZVImage.SynchronizePointOfView(viewSrcTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize point of view between image views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := view3DDst.SynchronizeWindow(viewSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := view3DDst.SynchronizeWindow(viewSrcTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# XYZ Image To Point Cloud Converter 3D 객체 생성 # Create XYZ Image To Point Cloud Converter 3D object
		xyzImageToPointCloudConverter3D = CXYZImageToPointCloudConverter3D()

		# Source XYZV 이미지 설정 # Set Source XYZV image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := xyzImageToPointCloudConverter3D.SetSourceImage(fliSrcXYZVImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Source XYZV image.\n')
			break
		
		# Source Texture 이미지 설정 # Set Source Texture image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := xyzImageToPointCloudConverter3D.SetTextureImage(fliSrcTextureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Source Texture image.\n')
			break
		
		# Destination Point Cloud 설정 # Set Destination Point Cloud
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := xyzImageToPointCloudConverter3D.SetDestinationObject(floDestination)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Destination 3D object.\n')
			break
		
		# Coordinate Adjustment Scale 설정 # Set coordinate adjustment scale
		if (res := xyzImageToPointCloudConverter3D.SetCoordinateAdjustmentScale(1, -1, -1)).IsFail():
			ErrorPrint(res, 'Failed to set coordinate adjustment scale.\n')
			break
		
		# Coordinate Adjustment Offset 설정 # Set coordinate adjustment offset
		if (res := xyzImageToPointCloudConverter3D.SetCoordinateAdjustmentOffset(-41, -5, 900)).IsFail():
			ErrorPrint(res, 'Failed to set coordinate adjustment offset.\n')
			break
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := xyzImageToPointCloudConverter3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute XYZ Image To Point Cloud Converter 3D.\n')
			break
		

		# 결과 3D 객체 출력 # Print resulting 3D Object
		if (res := view3DDst.PushObject(floDestination)).IsFail():
			ErrorPrint(res, 'Failed to display the 3D Object.\n')
			break
		
		# 3D View 카메라 설정 # Set 3D view camera
		fl3DCam = CFL3DCamera()

		fl3DCam.SetDirection(CFLPoint3[Single](0, 0, -1))
		fl3DCam.SetDirectionUp(CFLPoint3[Single](0, 1, 0))
		fl3DCam.SetPosition(CFLPoint3[Single](10, -20, 750))

		view3DDst.SetCamera(fl3DCam)

		# 화면에 출력하기 위해 이미지 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released
		layerViewXYZV = viewSrcXYZVImage.GetLayer(0)
		layerViewTexture = viewSrcTextureImage.GetLayer(0)

		# 화면에 출력하기 위해 3D 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from 3D view for display
		# 이 객체는 3D 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an 3D view and does not need to be released
		layerView3D = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear figures drawn on existing layer
		layerViewXYZV.Clear()
		layerViewTexture.Clear()
		layerView3D.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerViewXYZV.DrawTextCanvas(CFLPoint[Double](0, 0), 'XYZV Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerViewTexture.DrawTextCanvas(CFLPoint[Double](0, 0), 'Texture Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerView3D.DrawTextCanvas(CFLPoint[Double](0, 0), 'Destination Point Cloud', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewSrcXYZVImage.Invalidate(True)
		viewSrcTextureImage.Invalidate(True)

		# 3D 뷰를 갱신 # Update 3D view
		view3DDst.Invalidate(True)

		# 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until a view is closed before exiting
		while viewSrcXYZVImage.IsAvailable() and viewSrcTextureImage.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)
		
		break
	
	# End of main function

if __name__ == '__main__':
    main()