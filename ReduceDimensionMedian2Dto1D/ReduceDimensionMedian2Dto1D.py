# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImageX = CFLImage()
	fliDestinationImageY = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDstX = CGUIViewImage()
	viewImageDstY = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/ReduceDimensionMedian2Dto1D/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDestinationImageX.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDestinationImageY.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDstX.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDstY.Create(1124, 0, 1636, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDstX.SetImagePtr(fliDestinationImageX)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDstY.SetImagePtr(fliDestinationImageY)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDstX)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDstY)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Reduce Dimension Median 2D to 1D 객체 생성 # Create Reduce Dimension Median 2D to 1D object
		reduceDimensionMedian2Dto1D = CReduceDimensionMedian2Dto1D()

		# Source 이미지 설정 # Set the source image
		reduceDimensionMedian2Dto1D.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 # Set the destination image
		reduceDimensionMedian2Dto1D.SetDestinationImage(fliDestinationImageX)

		# 축소 차원 설정 # Set reduction dimension
		reduceDimensionMedian2Dto1D.SetReductionDimension(CReduceDimensionMedian2Dto1D.EReductionDimension.X)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := reduceDimensionMedian2Dto1D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Reduce Dimension Median 2D to 1D.')
			break

		# Destination 이미지 설정 # Set the destination image
		reduceDimensionMedian2Dto1D.SetDestinationImage(fliDestinationImageY)

		# 축소 차원 설정 # Set reduction dimension
		reduceDimensionMedian2Dto1D.SetReductionDimension(CReduceDimensionMedian2Dto1D.EReductionDimension.Y)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := reduceDimensionMedian2Dto1D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Reduce Dimension Median 2D to 1D.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestinationX = viewImageDstX.GetLayer(0)
		layerDestinationY = viewImageDstY.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestinationX.Clear()
		layerDestinationY.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestinationX.DrawTextCanvas(flpPoint, 'Destination Image(X Dimension)', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestinationY.DrawTextCanvas(flpPoint, 'Destination Image(Y Dimension)', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDstX.Invalidate(True)
		viewImageDstY.Invalidate(True)

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if((res := (viewImageDstX.ZoomFit())).IsFail()):
			ErrorPrint(res, 'Failed to zoom fit.')
			break

		if((res := (viewImageDstY.ZoomFit())).IsFail()):
			ErrorPrint(res, 'Failed to zoom fit.')
			break

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDstX.IsAvailable() and viewImageDstY.IsAvailable():
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