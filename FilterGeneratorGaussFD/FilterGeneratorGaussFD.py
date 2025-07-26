# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliFFTImage = CFLImage()
	fliGaussFilterImage = CFLImage()
	fliGaussImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageFFT = CGUIViewImage()
	viewImageGaussFilter = CGUIViewImage()
	viewImageGauss = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/FilterGeneratorFD/Sea1Ch.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(100, 0, 500, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# FFT 이미지 뷰 생성 // Create the FFT image view
		if (res := viewImageFFT.Create(100, 400, 500, 800)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Gauss filter 이미지 뷰 생성 // Create the butterworth filter image view
		if (res := viewImageGaussFilter.Create(500, 0, 900, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Gauss 이미지 뷰 생성 // Create the butterworth image view
		if (res := viewImageGauss.Create(500, 400, 900, 800)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageFFT)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageGaussFilter)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageGauss)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# FFT 이미지 뷰에 이미지를 디스플레이 // Display the image in the FFT image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageFFT.SetImagePtr(fliFFTImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Gauss filter 이미지 뷰에 이미지를 디스플레이 // Display the image in the butterworth filter image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageGaussFilter.SetImagePtr(fliGaussFilterImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Gauss 이미지 뷰에 이미지를 디스플레이 // Display the image in the butterworth image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageGauss.SetImagePtr(fliGaussImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageFFT)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageGaussFilter)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageGauss)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Fourier Transform 객체 생성 // Create Fourier Transform object
		fourierTransform = CFourierTransform()

		# Source 이미지 설정 // Set the source image
		fourierTransform.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set the destination image
		fourierTransform.SetDestinationImage(fliFFTImage)

		# 결과 이미지 포멧 설정 (FFT image, 32/64 bit Floating Point 설정 가능) // Set the result image format (FFT image, 32/64 bit Floating Point can be set)
		fourierTransform.SetResultType(EFloatingPointAccuracy.Bit32)

		# 푸리에 변환 결과 이미지를 쉬프트해서 받도록 설정 // Set to receive the Fourier transform result image shifted
		fourierTransform.SetShiftSpectrum(EFourierTransformShiftSpectrum.Shift)

		# 알고리즘 수행 // Execute algorithm
		if (res := fourierTransform.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Fourier Transform.')
			break

		# FilterGeneratorGaussFD 객체 생성 // Create FilterGeneratorGaussFD object
		filterGeneratorGaussFD = CFilterGeneratorGaussFD()

		# Source 이미지 설정 // Set the source image
		filterGeneratorGaussFD.SetSourceImage(fliFFTImage)

		# 정밀도 설정 (32/64 bit Floating Point 설정 가능) // Set the precision (32/64 bit Floating Point can be set)
		filterGeneratorGaussFD.SetAccuracy(EFloatingPointAccuracy.Bit32)

		# 필터 타입 설정 // Set the filter type
		filterGeneratorGaussFD.SetType(CFilterGeneratorGaussFD.EFilterBaseFDType.FFT_Shift)

		# Destination 이미지 설정 // Set the destination image
		filterGeneratorGaussFD.SetDestinationImage(fliGaussFilterImage)

		# Sigma1 설정 // Set Sigma1
		filterGeneratorGaussFD.SetSigma1(2)

		# Sigma2 설정 // Set Sigma2
		filterGeneratorGaussFD.SetSigma2(1)

		# Phi 설정 // Set Phi
		filterGeneratorGaussFD.SetPhi(0.785398)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := filterGeneratorGaussFD.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute FilterGeneratorGaussFD.')
			break

		# Opeartion Multiply 객체 생성 // Create OperationMultiply object
		operationMultiply = COperationMultiply()

		# 연산 방식 설정 // Set operation source
		operationMultiply.SetOperationSource(EOperationSource.Image)

		# Source 이미지 설정 // Set the source image
		operationMultiply.SetSourceImage(fliFFTImage)

		# Operand 이미지 설정 // Set the operand image
		operationMultiply.SetOperandImage(fliGaussFilterImage)

		# Destination 이미지 설정 // Set the destination image
		operationMultiply.SetDestinationImage(fliGaussImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := operationMultiply.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute OperationMultiply.')
			break

		# Source 이미지 설정(FFT image) // Set the source image (FFT image)
		fourierTransform.SetSourceImage(fliGaussImage)

		# Destination 이미지 설정(IFFT image) // Set the destination image (IFFT image)
		fourierTransform.SetDestinationImage(fliGaussImage)

		# 알고리즘 수행 // Execute algorithm
		if (res := fourierTransform.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Fourier Transform.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerFFT = viewImageFFT.GetLayer(0)
		layerGaussFilter = viewImageGaussFilter.GetLayer(0)
		layerGauss = viewImageGauss.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerFFT.Clear()
		layerGaussFilter.Clear()
		layerGauss.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerFFT.DrawTextCanvas(flpPoint, 'FFT Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerGaussFilter.DrawTextCanvas(flpPoint, 'Gauss Filter', EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layerGauss.DrawTextCanvas(flpPoint, 'Gauss Filtering Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)
		viewImageFFT.Invalidate(True)
		viewImageGaussFilter.Invalidate(True)
		viewImageGauss.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageFFT.IsAvailable() and viewImageGaussFilter.IsAvailable() and viewImageGauss.IsAvailable():
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