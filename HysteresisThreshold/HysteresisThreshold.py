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
	
	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/Threshold/Checker Board_1Ch.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSrc.Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		if (res := viewImageDst.Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		
		# 알고리즘 객체 생성 # Create algorithm object
		ht = CHysteresisThreshold()

		# Source 이미지 설정 # Set source image 
		if (res := ht.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# Destination 이미지 설정 # Set destination image
		if (res := ht.SetDestinationImage(fliDstImage)[0]).IsFail():
			break
		# Max Length 설정 # Set Max Length
		if (res := ht.SetMaxLength(100)).IsFail():
			break
		# Output Mode 설정 # Set Output Mode
		if (res := ht.SetOutputMode(CHysteresisThreshold.EOutputMode.Binary)).IsFail():
			break
		# Logical Condition Of Channels 설정 # Set Logical Condition Of Channels
		if (res := ht.SetLogicalConditionOfChannels(ELogicalConditionOfChannels.And)).IsFail():
			break
		# Low Threshold 설정 # Set Low Threshold
		mvLowThreshold = CMultiVar[Double](110)
		if (res := ht.SetLowThreshold(mvLowThreshold)).IsFail():
			break
		# High Threshold 설정 # Set High Threshold
		mvHighThreshold = CMultiVar[Double](190)
		if (res := ht.SetHighThreshold(mvHighThreshold)).IsFail():
			break

		# 알고리즘 수행 # Execute the algorithm
		if (res := (ht.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break

		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		flpTemp = CFLPoint[Double](0, 0)
		if (res := layerSrc.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := layerDst.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
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