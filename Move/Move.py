# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	class EType:
		Source = 0
		Destination = 1
		ETypeCount = 2

	# 이미지 객체 선언 // Declare the image object
	arrFliImage = [CFLImage() for _ in range(EType.ETypeCount)]

	# 이미지 뷰 선언 // Declare the image view
	arrViewImage = [CGUIViewImage() for _ in range(EType.ETypeCount)]

	while True:

		# Source 이미지 로드 // Load image
		if (res := arrFliImage[EType.Source].Load('../../ExampleImages/Affine/Generator.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := arrFliImage[EType.Destination].Assign(arrFliImage[EType.Source])).IsFail():
			ErrorPrint(res, 'Failed to assign the image file.')
			break

		bError = False

		for i in range(EType.ETypeCount):
			x = i % 2
			y = i // 2

			# 이미지 뷰 생성 // Create image view
			if (res := arrViewImage[i].Create(x * 400 + 400, y * 400, x * 400 + 400 + 400, y * 400 + 400)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				bError = True
				break

			# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				bError = True
				break

			if i == EType.Source:
				continue

			# 시점 동기화 // Synchronize view
			if (res := arrViewImage[EType.Source].SynchronizePointOfView(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view.')
				bError = True
				break

			# 윈도우 위치 동기화 // Synchronize window
			if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				bError = True
				break

		if bError:
			break

		# ROI 설정을 위한 객체 생성 // Create ROI
		fleROI = CFLEllipse[Double](370, 260, 100, 50, 34)

		# Move 객체 생성 // Create Move object
		move = CMove()
		# Source 이미지 설정 // Set the source image
		move.SetSourceImage(arrFliImage[EType.Source])
		# Source ROI 설정 // Set the Source ROI
		move.SetSourceROI(fleROI)
		# Destination 이미지 설정 // Set the destination image
		move.SetDestinationImage(arrFliImage[EType.Destination])
		# Destination ROI 설정 // Set Destination ROI
		move.SetDestinationROI(fleROI)
		# 이동할 크기 설정 // Set movement parameter
		move.SetMovement(15.0, 15.0)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := move.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute move.')
			break

		# 레이어 객체 가져오기 // Get layers
		arrLayer = [arrViewImage[i].GetLayer(0) for i in range(EType.ETypeCount)]

		for i in range(EType.ETypeCount):
			arrLayer[i].Clear()

			# ROI 디스플레이 // Display ROI
			if (res := arrLayer[i].DrawFigureImage(fleROI, EColor.LIME)).IsFail():
				ErrorPrint(res, 'Failed to draw figure.')

		# 텍스트 디스플레이 // Display text
		flpZero = CFLPoint[Double](0, 0)

		if (res := arrLayer[EType.Source].DrawTextCanvas(flpZero, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination].DrawTextCanvas(flpZero, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 // Update image view
		[arrViewImage[i].Invalidate(True) for i in range(EType.ETypeCount)]

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		bAvailable = True

		while bAvailable :
			for i in range(EType.ETypeCount) :
				bAvailable = arrViewImage[i].IsAvailable()

				if bAvailable == False :
					break

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