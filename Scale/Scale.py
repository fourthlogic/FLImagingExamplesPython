# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	class EType:
		Source = 0
		Destination1 = 1
		Destination2 = 2
		Destination3 = 3
		ETypeCount = 4

	# 이미지 객체 선언 // Declare the image object
	arrFliImage = [CFLImage() for i in range(EType.ETypeCount)]

	# 이미지 뷰 선언 // Declare the image view
	arrViewImage = [CGUIViewImage() for i in range(EType.ETypeCount)]

	while True:

		bError = False

		# 이미지 로드 // Load image
		if (res := arrFliImage[EType.Source].Load('../../ExampleImages/Affine/Sea.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지로 복사 // Copy Source to Destination images
		for i in range(EType.Destination1, EType.ETypeCount):
			if (res := arrFliImage[i].Assign(arrFliImage[EType.Source])).IsFail():
				ErrorPrint(res, 'Failed to assign the image file.')
				bError = True
				break
		
		if bError:
			break

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

			if i != EType.Source:
				# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
				if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail():
					ErrorPrint(res, 'Failed to synchronize window.')
					bError = True
					break

		if bError:
			break

		# Scale 객체 생성 // Create Scale object
		scale = CScale()
		# Source 이미지 설정 // Set the source image
		scale.SetSourceImage(arrFliImage[EType.Source])
		# Destination 이미지 설정 // Set the destination image
		scale.SetDestinationImage(arrFliImage[EType.Destination1])
		# Scale 변환 방식 비율로 설정 // Set to scale conversion method ratio
		scale.SetScaleMethod(EScaleMethod.Ratio)
		# Scale 비율 설정 // set scale ratio
		scale.SetScale(1.5, 1.5)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := scale.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute scale.')
			break

		# Destination 이미지 설정 // Set the destination image
		scale.SetDestinationImage(arrFliImage[EType.Destination2])
		# Scale 변환 방식 비율로 설정 // Set to scale conversion method ratio
		scale.SetScaleMethod(EScaleMethod.Ratio)
		# Scale 비율 설정 // set scale ratio
		scale.SetScale(1.5, 1.5)
		# Image Resize 설정 // Set Image Resize
		scale.SetResizeMethod(EResizeMethod.Resize)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := scale.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute scale.')
			break

		# Destination 이미지 설정 // Set the destination image
		scale.SetDestinationImage(arrFliImage[EType.Destination3])
		# Scale 변환 방식 픽셀로 설정 // Scale conversion method set to pixel
		scale.SetScaleMethod(EScaleMethod.ScaleUnitsToPixels)
		# Scale 변환 크기 설정 // Set the Scale transform size
		scale.SetScale(1024, 1024)
		# Image Resize 설정 // Set Image Resize
		scale.SetResizeMethod(EResizeMethod.Resize)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := scale.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute scale.')
			break
		
		# 레이어 객체 가져오기 // Get layers
		arrLayer = [arrViewImage[i].GetLayer(0) for i in range(EType.ETypeCount)]

		for i in range(EType.ETypeCount):
			arrLayer[i].Clear()

		# 텍스트 디스플레이 // Draw text for view info
		flpZero = CFLPoint[Double](0, 0)

		if (res := arrLayer[EType.Source].DrawTextCanvas(flpZero, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := arrLayer[EType.Destination1].DrawTextCanvas(flpZero, 'Destination1 Image (x1.5)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination2].DrawTextCanvas(flpZero, 'Destination2 Image (x1.5 Resize)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination3].DrawTextCanvas(flpZero, 'Destination3 Image (1024x1024 Resize)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 뷰 갱신 및 ZoomFit // Refresh and zoom fit
		for i in range(EType.ETypeCount):
			arrViewImage[i].ZoomFit()
			arrViewImage[i].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		bAvailable = True
		while bAvailable:
			for i in range(EType.ETypeCount):
				bAvailable = arrViewImage[i].IsAvailable()
				if not bAvailable:
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