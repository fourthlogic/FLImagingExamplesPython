# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	view3DDst = CGUIView3D()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/laserTriangulation3D/SrcImage.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 600, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(600, 0, 1100, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Destination 3D 이미지 뷰 생성 # Create the destination 3D image view
		if (res := view3DDst.Create(100, 448, 1100, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(view3DDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# Baseline ROI 생성 # Set the base line of the laser
		fliBaseLine = CFLLine[Double](0, 61, 1216, 61)

		# Census Transform 객체 생성 # Create Census Transform object
		laserTriangulation = CLaserTriangulation3D()

		# Source 이미지 설정 # Set the source image
		laserTriangulation.SetSourceImage(fliSourceImage)

		# Destination Height Map 이미지 설정 # Set the destination height map image
		laserTriangulation.SetDestinationHeightMapImage(fliDestinationImage)

		# Baseline ROI 설정 # Set the base line of the laser
		laserTriangulation.SetBaseLine(fliBaseLine)

		# Source 이미지 타입 설정 # Set the type of the source image
		laserTriangulation.SetSourceType(CLaserTriangulation3D.ESourceType.Image)

		# Pixel Accuracy 설정 # Set the pixel accuracy
		laserTriangulation.SetPixelAccuracy(0.165)

		# Scan Accuracy 설정 # Set the scan accuracy
		laserTriangulation.SetScanAccuracy(0.2)

		# Working Distance 설정 # Set the working distance
		laserTriangulation.SetWorkingDistance(214.7)

		# 레이저 각도 설정 # Set the angle of laser
		laserTriangulation.SetAngleOfLaser(60)

		# 레이저 밝기 설정 # Set laser brightness threshold
		laserTriangulation.SetLaserThreshold(64)

		# 평균 Window의 pixel 길이 설정 # Set Average Window Pixel Length
		laserTriangulation.SetAverageWindowLength(5)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := laserTriangulation.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Laser Triangulation.')
			break

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDst.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# 3D 뷰 결과 출력 # Display 3D view result
		fl3DOHM = CFL3DObjectHeightMap(fliDestinationImage)
		
		if (res := view3DDst.PushObject(fl3DOHM)).IsFail():
			ErrorPrint(res, 'Failed to add 3D Object.')
			break
		
		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := view3DDst.ZoomFit()).IsFail():
			ErrorPrint(res, 'Failed to Zoom Fit.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)
		layer3DDestination = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layer3DDestination.DrawTextCanvas(flpPoint, 'Destination 3D', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)
		view3DDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable() and view3DDst.IsAvailable():
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