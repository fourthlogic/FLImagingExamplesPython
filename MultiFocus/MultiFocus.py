# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/MultiFocus/Source.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		fliSrcImage.SelectPage(0)

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSrc.Create(400, 0, 1012, 550)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		if (res := viewImageSrc.SetImagePtr(fliSrcImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(1012, 0, 1624, 550)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		if (res := viewImageDst.SetImagePtr(fliDstImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize view.\n")
			break


		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageSrc.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit.\n")
			break


		viewImageSrc.SetFixThumbnailView(True)

		# MultiFocus 객체 생성 # Create MultiFocus object
		multiFocus = CMultiFocus()
		# Source 이미지 설정 # Set the source image
		multiFocus.SetSourceImage(fliSrcImage)
		# Destination 이미지 설정 # Set the destination image
		multiFocus.SetDestinationImage(fliDstImage)
		# Kernel Size 설정 # Set the kernel size
		multiFocus.SetKernel(41)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := multiFocus.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.\n")
			break


		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDst.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit.\n")
			break


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#				 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#				  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()

		if (res := layerSrc.DrawTextCanvas(flp, ("Source Image"), EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		if (res := layerDst.DrawTextCanvas(flp, ("Destination Image"), EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImageSrc.Invalidate(True)

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