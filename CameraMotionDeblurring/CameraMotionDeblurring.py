# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	arrFliImage = [CFLImage() for i in range(2)]

	# 이미지 뷰 선언 # Declare the image view
	arrViewImage = [CGUIViewImage() for i in range(2)]

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := arrFliImage[0].Load('../../ExampleImages/CameraMotionDeblurring/CircuitBlur.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := arrFliImage[1].Assign(arrFliImage[0])).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := arrViewImage[0].Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := arrViewImage[1].Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		bError = False

		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		for i in range(2):
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				break

		if bError:
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 객체 생성 # Create object
		cameraMotionDeblurring = CCameraMotionDeblurring()

		# Source 이미지 설정 # Set the source image
		cameraMotionDeblurring.SetSourceImage(arrFliImage[0])

		# Destination 이미지 설정 # Set the destination image
		cameraMotionDeblurring.SetDestinationImage(arrFliImage[1])

		# Mode 설정 # Set Mode
		cameraMotionDeblurring.EnableWithEstimation(True)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := cameraMotionDeblurring.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		arrLayer = [CGUIViewImageLayer() for i in range(2)]

		for i in range(2):
			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
			arrLayer[i] = arrViewImage[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
			arrLayer[i].Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := arrLayer[0].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[1].DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		arrViewImage[0].Invalidate(True)
		arrViewImage[1].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while arrViewImage[0].IsAvailable() and arrViewImage[1].IsAvailable():
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