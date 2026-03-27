# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	
	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/ActiveContour/Grid Of Cross.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if ((res := viewImageSrc.Create(100, 0, 600, 500)).IsFail() or
			(res := viewImageDst.Create(600, 0, 1100, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail() or
			(res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		viewImageDst.EnablePixelSegmentationMode(True)


		# 알고리즘 객체 생성 # Create algorithm object
		activeContour = CActiveContour()

		# Source 이미지 설정 # Set source image 
		if (res := activeContour.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# Source ROI 설정 # Set Source ROI
		flfSourceROI = CFigureUtilities.ConvertFigureStringToObject("RG[D(129.22800000000007, 126.67680000000001), D(731.22800000000007, 120.67680000000001), D(733.22800000000007, 262.67680000000001), D(253.22800000000007, 246.67680000000001), D(265.22800000000007, 600.67679999999996), D(603.22800000000007, 594.67679999999996), D(607.22800000000007, 400.67680000000001), D(403.22800000000007, 396.67680000000001), D(409.22800000000007, 448.67680000000001), D(565.22800000000007, 450.67680000000001), D(549.22800000000007, 556.67679999999996), D(289.22800000000007, 558.67679999999996), D(291.22800000000007, 292.67680000000001), D(721.22800000000007, 294.67680000000001), D(721.22800000000007, 720.67679999999996), D(119.22800000000007, 718.67679999999996), D(113.22800000000007, 142.67680000000001)]")
		if (res := activeContour.SetSourceROI(flfSourceROI)).IsFail():
			break
		# Destination 이미지 설정 # Set destination image
		if (res := activeContour.SetDestinationImage(fliDstImage)[0]).IsFail():
			break
		# Point Count 설정 # Set Point Count
		if (res := activeContour.SetPointCount(3000)).IsFail():
			break
		# Max Length 설정 # Set Max Length
		if (res := activeContour.SetMaxLength(3)).IsFail():
			break
		# Low Threshold 설정 # Set Low Threshold
		if (res := activeContour.SetLowThreshold(20)).IsFail():
			break
		# High Threshold 설정 # Set High Threshold
		if (res := activeContour.SetHighThreshold(50)).IsFail():
			break
		# Fit Margin 설정 # Set Fit Margin
		if (res := activeContour.SetFitMargin(3)).IsFail():
			break

		# 알고리즘 수행 # Execute the algorithm
		if (res := (activeContour.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break

		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)

		for i32Iteration in range(0, 20):
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Fit()
			activeContour.Spacing()
			activeContour.Spacing()
			activeContour.Spacing()
			activeContour.Spacing()
			activeContour.Spacing()

			# Push Back Figures
			viewImageSrc.ClearFigureObject()
			viewImageSrc.PushBackFigureObject(activeContour.GetContourFigure())
			viewImageSrc.Invalidate(True)

			CThreadUtilities.Sleep(50)


		viewImageSrc.PushBackFigureObject(activeContour.GetSourceROI())
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		flpTemp = CFLPoint[Double](0, 0)
		if ((res := layerSrc.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		# 이미지 뷰를 Zoom fit # Zoom fit image view
		viewImageSrc.ZoomFit()
		viewImageDst.ZoomFit()

		# 이미지 뷰를 갱신 합니다. # Update image view
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