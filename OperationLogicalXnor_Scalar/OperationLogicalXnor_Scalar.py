
# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestination1Image = CFLImage()
	fliDestination2Image = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst1 = CGUIViewImage()
	viewImageDst2 = CGUIViewImage()

	while True:
				
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/OperationLogicalXnor/Cat.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 1 이미지 뷰 생성 # Create the destination 1 image view
		if (res := viewImageDst1.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Destination 2 이미지 뷰 생성 # Create the destination 2 image view
		if (res := viewImageDst2.Create(1124, 0, 1636, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 1 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination 1 image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst1.SetImagePtr(fliDestination1Image)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Destination 2 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination 2 image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst2.SetImagePtr(fliDestination2Image)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst1)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst1)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Operation Logical Xnor 객체 생성 # Create Operation Logical Xnor object
		operationLogicalXnor = COperationLogicalXnor()

		# Source 이미지 설정 # Set the source image
		operationLogicalXnor.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 # Set the destination image
		operationLogicalXnor.SetDestinationImage(fliDestination1Image)
		
		# 연산 방식 스칼라로 설정 # Set operation source to scalar
		operationLogicalXnor.SetOperationSource(EOperationSource.Scalar)
		
		# Logical Xnor 값 지정 # Set the Logical Xnor value
		mvScalar = CMultiVar[Double](0, 0, 0)
		operationLogicalXnor.SetScalarValue(mvScalar)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := operationLogicalXnor.Execute()).IsFail():

			ErrorPrint(res, 'Failed to execute Operation Logical Xnor.')
			break

		# Destination 이미지 설정 # Set the destination image
		operationLogicalXnor.SetDestinationImage(fliDestination2Image)
		
		# Logical Xnor 값 지정 # Set the Logical Xnor value
		mvScalar = CMultiVar[Double](255, 255, 255)
		operationLogicalXnor.SetScalarValue(mvScalar)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := operationLogicalXnor.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Logical Xnor.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination1 = viewImageDst1.GetLayer(0)
		layerDestination2 = viewImageDst2.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination1.Clear()
		layerDestination2.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerDestination1.DrawTextCanvas(flpPoint, 'Destination Image(LogicalXnor 0)', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerDestination2.DrawTextCanvas(flpPoint, 'Destination Image(LogicalXnor 255)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst1.Invalidate(True)
		viewImageDst2.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst1.IsAvailable() and viewImageDst2.IsAvailable():
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