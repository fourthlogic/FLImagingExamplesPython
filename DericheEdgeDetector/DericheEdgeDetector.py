# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():
	CLibraryUtilities.Initialize()

	# 이미지 객체 선언 // Declare the image object
	fliISrcImage = CFLImage()
	fliIDstImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImage = [CGUIViewImage() for i in range(2)]

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliISrcImage.Load('../../ExampleImages/DericheEdgeDetector/Circuit Board.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := fliIDstImage.Assign(fliISrcImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[1].SetImagePtr(fliIDstImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 객체 생성 // Create object
		Deriche = CDericheEdgeDetector()

		# Source 이미지 설정 // Set the source image
		Deriche.SetSourceImage(fliISrcImage)

		# Destination 이미지 설정 // Set the destination image
		Deriche.SetDestinationImage(fliIDstImage)

		# 이미지 전처리 Smoothing/Normal 설정 / Set Image Preprocessing Mode Smoothing/Normal
		Deriche.SetConvolutionMode(CDericheEdgeDetector.EConvolutionMode.Normal)

		# Threshold 설정 // Set threshold value
		mvThresholdValue = CMultiVar[Double](20, 25)
		Deriche.SetThreshold(mvThresholdValue)
		
		# Alpha 값 설정 // Set alpha value
		Deriche.SetAlpha(1.0)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := Deriche.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSrc = viewImage[0].GetLayer(0)
		layerDst = viewImage[1].GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSrc.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerDst.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImage[0].Invalidate(True)
		viewImage[1].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImage[0].IsAvailable() and viewImage[1].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()