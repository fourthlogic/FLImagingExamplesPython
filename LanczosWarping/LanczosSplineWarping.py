# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage =  [CFLImage(), CFLImage()]
	fliDestinationImage = [CFLImage(), CFLImage()]

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc= [CGUIViewImage(), CGUIViewImage()]
	viewImageDst= [CGUIViewImage(), CGUIViewImage()]

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage[0].Load('../../ExampleImages/LanczosSplineWarping/chess.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc[0].Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if (res := viewImageSrc[1].Create(100, 512, 612, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst[0].Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if (res := viewImageSrc[1].Create(612, 512, 1124, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SynchronizePointOfView(viewImageSrc[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageDst[1].SynchronizePointOfView(viewImageSrc[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc[0].SetImagePtr(fliSourceImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc[1].SetImagePtr(fliSourceImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SetImagePtr(fliDestinationImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDst[1].SetImagePtr(fliDestinationImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SynchronizeWindow(viewImageSrc[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
			
		if (res := viewImageDst[1].SynchronizeWindow(viewImageSrc[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Lanczos Spline Warping 객체 생성 // Create Lanczos Spline Warping object
		lanczosSplineWarping = CLanczosSplineWarping()

		# Source 이미지 설정 // Set the source image
		lanczosSplineWarping.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set the destination image
		lanczosSplineWarping.SetDestinationImage(fliDestinationImage)
	
		# Interpolation Method 설정 // Set the interpolation method
		lanczosSplineWarping.SetInterpolationMethod(EInterpolationMethod.Bilinear);
		
		# 그리드를 (5,5)로 초기화 // Initialize the grid to (5,5)
		CFLPoint<Int> flpGridSize =CFLPoint<Int>(5, 5);
		CFLPoint<Int> flpGridIndex = CFLPoint<Int>();
		flpaSource = CFLPointArray();
		flpaDestination = CFLPointArray();

		f64ScaleX = fliSourceImage[0].GetWidth() / 4.0;
		f64ScaleY = fliSourceImage[0].GetHeight() / 4.0;

		for y in range( flpGridSize.y):
			flpGridIndex.y = y;

			for x in range( flpGridSize.x):
				flpGridIndex.x = x;

				# Grid Index와 같은 좌표로 Source 좌표를 설정 // Set Source coordinates to the same coordinates as Grid Index
				CFLPoint<Double> flpSource = CFLPoint<Double>(flpGridIndex.x * f64ScaleX, flpGridIndex.y * f64ScaleY);

				f64RandomX = CRandomGenerator.Double(-0.2, 0.2);
				f64RandomY = CRandomGenerator.Double(-0.2, 0.2);

				# 외곽의 좌표는 안쪽으로 변형 되도록 설정 // Set the outer coordinates to be Warpinged inward
				if y == 0:
					f64RandomY = -f64RandomY if f64RandomY < 0 else f64RandomY
				
				if x == 0:
					f64RandomX = -f64RandomX if f64RandomX < 0 else f64RandomX
				
				if y == flpGridSize.y - 1:
					f64RandomY = -f64RandomY if  f64RandomY > 0 else f64RandomY
				
				if x == flpGridSize.x - 1:
					f64RandomX = -f64RandomX if f64RandomX < 0 else f64RandomX
				
				# Grid Index와 같은 좌표에서 미세한 랜덤 값을 부여해서 좌표를 왜곡 // Distort coordinates by giving fine random values at the same coordinates as Grid Index
				CFLPoint<Double> flpDistortion = CFLPoint<Double>((flpGridIndex.x + f64RandomX) * f64ScaleX, (flpGridIndex.y + f64RandomY) * f64ScaleY)
				
				flpaSource.PushBack(flpSource)
				flpaDestination.PushBack(flpDistortion)
                  








		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := lanczosSplineWarping.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Flip.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageDst.GetLayer(0)
		layerDestination = [viewImageSrc[0].GetLayer(0), viewImageSrc[1].GetLayer(0), viewImageSrc[2].GetLayer(0)]

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination[0].Clear()
		layerDestination[1].Clear()
		layerDestination[2].Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		res = layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerDestination[0].DrawTextCanvas(flpPoint, 'Destination Image Horizontal', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerDestination[1].DrawTextCanvas(flpPoint, 'Destination Image Vertical', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		res = layerDestination[2].DrawTextCanvas(flpPoint, 'Destination Image Both', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageDst.Invalidate(True)
		viewImageSrc[0].Invalidate(True)
		viewImageSrc[1].Invalidate(True)
		viewImageSrc[2].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageDst.IsAvailable() and viewImageSrc[0].IsAvailable() and viewImageSrc[1].IsAvailable() and viewImageSrc[2].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()