# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliISrcImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = [CGUIViewImage() for i in range(1)]
	
	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliISrcImage.Load('../../ExampleImages/PixelCounter/Semiconductor.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# 이미지 뷰 생성 # Create source image view
		if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Pixel Counter 객체 생성 # Create Pixel Counter object
		PixelCounter = CPixelCounter()

		# Source 이미지 설정 # Set source image 
		PixelCounter.SetSourceImage(fliISrcImage)

		# Source ROI 이미지 설정 # Set Source ROI
		flfSourceROI = CFLQuad[Double](170.550171, 102.400000, 380.243003, 135.950853, 341.100341, 312.092833, 124.417747, 265.960410)
		PixelCounter.SetSourceROI(flfSourceROI)

		# threshold 모드 설정(Single) # Set Threshold Mode(Single)
		PixelCounter.SetThresholdMode(EThresholdMode.Single)

		# 임계값 설정 (다채널 경우 CMultiVar 사용) # Set threshold value(Use CMultiVarD for multi-channel)
		PixelCounter.SetThreshold(120, EThresholdIndex.First)
		PixelCounter.SetThreshold(230, EThresholdIndex.Second)

		# 논리 조건 설정 # Set condition value
		PixelCounter.SetLogicalCondition(int(ELogicalCondition.Greater), EThresholdIndex.First)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := PixelCounter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Pixel Counter.')
			break
		
		i64TotalPixel = PixelCounter.GetResultTotalPixelCount()
		i64ValidPixel = PixelCounter.GetResultValidPixelCount()
		i64InvalidPixel = PixelCounter.GetResultInvalidPixelCount()

		# 전체 픽셀, 유효한 픽셀, 유효하지 않은 픽셀 갯수 출력 # display Total, Valid, Invalid Pixel Count
		print(f"Total Pixel Count : {i64TotalPixel}")
		print(f"Valid Pixel Count : {i64ValidPixel}")
		print(f"Invalid Pixel Count : {i64InvalidPixel}")

		# Text 출력 # Display Text 
		flsDrawText = f"Source Image\n120 < threshold\nTotal Pixel Count: {i64TotalPixel}\nValid Pixel Count: {i64ValidPixel}\nInvalid Pixel Count: {i64InvalidPixel}"

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer1 = viewImage[0].GetLayer(0)
		
		flpPoint = CFLPoint[Double](0, 0)
		
		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layer1.DrawTextImage(flpPoint, flsDrawText, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# Source ROI 출력 // Display Source ROI 
		if (res := layer1.DrawFigureImage(flfSourceROI, EColor.LIME)).IsFail():
			ErrorPrint(res, "Failed to draw Source ROI .\n");

		# 이미지 뷰를 갱신 합니다. # Update the image view.
		viewImage[0].Invalidate(True)
			
		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImage[0].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()