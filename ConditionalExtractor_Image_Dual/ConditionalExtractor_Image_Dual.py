# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	class EType:
		Source = 0
		Operand1 = 1
		Operand2 = 2
		Destination = 3
		ETypeCount = 4

	# 이미지 객체 선언 # Declare the image object
	arrFliImage = [CFLImage() for i in range(EType.ETypeCount)]

	# 이미지 뷰 선언 # Declare the image view
	arrViewImage = [CGUIViewImage() for i in range(EType.ETypeCount)]

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := arrFliImage[EType.Source].Load('../../ExampleImages/ConditionalExtractor/CatSource.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Operand1 이미지 로드 # Load the operand1 image
		if (res := arrFliImage[EType.Operand1].Load('../../ExampleImages/ConditionalExtractor/CatOperandDual1.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Operand2 이미지 로드 # Load the operand2 image
		if (res := arrFliImage[EType.Operand2].Load('../../ExampleImages/ConditionalExtractor/CatOperandDual2.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination2 image as same as source image
		if (res := arrFliImage[EType.Destination].Assign(arrFliImage[EType.Source])).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		bError = False

		for i in range(EType.ETypeCount):

			#이미지 뷰 생성 # Create image view
			if (res := arrViewImage[i].Create(i * 448 + 100, 0, i * 448 + 100 + 448, 448)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				bError = True
				break

			# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				bError = True
				break

			if i == EType.Source:
				continue

			# 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the image views
			if (res := arrViewImage[EType.Source].SynchronizePointOfView(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view.')
				bError = True
				break

			# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
			if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				bError = True
				break

		if bError:
			break

		# 객체 생성 # Create object
		conditionalExtractor = CConditionalExtractor()

		# Source 이미지 설정 # Set the source image
		conditionalExtractor.SetSourceImage(arrFliImage[EType.Source])

		# Operand1 이미지 설정 # Set the operand1 image
		conditionalExtractor.SetOperandImage(arrFliImage[EType.Operand1])

		# Operand2 이미지 설정 # Set the operand2 image
		conditionalExtractor.SetOperandImage2(arrFliImage[EType.Operand2])

		# Destination 이미지 설정 # Set the destination image
		conditionalExtractor.SetDestinationImage(arrFliImage[EType.Destination])

		# 연산 방식 설정 # Set the operation source
		conditionalExtractor.SetOperationSource(EOperationSource.Image)

		# Threshold Mode 설정 # Set the threshold mode
		conditionalExtractor.SetThresholdMode(EThresholdMode.Dual_Or)

		# 논리조건 설정 # Set the logical condition
		conditionalExtractor.SetLogicalCondition(ELogicalCondition.Greater)
		conditionalExtractor.SetLogicalCondition(ELogicalCondition.Equal, EThresholdIndex.Second)

		# 조건이 거짓일 경우 Out of Range 값 설정 여부 결정 # Determine the Out of Range value if the condition is false
		conditionalExtractor.EnableOutOfRange(True)

		# 조건이 거짓일 경우 Out of range 값 설정하기 위한 MultiVar 객체 생성 # Create the MultiVar object that sets the Out of Range value if the condition is false
		mvOutOfRange = CMultiVar[Double](0, 0, 0)

		# Out of Range 값 설정 # Set Out of Range value
		conditionalExtractor.SetOutOfRangeValue(mvOutOfRange)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := conditionalExtractor.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Conditional Extractor.')
			break
		
		arrLayer = [CGUIViewImageLayer() for i in range(EType.ETypeCount)]

		for i in range(EType.ETypeCount):

			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
			arrLayer[i] = arrViewImage[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
			arrLayer[i].Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := arrLayer[EType.Source].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Operand1].DrawTextCanvas(flpPoint, 'Operand1 Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Operand2].DrawTextCanvas(flpPoint, 'Operand2 Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination].DrawTextCanvas(flpPoint, 'Destination Image\nDual Or(Greater, Equal)', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		[arrViewImage[i].Invalidate(True) for i in range(EType.ETypeCount)]

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
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