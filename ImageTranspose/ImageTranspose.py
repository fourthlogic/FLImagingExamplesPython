# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImageXY = CFLImage()
	fliDestinationImageXZ = CFLImage()
	fliDestinationImageYX = CFLImage()
	fliDestinationImageYZ = CFLImage()
	fliDestinationImageZX = CFLImage()
	fliDestinationImageZY = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageDestinationXY = CGUIViewImage()
	viewImageDestinationXZ = CGUIViewImage()
	viewImageDestinationYX = CGUIViewImage()
	viewImageDestinationYZ = CGUIViewImage()
	viewImageDestinationZX = CGUIViewImage()
	viewImageDestinationZY = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/ImageTranspose/Gradation.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSource.Create(100, 0, 700, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create destination image view
		if (res := viewImageDestinationXY.Create(700, 0, 1000, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDestinationXZ.Create(1000, 0, 1300, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDestinationYX.Create(1300, 0, 1600, 300)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDestinationYZ.Create(700, 300, 1000, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDestinationZX.Create(1000, 300, 1300, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDestinationZY.Create(1300, 300, 1600, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source와 Desitination 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the source and destination image view windows
		if (res := viewImageSource.SynchronizeWindow(viewImageDestinationXY)[0]).IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSource.SynchronizeWindow(viewImageDestinationXZ)[0]).IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSource.SynchronizeWindow(viewImageDestinationYX)[0]).IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSource.SynchronizeWindow(viewImageDestinationYZ)[0]).IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSource.SynchronizeWindow(viewImageDestinationZX)[0]).IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSource.SynchronizeWindow(viewImageDestinationZY)[0]).IsFail() :
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDestinationXY.SetImagePtr(fliDestinationImageXY)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDestinationXZ.SetImagePtr(fliDestinationImageXZ)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDestinationYX.SetImagePtr(fliDestinationImageYX)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDestinationYZ.SetImagePtr(fliDestinationImageYZ)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDestinationZX.SetImagePtr(fliDestinationImageZX)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDestinationZY.SetImagePtr(fliDestinationImageZY)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Image Transpose 객체 생성 # Create Image Transpose object
		imageTranspose = CImageTranspose()

		# Source 이미지 설정 # Set the source image
		imageTranspose.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 # Set the destination image
		imageTranspose.SetDestinationImage(fliDestinationImageXY)

		# Transpose 후 사용자에게 보일 평면을 XY 평면으로 설정 # Set the plane to the XY plane to be visible to the user after Transpose
		imageTranspose.SetResultPlane(CImageTranspose.EPlane.XY);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := imageTranspose.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Image Transpose.')
			break

		# Destination 이미지 설정 # Set the destination image
		imageTranspose.SetDestinationImage(fliDestinationImageXZ)

		# Transpose 후 사용자에게 보일 평면을 XZ 평면으로 설정 # Set the plane to the XZ plane to be visible to the user after Transpose
		imageTranspose.SetResultPlane(CImageTranspose.EPlane.XZ);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := imageTranspose.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Image Transpose.')
			break

		# Destination 이미지 설정 # Set the destination image
		imageTranspose.SetDestinationImage(fliDestinationImageYX)

		# Transpose 후 사용자에게 보일 평면을 YX 평면으로 설정 # Set the plane to the YX plane to be visible to the user after Transpose
		imageTranspose.SetResultPlane(CImageTranspose.EPlane.YX);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := imageTranspose.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Image Transpose.')
			break

		# Destination 이미지 설정 # Set the destination image
		imageTranspose.SetDestinationImage(fliDestinationImageYZ)

		# Transpose 후 사용자에게 보일 평면을 YZ 평면으로 설정 # Set the plane to the YZ plane to be visible to the user after Transpose
		imageTranspose.SetResultPlane(CImageTranspose.EPlane.YZ);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := imageTranspose.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Image Transpose.')
			break

		# Destination 이미지 설정 # Set the destination image
		imageTranspose.SetDestinationImage(fliDestinationImageZX)

		# Transpose 후 사용자에게 보일 평면을 ZX 평면으로 설정 # Set the plane to the ZX plane to be visible to the user after Transpose
		imageTranspose.SetResultPlane(CImageTranspose.EPlane.ZX);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := imageTranspose.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Image Transpose.')
			break

		# Destination 이미지 설정 # Set the destination image
		imageTranspose.SetDestinationImage(fliDestinationImageZY)

		# Transpose 후 사용자에게 보일 평면을 ZY 평면으로 설정 # Set the plane to the ZY plane to be visible to the user after Transpose
		imageTranspose.SetResultPlane(CImageTranspose.EPlane.ZY);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := imageTranspose.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Image Transpose.')
			break

		# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춰준다. # With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen.
		viewImageDestinationXY.ZoomFit();
		viewImageDestinationXZ.ZoomFit();
		viewImageDestinationYX.ZoomFit();
		viewImageDestinationYZ.ZoomFit();
		viewImageDestinationZX.ZoomFit();
		viewImageDestinationZY.ZoomFit();

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSource.GetLayer(0)
		layerDestinationXY = viewImageDestinationXY.GetLayer(0)
		layerDestinationXZ = viewImageDestinationXZ.GetLayer(0)
		layerDestinationYX = viewImageDestinationYX.GetLayer(0)
		layerDestinationYZ = viewImageDestinationYZ.GetLayer(0)
		layerDestinationZX = viewImageDestinationZX.GetLayer(0)
		layerDestinationZY = viewImageDestinationZY.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestinationXY.Clear()
		layerDestinationXZ.Clear()
		layerDestinationYX.Clear()
		layerDestinationYZ.Clear()
		layerDestinationZX.Clear()
		layerDestinationZY.Clear()
		flpZero = CFLPoint[Double](0, 0)

		if(res := layerSource.DrawTextCanvas(flpZero , 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if(res := layerDestinationXY.DrawTextCanvas(flpZero , 'XY Plane Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if(res := layerDestinationXZ.DrawTextCanvas(flpZero , 'XZ Plane Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if(res := layerDestinationYX.DrawTextCanvas(flpZero , 'YX Plane Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if(res := layerDestinationYZ.DrawTextCanvas(flpZero , 'YZ Plane Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if(res := layerDestinationZX.DrawTextCanvas(flpZero , 'ZX Plane Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if(res := layerDestinationZY.DrawTextCanvas(flpZero , 'ZY Plane Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSource.Invalidate(True)
		viewImageDestinationXY.Invalidate(True)
		viewImageDestinationXZ.Invalidate(True)
		viewImageDestinationYX.Invalidate(True)
		viewImageDestinationYZ.Invalidate(True)
		viewImageDestinationZX.Invalidate(True)
		viewImageDestinationZY.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSource.IsAvailable() and viewImageDestinationXY.IsAvailable() and viewImageDestinationXZ.IsAvailable() and viewImageDestinationYX.IsAvailable() and viewImageDestinationYZ.IsAvailable() and viewImageDestinationZX.IsAvailable() and viewImageDestinationZY.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()