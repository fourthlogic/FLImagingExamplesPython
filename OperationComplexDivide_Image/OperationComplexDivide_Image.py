# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliOperandImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageOpr = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/OperationComplexDivide/ExampleSource.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Operand 이미지 로드 # Load the operand image
		if (res := fliOperandImage.Load('../../ExampleImages/OperationComplexDivide/ExampleOperand.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 600, 545)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Operand 이미지 뷰 생성 # Create operand image view
		if (res := viewImageOpr.Create(600, 0, 1100, 545)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(1100, 0, 1600, 545)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageOpr))[0].IsFail() or \
			(res := viewImageSrc.SynchronizePointOfView(viewImageDst))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage))[0].IsFail() or \
			(res := viewImageOpr.SetImagePtr(fliOperandImage))[0].IsFail() or \
			(res := viewImageDst.SetImagePtr(fliDestinationImage))[0].IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageOpr))[0].IsFail() or \
			(res := viewImageSrc.SynchronizeWindow(viewImageDst))[0].IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Operation Complex Multiply 객체 생성 # Create Operation Complex Multiply object
		cd = COperationComplexDivide()

		# Source 이미지 설정 # Set the source image
		cd.SetSourceImage(fliSourceImage)

		# Operand 이미지 설정 # Set the operand image
		cd.SetOperandImage(fliOperandImage)

		# Destination 이미지 설정 # Set the destination image
		cd.SetDestinationImage(fliDestinationImage)
		
		# 연산 방식 스칼라로 설정 # Set operation source to image
		cd.SetOperationSource(EOperationSource.Image);

		# 오버플로 처리 방법 설정 # Set the overflow handling method
		cd.SetOverflowMethod(EOverflowMethod.Wrapping);

		# 공백 색상 칠하기 모드 해제 // Set the Fill blank color mode false
		# 결과 이미지가 이미 존재할 경우 연산되지 않은 영역을 공백 색상으로 칠하지 않고 원본 그대로 둔다. // If the destination image already exists, the uncomputed area is left intact without being painted in a blank color.
		cd.EnableFillBlankColorMode(False);
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := cd.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute complex divide.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerOperand = viewImageOpr.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerOperand.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerOperand.DrawTextCanvas(flpPoint, 'Operand Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageOpr.Invalidate(True)
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageOpr.IsAvailable() and viewImageDst.IsAvailable():
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
