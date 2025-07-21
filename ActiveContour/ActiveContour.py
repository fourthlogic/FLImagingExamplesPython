# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	
	# 이미지 객체 선언 # Declare the image object
	fliISrcImage = CFLImage()
	fliIDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = List[CGUIViewImage]()
	viewImage.Add(CGUIViewImage())
	viewImage.Add(CGUIViewImage())

	while True:
		res = CResult()

		# 이미지 로드 # Load image
		if (res := fliISrcImage.Load("../../ExampleImages/ActiveContour/Grid Of Cross.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. 
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize view\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		if (res := viewImage[0].SynchronizeWindow(viewImage[1]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize window\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImage[0].SetImagePtr(fliISrcImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImage[1].SetImagePtr(fliIDstImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# Active Contour 객체 생성 # Create Active Contour object
		ac = CActiveContour()

		# Source 이미지 설정 # Set source image 
		ac.SetSourceImage(fliISrcImage)

		# Source ROI 설정 # Set Source ROI
		flfSourceROI = CFigureUtilities.ConvertFigureStringToObject("RG[D(129.22800000000007, 126.67680000000001), D(731.22800000000007, 120.67680000000001), D(733.22800000000007, 262.67680000000001), D(253.22800000000007, 246.67680000000001), D(265.22800000000007, 600.67679999999996), D(603.22800000000007, 594.67679999999996), D(607.22800000000007, 400.67680000000001), D(403.22800000000007, 396.67680000000001), D(409.22800000000007, 448.67680000000001), D(565.22800000000007, 450.67680000000001), D(549.22800000000007, 556.67679999999996), D(289.22800000000007, 558.67679999999996), D(291.22800000000007, 292.67680000000001), D(721.22800000000007, 294.67680000000001), D(721.22800000000007, 720.67679999999996), D(119.22800000000007, 718.67679999999996), D(113.22800000000007, 142.67680000000001)]")
		ac.SetSourceROI(flfSourceROI)

		# Destination 이미지 설정 # Set destination image
		ac .SetDestinationImage(fliIDstImage)

		# Point Count 설정 # Set Point Count
		ac.SetPointCount(3000)

		# Max Length 설정 # Set Max Length
		ac.SetMaxLength(3)

		# Low Threshold 설정 # Set Low Threshold
		ac.SetLowThreshold(20)

		# High Threshold 설정 # Set High Threshold
		ac.SetHighThreshold(50)

		# Fit Margin 설정 # Set Fit Margin
		ac.SetFitMargin(3)

		# 알고리즘 수행 # Execute the algorithm
		if (res := (ac.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Active Contour.")
			break


		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImage[0].Invalidate(True)
		viewImage[1].Invalidate(True)

		for i32Iteration in range(0, 20):
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Fit()
			ac.Spacing()
			ac.Spacing()
			ac.Spacing()
			ac.Spacing()
			ac.Spacing()

			# Push Back Figures
			viewImage[0].ClearFigureObject()
			viewImage[0].PushBackFigureObject(ac.GetContourFigure())
			viewImage[0].Invalidate(True)

			CThreadUtilities.Sleep(50)


		viewImage[0].PushBackFigureObject(ac.GetSourceROI())

		# 레이어는 따로 해제하지 않아도 View가 해제 될 때 같이 해제된다. # The layer is released together when View is released without releasing it separately.
		layer1 = viewImage[0].GetLayer(0)
		layer2 = viewImage[1].GetLayer(0)
		flpTemp = CFLPoint[Double](0, 0)

		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layer1.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")

		if (res := layer2.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")


		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImage[0].Invalidate(True)
		viewImage[1].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImage[0].IsAvailable():			
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