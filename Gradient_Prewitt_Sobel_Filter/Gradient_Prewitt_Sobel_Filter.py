
# FLImagingClrPy 선언 // Declare FLImagingClrPy
from enum import Enum
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

class Edst(Enum):
	Gradient = 0
	Prewitt = 1
	Sobel = 2
	EDstCount = 3

# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	listFliDestinationImage = list[CFLImage]()

	for i in range(0, Edst.EDstCount) :
		listFliDestinationImage.append(CFLImage())

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	listViewImageDst = list[CGUIViewImage]()

	for i in range(0, Edst.EDstCount) :
		listViewImageDst.append(CGUIViewImage())

	bError = False

	while True:
		
		# Source 이미지 로드 // Load the source image
		res = fliSourceImage.Load("../../ExampleImages/EdgeDetection/Alphabat.flif")
		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(400, 0, 800, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		for i in range(0, Edst.EDstCount) :

			# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
			if (res := listFliDestinationImage[i].Assign(fliSourceImage)).IsFail():
				ErrorPrint(res, 'Failed to load the image file.')
				bError = True
				break

			i32X = (i + 1) % 2;
			i32Y = int((i + 1) / 2);

			# Destination 이미지 뷰 생성 // Create the destination image view
			if (res := listViewImageDst[i].Create(i32X * 400 + 400, i32Y * 400, i32X * 400 + 400 + 400, i32Y * 400 + 400)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				bError = True
				break

			# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := listViewImageDst[i].SetImagePtr(listFliDestinationImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				bError = True
				break

			# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the three image views
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := viewImageSrc.SynchronizePointOfView(listViewImageDst[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view.')
				bError = True
				break

			# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := viewImageSrc.SynchronizeWindow(listViewImageDst[i])[0]).IsFail():
				ErrorPrint(res[0], 'Failed to synchronize window.')
				bError = True
				break

		if bError:
			break

		# ROI 설정을 위한 FLRect 생성
		flrROI = CFLRect[int](200, 200, 500, 500);

		# Convolution Gradient 객체 생성 // Create Convolution Gradient object
		convolutionGradient = CGradientFilter();

		# Source 이미지 설정 // Set the source image
		convolutionGradient.SetSourceImage(fliSourceImage);
		# Source ROI 설정 // Set the Source ROI
		convolutionGradient.SetSourceROI(flrROI);
		# Destination 이미지 설정 // Set the destination image
		convolutionGradient.SetDestinationImage(listFliDestinationImage[Edst.Gradient]);
		# Destination ROI 설정 // Set Destination ROI
		convolutionGradient.SetDestinationROI(flrROI);
		# Convolution Gradient 커널 연산 방법 설정
		convolutionGradient.SetKernelMethod(CGradientFilter.EKernel.Gradient);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := convolutionGradient.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Gradient Filter.')
			break

		# Convolution Prewitt 객체 생성 // Create Convolution Prewitt object
		convolutionPrewitt = CPrewittFilter();

		# Source 이미지 설정 // Set the source image
		convolutionPrewitt.SetSourceImage(fliSourceImage);
		# Source ROI 설정 // Set the Source ROI
		convolutionPrewitt.SetSourceROI(flrROI);
		# Destination 이미지 설정 // Set the destination image
		convolutionPrewitt.SetDestinationImage(listFliDestinationImage[Edst.Prewitt]);
		# Destination ROI 설정 // Set Destination ROI
		convolutionPrewitt.SetDestinationROI(flrROI);
		# Convolution Prewitt 커널 연산 방법 설정
		convolutionPrewitt.SetKernelMethod(CPrewittFilter.EKernel.Prewitt);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := convolutionPrewitt.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Prewitt Filter.')
			break

		# Convolution Sobel 객체 생성 // Create Convolution Sobel object
		convolutionSobel = CSobelFilter();

		# Source 이미지 설정 // Set the source image
		convolutionSobel.SetSourceImage(fliSourceImage);
		# Source ROI 설정 // Set the Source ROI
		convolutionSobel.SetSourceROI(flrROI);
		# Destination 이미지 설정 // Set the destination image
		convolutionSobel.SetDestinationImage(listFliDestinationImage[Edst.Sobel]);
		# Destination ROI 설정 // Set Destination ROI
		convolutionSobel.SetDestinationROI(flrROI);
		# Convolution Sobel 커널 연산 방법 설정
		convolutionSobel.SetKernelMethod(CSobelFilter.EKernel.Sobel);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := convolutionSobel.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Sobel Filter.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		listLayerDst = list[CGUIViewImageLayer]()

		for i in range(0, Edst.EDstCount) :
			listLayerDst.append(listViewImageDst[i].GetLayer(0))

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		listLayerDst[Edst.Gradient].Clear()
		listLayerDst[Edst.Prewitt].Clear()
		listLayerDst[Edst.Sobel].Clear()

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
		# FLImaging의 Figure 객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능 // FLimaging's Figure objects can be displayed as a function regardless of the shape
		# 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 // The function DrawFigureImage below means drawing a picture based on the image coordinates
		# 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. // The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
		# 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) // Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		if (res := listLayerDst[Edst.Gradient].DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		if (res := listLayerDst[Edst.Prewitt].DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		if (res := listLayerDst[Edst.Sobel].DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# 이미지 뷰 정보 표시 // Display image view information
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. // The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다.
		# If the color parameter is set as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by treating it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := listLayerDst[Edst.Gradient].DrawTextCanvas(flpPoint, 'Gradient Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := listLayerDst[Edst.Prewitt].DrawTextCanvas(flpPoint, 'Prewitt Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := listLayerDst[Edst.Sobel].DrawTextCanvas(flpPoint, 'Sobel Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)

		for i in range(0, Edst.EDstCount) :
			listViewImageDst[i].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and listViewImageDst[Edst.Gradient].IsAvailable() and listViewImageDst[Edst.Prewitt].IsAvailable() and listViewImageDst[Edst.Sobel].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

if __name__ == '__main__':
    main()