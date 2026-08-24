# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliOperand1Image = CFLImage()
	fliOperand2Image = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageOpr1 = CGUIViewImage()
	viewImageOpr2 = CGUIViewImage()

	while True:
		
		# 이미지 로드 # Load image
		if (res := fliSourceImage.Load('../../ExampleImages/CorrelationCoefficient/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliOperand1Image.Load('../../ExampleImages/CorrelationCoefficient/Operand1.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliOperand2Image.Load('../../ExampleImages/CorrelationCoefficient/Operand2.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSrc.Create(400, 0, 950, 550)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageOpr1.Create(950, 0, 1500, 550)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageOpr2.Create(1500, 0, 2050, 550)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageOpr1.SetImagePtr(fliOperand1Image)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageOpr2.SetImagePtr(fliOperand2Image)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views.
		if (res := viewImageSrc.SynchronizePointOfView(viewImageOpr1)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageSrc.SynchronizePointOfView(viewImageOpr2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		if (res := viewImageSrc.SynchronizeWindow(viewImageOpr1)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		if (res := viewImageSrc.SynchronizeWindow(viewImageOpr2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Correlation Coefficient 객체 생성 # Create Correlation Coefficient object
		correlationCoefficient = CCorrelationCoefficient()

		# Source 이미지 설정 # Set the source image
		correlationCoefficient.SetSourceImage(fliSourceImage)

		# Operand 이미지 설정 # Set the operand image
		correlationCoefficient.SetOperandImage(fliOperand1Image)

		# 알고리즘 수행 # Execute the algorithm
		if (res := correlationCoefficient.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Correlation Coefficient.')
			break

		# 결과값을 받아올 CMultiVar[Double] 컨테이너 생성 # Create the CMultiVar[Double] object to push the result
		mvResult1 = CMultiVar[Double]()

		# 결과 값을 가져오는 함수 # Function that get result value
		if (res := correlationCoefficient.GetResult(mvResult1))[0].IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# Operand 이미지 설정 # Set the operand image
		correlationCoefficient.SetOperandImage(fliOperand2Image)

		# 알고리즘 수행 # Execute the algorithm
		if (res := correlationCoefficient.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Correlation Coefficient.')
			break

		# 결과값을 받아올 CMultiVar[Double] 컨테이너 생성 # Create the CMultiVar[Double] object to push the result
		mvResult2 = CMultiVar[Double]()

		# 결과 값을 가져오는 함수 # Function that get result value
		if (res := correlationCoefficient.GetResult(mvResult2))[0].IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerOperand1 = viewImageOpr1.GetLayer(0)
		layerOperand2 = viewImageOpr2.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerOperand1.Clear()
		layerOperand2.Clear()

		strResult1 = 'Operand 1\nCorrelation Coefficient : {}'.format(mvResult1.GetAt(0))
		strResult2 = 'Operand 2\nCorrelation Coefficient : {}'.format(mvResult2.GetAt(0))

		Console.WriteLine(strResult1)
		Console.WriteLine(strResult2)

		flpPoint = CFLPoint[Double](0, 0)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerOperand1.DrawTextCanvas(flpPoint, strResult1, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerOperand2.DrawTextCanvas(flpPoint, strResult2, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageOpr1.Invalidate(True)
		viewImageOpr2.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageOpr1.IsAvailable() and viewImageOpr2.IsAvailable():
			CThreadUtilities.Sleep(1)

		viewImageSrc.Destroy()
		viewImageOpr1.Destroy()
		viewImageOpr2.Destroy()

		break
	
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()