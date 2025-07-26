# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		# Source 이미지 로드 // Load the source image
		if (res := (fliSrcImage.Load('../../ExampleImages/RegionInterpolation/Sky_Damaged.flif'))).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break

		# Source 이미지 뷰 생성 // Create the source image view
		if (res := (viewImageSrc.Create(400, 0, 800, 400))).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
			
		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := (viewImageSrc.SetImagePtr(fliSrcImage))[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := (viewImageDst.Create(800, 0, 1200, 400))).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := (viewImageDst.SetImagePtr(fliDstImage))[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break


		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := (viewImageSrc.SynchronizePointOfView(viewImageDst))[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view\n");
			break

		# 이미지 뷰 윈도우의 위치를 맞춤 // Align the position of the image view window
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := (viewImageSrc.SynchronizeWindow(viewImageDst))[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.\n')
			break

		# Bilinear Region Interpolation 객체 생성 // Create Bilinear Region Interpolation object
		sBRI = CBilinearRegionInterpolation()

		# Source 이미지 설정 // Set the source image
		sBRI.SetSourceImage(fliSrcImage)
		# Destination 이미지 설정 // Set the destination image
		sBRI.SetDestinationImage(fliDstImage)
		# 보정 분할 Depth 설정 // Set calibration division depth
		sBRI.SetDivisionDepth(5);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := (sBRI.Execute())).IsFail():
			ErrorPrint(res, 'Failed to execute bilinear region interpolation.')
			break

		# ROI Draw를 위한 CFLRectL 객체 생성 // Create ROI Draw를 위한 CFLRectL object
		flrROI = CFLRect[int](164, 234, 339, 390);

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		layerSrc.Clear()
		layerDst.Clear()

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
		# FLImaging의 Figure 객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능 // FLimaging's Figure objects can be displayed as a function regardless of the shape
		# 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 // The function DrawFigureImage below means drawing a picture based on the image coordinates
		# 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. // The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
		# 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) // Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
		
		if (res := (layerSrc.DrawFigureImage(flrROI, EColor.LIME))).IsFail():
			ErrorPrint(res, 'Failed to draw figure.\n');

		if (res := (layerDst.DrawFigureImage(flrROI, EColor.LIME))).IsFail():
			ErrorPrint(res, 'Failed to draw figure.\n');

		# View 정보를 디스플레이 한다. // Display view information
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. // The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다. // If the color parameter is added as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by processing it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpZero = CFLPoint[Double](0, 0)

		if (res := (layerSrc.DrawTextCanvas(flpZero, 'Source Image', EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break

		if (res := (layerDst.DrawTextCanvas(flpZero, 'Destination Image(Bilinear)', EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break

		# 이미지 뷰를 갱신한다. // Update the image view.
		viewImageSrc.Invalidate(False)
		viewImageDst.Invalidate(False)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()