# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/OperationCompare/candle.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(400, 0, 912, 484)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()

		# HOG 객체 생성 // Create HOG object
		hog = CHistogramsOfOrientedGradients()

		# ROI 범위 설정 // Set the ROI value
		flrROI = CFLRect[int](200, 10, 300, 200)

		# Source 이미지 설정 // Set the source image
		hog.SetSourceImage(fliSourceImage)

		# Source ROI 설정 // Set the Source ROI
		hog.SetSourceROI(flrROI)

		# 알고리즘 수행 // Execute the algorithm
		if (res := hog.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Histograms Of Oriented Gradients.')
			break

		# 실행 결과를 받아오기 위한 컨테이너 // Container to get Calculated results
		flfaPeakVectors = CFLFigureArray()

		# 피크 벡터 추출 // Get Peak Vectors
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := hog.GetPeakVectorsFigure(0,flfaPeakVectors)[0]).IsFail():
			ErrorPrint(res, 'Failed to get result.')
			break

		# 피크 벡터를 출력 // Print Peak Vectors
		layerSource.DrawFigureImage(flfaPeakVectors.GetAt(0), EColor.BLUE, 3, EColor.BLUE, EGUIViewImagePenStyle.Solid, 0.3, 0.3)
		layerSource.DrawFigureImage(flfaPeakVectors.GetAt(1), EColor.GREEN, 3, EColor.GREEN, EGUIViewImagePenStyle.Solid, 0.3, 0.3)
		layerSource.DrawFigureImage(flfaPeakVectors.GetAt(2), EColor.RED, 3, EColor.RED, EGUIViewImagePenStyle.Solid, 0.3, 0.3)
		
		# ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figures objects on the image view.')
			break

		# 이미지 뷰를 갱신 합니다. // Update image view
		viewImageSrc.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		while viewImageSrc.IsAvailable() :
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

if __name__ == '__main__':
    main()