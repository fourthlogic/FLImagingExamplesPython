# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():
	CLibraryUtilities.Initialize()

	# 이미지 객체 선언 # Declare the image object
	listFliImage = [CFLImage(), CFLImage(), CFLImage(), CFLImage(), CFLImage(), CFLImage()]

	# 이미지 뷰 선언 # Declare the image view
	listViewImage = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := listFliImage[0].Load('../../ExampleImages/OperationPower/Space3Ch.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination1 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination1 image as same as source image
		if (res := listFliImage[1].Assign(listFliImage[0])).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# Destination2 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination2 image as same as source image
		if (res := listFliImage[2].Assign(listFliImage[0])).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# Destination3 로드 # Load the destination3 image
		if (res := listFliImage[3].Load('../../ExampleImages/OperationPower/Dst16Depth.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination4 로드 # Load the destination4 image
		if (res := listFliImage[4].Load('../../ExampleImages/OperationPower/Dst16Depth.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination5 로드 # Load the destination5 image
		if (res := listFliImage[5].Load('../../ExampleImages/OperationPower/Dst64Depth.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Source 이미지 뷰 생성 # Create source image view
		if (res := listViewImage[0].Create(100, 0, 548, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Operand 이미지 뷰 생성 # Create operand image view
		if (res := listViewImage[1].Create(548, 0, 996, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := listViewImage[2].Create(996, 0, 1444, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := listViewImage[3].Create(100, 448, 548, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Operand 이미지 뷰 생성 # Create operand image view
		if (res := listViewImage[4].Create(548, 448, 996, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := listViewImage[5].Create(996, 448, 1444, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := listViewImage[0].SynchronizePointOfView(listViewImage[1]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizePointOfView(listViewImage[2]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizePointOfView(listViewImage[3]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizePointOfView(listViewImage[4]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizePointOfView(listViewImage[5]))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := listViewImage[0].SynchronizeWindow(listViewImage[1]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizeWindow(listViewImage[2]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizeWindow(listViewImage[3]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizeWindow(listViewImage[4]))[0].IsFail() or \
			(res := listViewImage[0].SynchronizeWindow(listViewImage[5]))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := listViewImage[0].SetImagePtr(listFliImage[0]))[0].IsFail() or \
			(res := listViewImage[1].SetImagePtr(listFliImage[1]))[0].IsFail() or \
			(res := listViewImage[2].SetImagePtr(listFliImage[2]))[0].IsFail() or \
			(res := listViewImage[3].SetImagePtr(listFliImage[3]))[0].IsFail() or \
			(res := listViewImage[4].SetImagePtr(listFliImage[4]))[0].IsFail() or \
			(res := listViewImage[5].SetImagePtr(listFliImage[5]))[0].IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		mvScalr1 = CMultiVar[Double](1.1, 1.2, 1.5)
		mvScalr2 = CMultiVar[Double](0.8, 0.8, 1.1)
		mvScalr3 = CMultiVar[Double](2.5, 2.5, 2.5)
		mvScalr4 = CMultiVar[Double](2.5, 2.5, 2.5)
		mvScalr5 = CMultiVar[Double](10, 10, 10)
		
		# Operation Power 객체 생성 # Create Operation scaled divide object
		power = COperationPower()

		# Source 이미지 설정 # Set the source image
		power.SetSourceImage(listFliImage[0])
		
		# Destination 이미지 설정 # Set the destination image
		power.SetDestinationImage(listFliImage[1])
		
		# Overflow Method Clamping 옵션으로 설정 // Set Overflow Method to Clamping option
		power.SetOverflowMethod(EOverflowMethod.Clamping)

		# 연산 방식 이미지로 설정 # Set operation source to image
		power.SetOperationSource(EOperationSource.Scalar)
		
		# Exponent 값 설정 // Set Exponent value
		power.SetScalarValue(mvScalr1)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := power.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# Destination 이미지 설정 # Set the destination image
		power.SetDestinationImage(listFliImage[2])
		
		# Overflow Method Clamping 옵션으로 설정 // Set Overflow Method to Clamping option
		power.SetOverflowMethod(EOverflowMethod.Clamping)

		# Exponent 값 설정 // Set Exponent value
		power.SetScalarValue(mvScalr2)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := power.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# Destination 이미지 설정 # Set the destination image
		power.SetDestinationImage(listFliImage[3])
		
		# Overflow Method Wrapping 옵션으로 설정 // Set Overflow Method to Wrapping option
		power.SetOverflowMethod(EOverflowMethod.Wrapping)

		# Exponent 값 설정 // Set Exponent value
		power.SetScalarValue(mvScalr3)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := power.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# Destination 이미지 설정 # Set the destination image
		power.SetDestinationImage(listFliImage[4])
		
		# Overflow Method Clamping 옵션으로 설정 // Set Overflow Method to Clamping option
		power.SetOverflowMethod(EOverflowMethod.Clamping)

		# Exponent 값 설정 // Set Exponent value
		power.SetScalarValue(mvScalr4)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := power.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# Destination 이미지 설정 # Set the destination image
		power.SetDestinationImage(listFliImage[5])
		
		# Overflow Method Clamping 옵션으로 설정 // Set Overflow Method to Clamping option
		power.SetOverflowMethod(EOverflowMethod.Wrapping)

		# Exponent 값 설정 // Set Exponent value
		power.SetScalarValue(mvScalr5)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := power.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		listLayer = [listViewImage[0].GetLayer(0), listViewImage[1].GetLayer(0), listViewImage[2].GetLayer(0), listViewImage[3].GetLayer(0), listViewImage[4].GetLayer(0), listViewImage[5].GetLayer(0)]

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		listLayer[0].Clear()
		listLayer[1].Clear()
		listLayer[2].Clear()
		listLayer[3].Clear()
		listLayer[4].Clear()
		listLayer[5].Clear()
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint1 = CFLPoint[Double](5, 0)
		flpPoint2 = CFLPoint[Double](5, 22)

		if  (res := listLayer[0].DrawTextCanvas(flpPoint1, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := listLayer[1].DrawTextCanvas(flpPoint1, 'Destination 1 Image(Power 1.1, 1.2, 1.5)', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := listLayer[1].DrawTextCanvas(flpPoint2, 'Unsigned Int / 8 / Clamping', EColor.YELLOW, EColor.BLACK, 15)).IsFail() or \
			(res := listLayer[2].DrawTextCanvas(flpPoint1, 'Destination2 Image(Power 0.8, 0.8, 1.1)', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := listLayer[2].DrawTextCanvas(flpPoint2, 'Unsigned Int / 8 / Clamping', EColor.YELLOW, EColor.BLACK, 15)).IsFail() or \
			(res := listLayer[3].DrawTextCanvas(flpPoint1, 'Destination3 Image(Power 2.5, 2.5, 2.5)', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := listLayer[3].DrawTextCanvas(flpPoint2, 'Unsigned Int / 16 / Wrapping', EColor.YELLOW, EColor.BLACK, 15)).IsFail() or \
			(res := listLayer[4].DrawTextCanvas(flpPoint1, 'Destination 4 Image(Power 2.5, 2.5, 2.5)', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := listLayer[4].DrawTextCanvas(flpPoint2, 'Unsigned Int / 16 / Clamping', EColor.YELLOW, EColor.BLACK, 15)).IsFail() or \
			(res := listLayer[5].DrawTextCanvas(flpPoint1, 'Destination 5 Image(Power 10, 10, 10)', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := listLayer[5].DrawTextCanvas(flpPoint2, 'Unsigned Int / 64 / Wrapping', EColor.YELLOW, EColor.BLACK, 15)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		listViewImage[0].Invalidate(True)
		listViewImage[1].Invalidate(True)
		listViewImage[2].Invalidate(True)
		listViewImage[3].Invalidate(True)
		listViewImage[4].Invalidate(True)
		listViewImage[5].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while listViewImage[0].IsAvailable() and listViewImage[1].IsAvailable() and listViewImage[2].IsAvailable() and \
			listViewImage[3].IsAvailable() and listViewImage[4].IsAvailable() and listViewImage[5].IsAvailable():
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
