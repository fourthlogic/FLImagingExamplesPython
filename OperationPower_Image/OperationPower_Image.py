# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	listFliImage0 = [CFLImage(), CFLImage(), CFLImage()]
	listFliImage1 = [CFLImage(), CFLImage(), CFLImage()]

	# 이미지 뷰 선언 # Declare the image view
	listViewImage0 = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]
	listViewImage1 = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := listFliImage0[0].Load('../../ExampleImages/OperationPower/Sea3Ch.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Operand 이미지 로드 # Load the operand image
		if (res := listFliImage0[1].Load('../../ExampleImages/OperationPower/Gradation.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 로드 # Load the source image
		if (res := listFliImage1[0].Load('../../ExampleImages/OperationPower/Sea3ChF32.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Operand 이미지 로드 # Load the operand image
		if (res := listFliImage1[1].Load('../../ExampleImages/OperationPower/Gradation.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := listFliImage0[2].Assign(listFliImage0[0])).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := listFliImage1[2].Assign(listFliImage1[0])).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		# Source 이미지 뷰 생성 # Create source image view
		if (res := listViewImage0[0].Create(100, 0, 548, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Operand 이미지 뷰 생성 # Create operand image view
		if (res := listViewImage0[1].Create(548, 0, 996, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := listViewImage0[2].Create(996, 0, 1444, 448)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := listViewImage1[0].Create(100, 448, 548, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Operand 이미지 뷰 생성 # Create operand image view
		if (res := listViewImage1[1].Create(548, 448, 996, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := listViewImage1[2].Create(996, 448, 1444, 896)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := listViewImage0[0].SynchronizePointOfView(listViewImage0[1])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizePointOfView(listViewImage0[2])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizePointOfView(listViewImage1[0])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizePointOfView(listViewImage1[1])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizePointOfView(listViewImage1[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := listViewImage0[0].SynchronizeWindow(listViewImage0[1])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizeWindow(listViewImage0[2])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizeWindow(listViewImage1[0])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizeWindow(listViewImage1[1])[0]).IsFail() or \
			(res := listViewImage0[0].SynchronizeWindow(listViewImage1[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := listViewImage0[0].SetImagePtr(listFliImage0[0])[0]).IsFail() or \
			(res := listViewImage0[1].SetImagePtr(listFliImage0[1])[0]).IsFail() or \
			(res := listViewImage0[2].SetImagePtr(listFliImage0[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := listViewImage1[0].SetImagePtr(listFliImage1[0])[0]).IsFail() or \
			(res := listViewImage1[1].SetImagePtr(listFliImage1[1])[0]).IsFail() or \
			(res := listViewImage1[2].SetImagePtr(listFliImage1[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Operation Power 객체 생성 # Create Operation Power object
		operationPower = COperationPower()

		# Source 이미지 설정 # Set the source image
		operationPower.SetSourceImage(listFliImage0[0])
				
		# Operand 이미지 설정 # Set the operand image
		operationPower.SetOperandImage(listFliImage0[1])
		
		# Destination 이미지 설정 # Set the destination image
		operationPower.SetDestinationImage(listFliImage0[2])
		
		# 연산 방식 이미지로 설정 # Set operation source to image
		operationPower.SetOperationSource(EOperationSource.Image)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := operationPower.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# Source 이미지 설정 # Set the source image
		operationPower.SetSourceImage(listFliImage1[0])
				
		# Operand 이미지 설정 # Set the operand image
		operationPower.SetOperandImage(listFliImage1[1])
		
		# Destination 이미지 설정 # Set the destination image
		operationPower.SetDestinationImage(listFliImage1[2])
		
		# 연산 방식 이미지로 설정 # Set operation source to image
		operationPower.SetOperationSource(EOperationSource.Image)

		# Overflow Method Wrapping 옵션으로 설정 // Set Overflow Method to Wrapping option
		operationPower.SetOverflowMethod(EOverflowMethod.Wrapping)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := operationPower.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Power.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		listLayer0 = [listViewImage0[0].GetLayer(0), listViewImage0[1].GetLayer(0), listViewImage0[2].GetLayer(0)]
		listLayer1 = [listViewImage1[0].GetLayer(0), listViewImage1[1].GetLayer(0), listViewImage1[2].GetLayer(0)]

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		listLayer0[0].Clear()
		listLayer0[1].Clear()
		listLayer0[2].Clear()

		listLayer1[0].Clear()
		listLayer1[1].Clear()
		listLayer1[2].Clear()
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](5, 5)

		if  (res := listLayer0[0].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := listLayer0[1].DrawTextCanvas(flpPoint, 'Operand Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := listLayer0[2].DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := listLayer1[0].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := listLayer1[1].DrawTextCanvas(flpPoint, 'Operand Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := listLayer1[2].DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		listViewImage0[0].Invalidate(True)
		listViewImage0[1].Invalidate(True)
		listViewImage0[2].Invalidate(True)
		listViewImage1[0].Invalidate(True)
		listViewImage1[1].Invalidate(True)
		listViewImage1[2].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while listViewImage0[0].IsAvailable() and listViewImage0[1].IsAvailable() and listViewImage0[2].IsAvailable() and \
			listViewImage1[0].IsAvailable() and listViewImage1[1].IsAvailable() and listViewImage1[2].IsAvailable():
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
