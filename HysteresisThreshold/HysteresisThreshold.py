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
		if (res := fliISrcImage.Load("../../ExampleImages/Threshold/Checker Board_1Ch.flif")).IsFail():
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

		# Hysteresis Threshold 객체 생성 # Create Hysteresis Threshold object
		ht = CHysteresisThreshold()

		# Source 이미지 설정 # Set source image 
		ht.SetSourceImage(fliISrcImage)

		# Destination 이미지 설정 # Set destination image
		ht.SetDestinationImage(fliIDstImage)

		# Max Length 설정 # Set Max Length
		ht.SetMaxLength(100)

		# Output Mode 설정 # Set Output Mode
		ht.SetOutputMode(CHysteresisThreshold.EOutputMode.Binary)

		# Logical Condition Of Channels 설정 # Set Logical Condition Of Channels
		ht.SetLogicalConditionOfChannels(ELogicalConditionOfChannels.And)

		# Low Threshold 설정 # Set Low Threshold
		mvLowThreshold = CMultiVar[Double](110)
		ht.SetLowThreshold(mvLowThreshold)

		# High Threshold 설정 # Set High Threshold
		mvHighThreshold = CMultiVar[Double](190)
		ht.SetHighThreshold(mvHighThreshold)

		# 알고리즘 수행 # Execute the algorithm
		if (res := (ht.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Hysteresis Threshold.")
			break


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