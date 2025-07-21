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
		res = fliSourceImage.Load('C:/Users/junhy/source/repos/fourthlogic/ExampleImages/OperationScaledDivide/Generator.flif')

		if res.IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Operand 이미지 로드 # Load the operand image
		res = fliOperandImage.Load('C:/Users/junhy/source/repos/fourthlogic/ExampleImages/OperationScaledDivide/Gradation_R2W.flif')

		if res.IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		res = fliDestinationImage.Assign(fliSourceImage)
		
		if res.IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		# Source 이미지 뷰 생성 # Create source image view
		res = viewImageSrc.Create(100, 0, 600, 545)

		if res.IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Operand 이미지 뷰 생성 # Create operand image view
		res = viewImageOpr.Create(600, 0, 1100, 545)

		if res.IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		res = viewImageDst.Create(1100, 0, 1600, 545)

		if res.IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageSrc.SynchronizePointOfView(viewImageOpr)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageSrc.SynchronizePointOfView(viewImageDst)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageSrc.SetImagePtr(fliSourceImage)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break
		
		# Operand 이미지 뷰에 이미지를 디스플레이 # Display the image in the operand image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageOpr.SetImagePtr(fliOperandImage)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break
		
		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageDst.SetImagePtr(fliDestinationImage)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageSrc.SynchronizeWindow(viewImageOpr)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		res = viewImageSrc.SynchronizeWindow(viewImageDst)

		if res[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break
		
		# ROI 설정을 위한 CFLRect 객체 생성 # Create a CFLRect object for setting ROI
		flrROI = CFLRect[int](200, 200, 500, 500);

		# Operation Scaled Divide 객체 생성 # Create Operation scaled divide object
		scaledDivide = COperationScaledDivide()

		# Source 이미지 설정 # Set the source image
		scaledDivide.SetSourceImage(fliSourceImage)
		
		# Source ROI 설정 # Set the Source ROI
		scaledDivide.SetSourceROI(flrROI);
		
		# Operand 이미지 설정 # Set the operand image
		scaledDivide.SetOperandImage(fliOperandImage)
		
		# Operand ROI 설정 # Set the Operand ROI
		scaledDivide.SetOperandROI(flrROI);
		
		# Destination 이미지 설정 # Set the destination image
		scaledDivide.SetDestinationImage(fliDestinationImage)
		
		# Destination ROI 설정 # Set the Destination ROI
		scaledDivide.SetDestinationROI(flrROI);
		
		# 연산 방식 스칼라로 설정 # Set operation source to image
		scaledDivide.SetOperationSource(EOperationSource.Image);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		res = scaledDivide.Execute()

		if res.IsFail():
			ErrorPrint(res, 'Failed to execute Operation Scaled Divide.')
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

		res = layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerOperand.DrawTextCanvas(flpPoint, 'Operand Image', EColor.YELLOW, EColor.BLACK, 20)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		res = layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)

		if res.IsFail():
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
