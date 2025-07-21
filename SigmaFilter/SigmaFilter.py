# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

class EType(Enum):
	Source = 0
	Destination1 = 1
	Destination2 = 2
	ETypeCount = 3

# 메인 함수 // Main function
def main():

	arrFliImage = []
	arrViewImage = []

	for i in range(EType.ETypeCount):
		# 이미지 객체 선언 // Declare the image object
		arrFliImage.append(CFLImage())

	for i in range(EType.ETypeCount):
		# 이미지 객체 선언 // Declare the image object
		arrViewImage.append(CGUIViewImage())

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := arrFliImage[EType.Source].Load('../../ExampleImages/NoiseImage/NoiseImage1.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination1 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination1 image as same as source image
		if (res := arrFliImage[EType.Destination1].Assign(arrFliImage[EType.Source])).IsFail():
			ErrorPrint(res, 'Failed to assign the image file.')
			break

		# Destination2 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination2 image as same as source image
		if (res := arrFliImage[EType.Destination2].Assign(arrFliImage[EType.Source])).IsFail():
			ErrorPrint(res, 'Failed to assign the image file.')
			break

		bError = False

		for i in range(EType.ETypeCount):
			# 이미지 뷰 생성 // Create image view
			if (res := arrViewImage[i].Create(i * 570 + 100, 0, i * 570 + 100 + 570, 427)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				break

			# 이미지 뷰에 이미지를 디스플레이 // Display the image in the image view
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				break

			if i == EType.Source:
				continue

			# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := arrViewImage[EType.Source].SynchronizePointOfView(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view.')
				break

			# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				break

		if bError:
			break

		# 객체 생성 // Create object
		sigmaFilter = CSigmaFilter()

		# Source 이미지 설정 // Set the source image
		sigmaFilter.SetSourceImage(arrFliImage[EType.Source])

		# Destination 이미지 설정 // Set the destination image
		sigmaFilter.SetDestinationImage(arrFliImage[EType.Destination1])

		# Kernel Size = 31 설정 // Set the Kernel Size = 31
		sigmaFilter.SetKernel(31)

		# Sigma = 3 설정 // Set the Sigma = 3
		sigmaFilter.SetSigma(3);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := sigmaFilter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# Destination 이미지를 Destination2로 설정 // Set destination image to destination2
		sigmaFilter.SetDestinationImage(arrFliImage[EType.Destination2])

		# Kernel Size = 101 설정 // Set the Kernel Size = 101
		sigmaFilter.SetKernel(101)

		# Sigma = 3 설정 // Set the Sigma = 3
		sigmaFilter.SetSigma(3);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := sigmaFilter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		arrLayer = []

		for i in range(EType.ETypeCount):
			arrLayer.append(CGUIViewImageLayer())

		for i in range(EType.ETypeCount):
			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
			arrLayer[i] = arrViewImage[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
			arrLayer[i].Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := arrLayer[EType.Source].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination1].DrawTextCanvas(flpPoint, 'SigmaFilter Size : 31x31 Sigma: 3', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination2].DrawTextCanvas(flpPoint, 'SigmaFilter Size : 101x101 Sigma: 3', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		for i in range(EType.ETypeCount):
			# 이미지 뷰를 갱신 // Update image view
			arrViewImage[i].Invalidate(True)
		
		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to exit
		bAvailable = True

		while bAvailable:
			for i in range(EType.ETypeCount):
				bAvailable = arrViewImage[i].IsAvailable()

				if bAvailable:
					break

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
