# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/NoiseGenerator/Plate.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDestinationImage.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
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

		# Noise Generator 객체 생성 # Create Noise Generator object
		noiseGenerator = CNoiseGenerator()

		# Source 이미지 설정 # Set the source image
		noiseGenerator.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 # Set the destination image
		noiseGenerator.SetDestinationImage(fliDestinationImage)

		# ROI 객체 생성 및 범위 설정 # Create ROI object and set range
		rectROI = CFLRect[Int64](61,63,583,376)

		# 처리할 ROI 설정 # Set the ROI to be processed
		noiseGenerator.SetSourceROI(rectROI)
		noiseGenerator.SetDestinationROI(rectROI)
		
		# 생성할 노이즈 타입 설정 # Set the noise type to generate
		noiseGenerator.SetNoiseType(CNoiseGenerator.ENoiseType.PhotonNoise)
		# 광자양 잡음의 광자 평균양 설정 # Set the average photon amount of photon noise
		noiseGenerator.SetPhotonCount(1000)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := noiseGenerator.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Noise Generator.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# ROI 영역을 Source Image View에 출력 # Display the ROI area to Source Image View
		if (res := layerSource.DrawFigureImage(rectROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw Source ROI.')
			break

		# ROI 영역을 Destination Image View에 출력 # Display the ROI area to Destination Image View
		if (res := layerDestination.DrawFigureImage(rectROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw Destination ROI.')
			break	
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
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