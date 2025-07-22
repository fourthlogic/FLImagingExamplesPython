# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# 메인 함수 // Main function
def main():

	class EType:
		Source = 0
		Operand = 1
		Destination = 2
		ETypeCount = 3

	# 이미지 객체 선언 // Declare the image object
	arrFliImage = [CFLImage() for i in range(EType.ETypeCount)]

	# 이미지 뷰 선언 // Declare the image view
	arrViewImage = [CGUIViewImage() for i in range(EType.ETypeCount)]

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := arrFliImage[EType.Source].Load('../../ExampleImages/OperationGreatestCommonDivisor/Sunset.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Operand 이미지 로드 // Load the operand image
		if (res := arrFliImage[EType.Operand].Load('../../ExampleImages/OperationGreatestCommonDivisor/palmtree.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := arrFliImage[EType.Destination].Assign(arrFliImage[EType.Source])).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		bError = False

		for i in range(EType.ETypeCount) :

			#이미지 뷰 생성 // Create image view
			if (res := arrViewImage[i].Create(i * 512 + 100, 0, i * 512 + 100 + 512, 512)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				bError = True
				break

			# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				bError = True
				break

			if i == EType.Source :
				continue

			# 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the image views
			if (res := arrViewImage[EType.Source].SynchronizePointOfView(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view.')
				bError = True
				break

			# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
			if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				bError = True
				break

		if bError :
			break

		# ROI 설정을 위한 CFLRect 객체 생성 // Create a CFLRect object for setting ROI
		flrROI = CFLRect[int](200, 200, 500, 500)

		# 객체 생성 // Create object
		gcd = COperationGreatestCommonDivisor()

		# Source 이미지 설정 // Set the source image
		gcd.SetSourceImage(arrFliImage[EType.Source])

		# Source ROI 설정 // Set the source ROI
		gcd.SetSourceROI(flrROI)

		# Operand 이미지 설정 // Set the operand image
		gcd.SetOperandImage(arrFliImage[EType.Operand])

		# Operand ROI 설정 // Set the operand ROI
		gcd.SetOperandROI(flrROI)

		# Destination 이미지 설정 // Set the destination image
		gcd.SetDestinationImage(arrFliImage[EType.Destination])

		# Destination ROI 설정 // Set Destination ROI
		gcd.SetDestinationROI(flrROI)

		# 연산 방식 설정 // Set the operation source
		gcd.SetOperationSource(EOperationSource.Image)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := gcd.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute operation GCD.')
			break

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := gcd.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		arrLayer = [CGUIViewImageLayer() for i in range(EType.ETypeCount)]

		for i in range(EType.ETypeCount) :

			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
			arrLayer[i] = arrViewImage[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
			arrLayer[i].Clear()

			# ROI 영역을 디스플레이 한다 // Display ROI
			# FLImaging의 Figure 객체들은 도형 모향에 상관없이 하나의 함수로 디스플레이가 가능 // FLimaging's Figure objects can be displayed with one function regardless of the shape
			# 아래 함수 DrawFigureImage는 Image 좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 // The function DrawFigureImage below means drawing a picture based on the image coordinates
			# 마지막 두 개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. // The last two parameters are opacity values, which mean opacity for 1 and complete transparency for 0.
			# 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) // Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
			if (res := arrLayer[i].DrawFigureImage(flrROI, EColor.LIME)).IsFail():
				ErrorPrint(res, "Falied to draw figure.")

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := arrLayer[EType.Source].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Operand].DrawTextCanvas(flpPoint, 'Operand Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination].DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
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

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

if __name__ == '__main__':
    main()