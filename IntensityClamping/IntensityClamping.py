
# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	arrFliImage = [CFLImage() for _ in range(2)]

    # 이미지 뷰 선언 // Declare the image view
	arrViewImage = [CGUIViewImage() for _ in range(2)]

	while True:
		
		# Source 이미지 로드 // Load the source image
		res = arrFliImage[0].Load("../../ExampleImages/IntensityClamping/Color.flif")
		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := arrFliImage[1].Assign(arrFliImage[0])).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := arrViewImage[0].Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := arrViewImage[1].Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the three image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := arrViewImage[0].SetImagePtr(arrFliImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := arrViewImage[1].SetImagePtr(arrFliImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1])[0]).IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break

		# Intensity Clamping 객체 생성 // Create Intensity Clamping object
		IntensityClamping = CIntensityClamping()

		# Source 이미지 설정 // Set the source image
		IntensityClamping.SetSourceImage(arrFliImage[0])
		# Destination 이미지 설정 // Set the destination image
		IntensityClamping.SetDestinationImage(arrFliImage[1])

		# IntensityClamping Scalar 값 설정 // Set comparsion value of IntensityClamping operation
		mvMinScalar = CMultiVar[Double](150, 150, 150)
		mvMaxScalar = CMultiVar[Double](200, 200, 200)
		IntensityClamping.SetIntensity(mvMinScalar, mvMaxScalar)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := IntensityClamping.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Intensity Clamping.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		arrLayer = [CGUIViewImageLayer() for _ in range(2)]
		
		for i in range(2):
			arrLayer[i] = arrViewImage[i].GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		for layer in arrLayer:
			layer.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := arrLayer[0].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := arrLayer[1].DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		for viewImage in arrViewImage:
			viewImage.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while arrViewImage[0].IsAvailable() and arrViewImage[0].IsAvailable():
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