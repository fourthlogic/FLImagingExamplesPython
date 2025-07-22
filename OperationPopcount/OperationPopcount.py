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

	res = CResult()

	while True:
		arrU8 = bytearray(32)
		for i in range(16):
			value = ~(0xffff << i) & 0xffff  # 16비트 마스크 유지
			arrU8[2*i] = value & 0xFF        # low byte
			arrU8[2*i+1] = (value >> 8) & 0xFF  # high byte

		# 버퍼로부터 Source 이미지 생성 # Create the source image from the buffer
		if (res := fliSourceImage.Create(4, 4, arrU8, EPixelFormat.C1_U16)).IsFail():
			ErrorPrint(res, "Failed to load the image file. \n")
			break

		# 이미지 뷰 생성 # Create image views
		if (res := viewImageSrc.Create(100, 0, 600, 545)).IsFail() or \
			(res := viewImageDst.Create(600, 0, 1100, 545)).IsFail():
			ErrorPrint(res, "Failed to create the image view. \n")
			break

		# 두 이미지 뷰의 시점을 동기화한다 # Synchronize the viewpoints of the two image views
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view. \n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the images in the image views
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail() or \
			(res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break

		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window. \n")
			break

		algObject = COperationPopcount()

		algObject.SetSourceImage(fliSourceImage)
		algObject.SetDestinationImage(fliDestinationImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute operation popcount.")
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpPoint, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text. \n")
			break

		# Source 이미지 뷰의 Pixel 값을 16진법으로 설정 # Show Pixel Values on Source Image View to Hexadecimal
		viewImageSrc.SetPixelNumberMode(EPixelNumberMode.Hexadecimal)

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
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