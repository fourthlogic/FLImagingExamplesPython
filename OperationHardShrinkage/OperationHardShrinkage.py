# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	
	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage0 = CFLImage()
	fliDestinationImage1 = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSource = CGUIViewImage()
	viewImageDestination0 = CGUIViewImage()
	viewImageDestination1 = CGUIViewImage()
	
	res = CResult()

	while True:

		# 이미지 로드 # Load image
		if (res := fliSourceImage.Load("../../ExampleImages/OperationHardShrinkage/Coord1D.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSource.Create(100, 0, 600, 500)).IsFail() or (res := viewImageDestination0.Create(600, 0, 1100, 500)).IsFail() or (res := viewImageDestination1.Create(1100, 0, 1600, 500)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. .
		if (res := viewImageSource.SynchronizePointOfView(viewImageDestination0)[0]).IsFail() or (res := viewImageSource.SynchronizePointOfView(viewImageDestination1)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view. \n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		if (res := viewImageSource.SynchronizeWindow(viewImageDestination0)[0]).IsFail() or (res := viewImageSource.SynchronizeWindow(viewImageDestination1)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window. \n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail() or (res := viewImageDestination0.SetImagePtr(fliDestinationImage0)[0]).IsFail() or (res := viewImageDestination1.SetImagePtr(fliDestinationImage1)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break

		algObject = COperationHardShrinkage()

		algObject.SetSourceImage(fliSourceImage)
		algObject.SetDestinationImage(fliDestinationImage0)
		algObject.SetOperationMode(COperationHardShrinkage.EOperationMode.Forward)
		algObject.SetLambda(0.2);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if ((res := algObject.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute algorithm.")
			break

		algObject.SetDestinationImage(fliDestinationImage1)
		algObject.SetOperationMode(COperationHardShrinkage.EOperationMode.Backward)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.")
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSource.GetLayer(0)
		layerDestination0 = viewImageDestination0.GetLayer(0)
		layerDestination1 = viewImageDestination1.GetLayer(0)

		# 기존에 Layer 에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination0.Clear()
		layerDestination1.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if ((res := layerSource.DrawTextCanvas(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDestination0.DrawTextCanvas(flpPoint, "Destination Forward Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDestination1.DrawTextCanvas(flpPoint, "Destination Backward Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text. \n")
			break

		# 이미지 뷰의 값 표현 방식 설정 # Set how values are expressed in image view
		viewImageSource.SetPixelNumberMode(EPixelNumberMode.Decimal)
		viewImageDestination0.SetPixelNumberMode(EPixelNumberMode.Decimal)
		viewImageDestination1.SetPixelNumberMode(EPixelNumberMode.Decimal)

		# floating 이미지의 색상 표현 범위 설정 # Set the color expression range of floating images
		viewImageSource.SetFloatingImageValueRange(-1.0, 1.0)
		viewImageDestination0.SetFloatingImageValueRange(-1.0, 1.0)
		viewImageDestination1.SetFloatingImageValueRange(-1.0, 1.0)

		# 이미지 뷰를 갱신 # Update image view
		viewImageSource.Invalidate(True)
		viewImageDestination0.Invalidate(True)
		viewImageDestination1.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageSource.IsAvailable() and viewImageDestination0.IsAvailable() and viewImageDestination1.IsAvailable():			
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