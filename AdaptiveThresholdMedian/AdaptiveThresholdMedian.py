# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# 메인 함수 // Main function
def main():
    # 이미지 객체 선언 // Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
	viewImage = [CGUIViewImage(), CGUIViewImage()]

	while True:
		# 이미지 로드 // Load image

		if (res := fliSrcImage.Load("../../ExampleImages/Threshold/Sun.flif")).IsFail() :
			ErrorPrint(res, "Failed to load the image file.")
			break
		
		# 이미지 뷰 생성 // Create image view
		if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail() :
			ErrorPrint(res, "Failed to create the image view.")
			break
		
		if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail() :
			ErrorPrint(res, "Failed to create the image view.")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail() :
			ErrorPrint(res, "Failed to synchronize view")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail() :
			ErrorPrint(res, "Failed to synchronize window")
			break

		# 이미지 뷰에 이미지를 디스플레이 // Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SetImagePtr(fliSrcImage)[0]).IsFail() :
			ErrorPrint(res, "Failed to set image object on the image view.")
			break
		
		# 이미지 뷰에 이미지를 디스플레이 // Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[1].SetImagePtr(fliDstImage)[0]).IsFail() :
			ErrorPrint(res, "Failed to set image object on the image view.")
			break

		# Adaptive Threshold Median 객체 생성 // Create Adaptive Threshold Median object
		adaptiveThresholdMedian = CAdaptiveThresholdMedian()

		# Source 이미지 설정 // Set source image 
		adaptiveThresholdMedian.SetSourceImage(fliSrcImage)

		# Destination 이미지 설정 // Set destination image
		adaptiveThresholdMedian.SetDestinationImage(fliDstImage)

		# 커널 사이즈 입력 // Set Kernel size 
		adaptiveThresholdMedian.SetKernel(25, 25)

		# 임계값 옵셋 설정 // Set threshold offset 
		adaptiveThresholdMedian.SetThresholdOffset(CMultiVar[Double](5))

		# 알고리즘 수행 // Execute the algorithm
		if (res := (adaptiveThresholdMedian.Execute())).IsFail() :
			ErrorPrint(res, "Failed to execute AdaptiveThreshold.")
			break

		# 출력을 위한 이미지 레이어를 얻어옵니다. //  Gets the image layer for output.
		# 따로 해제할 필요 없음 // No need to release separately
		layer1 = viewImage[0].GetLayer(0)
		layer2 = viewImage[1].GetLayer(0)
		flpTemp = CFLPoint[Double](0, 0)

		# View 정보를 디스플레이 합니다. // Display View information.
		if (res := layer1.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
			ErrorPrint(res, "Failed to draw text.")
		
		if (res := layer2.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
			ErrorPrint(res, "Failed to draw text.")

		# 이미지 뷰를 갱신 합니다. // Update the image view.
		viewImage[0].Invalidate(True)
		viewImage[1].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		while(viewImage[0].IsAvailable() and viewImage[0].IsAvailable()) :
			CThreadUtilities.Sleep(1)        

		break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()