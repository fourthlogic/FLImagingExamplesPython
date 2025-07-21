# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	
	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageDestination = CGUIViewImage()

	while True:
		res = CResult()

		# 이미지 로드 # Load image
		if (res := fliSourceImage.Load("../../ExampleImages/NoiseImage/NoiseImage1.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSource.Create(400, 0, 1052, 427)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageDestination.Create(1052, 0, 1692, 427)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. .
		if (res := viewImageSource.SynchronizePointOfView(viewImageDestination))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize view. \n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		if (res := viewImageSource.SynchronizeWindow(viewImageDestination))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize window. \n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImageSource.SetImagePtr(fliSourceImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImageDestination.SetImagePtr(fliDestinationImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break

		# Mean Shift Filter 객체 생성 # Create Mean Shift Filter object
		MeanShiftFilter = CMeanShiftFilter()

		# Source 이미지 설정 # Set source image 
		MeanShiftFilter.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 # Set destination image
		MeanShiftFilter.SetDestinationImage(fliDestinationImage)

		# Max iteration 설정 # Set max iteration
		MeanShiftFilter.SetMaxIteration(2)

		# Tolerance 설정 # Set tolerance
		MeanShiftFilter.SetTolerance(0)

		# Spatial bandwidth 설정 # Set spatial bandwidth
		MeanShiftFilter.SetSpatialBandwidth(2)

		# Range bandwidth 설정 # Set range bandwidth
		MeanShiftFilter.SetRangeBandwidth(128)

		# 알고리즘 수행 # Execute the algorithm
		if (res := (MeanShiftFilter.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Mean Shift Filter. \n")
			break


		# 출력을 위한 이미지 레이어를 얻어옵니다. #  Gets the image layer for output.
		# 따로 해제할 필요 없음 # No need to release separately
		layerSource = viewImageSource.GetLayer(0)
		layerDestination = viewImageDestination.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Delete the shapes drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		flpPoint = CFLPoint[Double](0, 0)

		if (res := (layerSource.DrawTextCanvas(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 30))).IsFail():
			ErrorPrint(res, "Failed to draw text. \n")
			break

		if (res := layerDestination.DrawTextCanvas(flpPoint, "Destination Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, "Failed to draw text. \n")
			break

		# 이미지 뷰를 갱신 합니다. # Update the image view.
		viewImageSource.Invalidate(True)
		viewImageDestination.Invalidate(True)

		# image 가 view 크기에 맞도록 확대 또는 축소합니다. # Zoom image to fit the view.
		if (res := (viewImageDestination.ZoomFit())).IsFail():
			ErrorPrint(res, "Failed to zoom fit. \n")
			break

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageSource.IsAvailable() and viewImageDestination.IsAvailable():			
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