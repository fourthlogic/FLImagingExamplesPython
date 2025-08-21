# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Statistics/MultiChannelSource.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(400, 0, 1150, 700)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Statistics 객체 생성 # Create Statistics object
		imageStatistics = CImageStatistics()

		# Source 이미지 설정 # Set the source image
		imageStatistics.SetSourceImage(fliSourceImage)

		# 상관관계를 구할 채널을 설정
		imageStatistics.SetCorrelatedChannel(0, 1)

		# 결과값을 받아올 double 변수 생성 # Create the variable to save the result
		f64Covariance = 0.0
		f64CorrelationCoeff = 0.0

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 공분산을 구하는 함수 # Function that calculate the covariance of the pixel value of the image(or the region of ROI)
		res, f64Covariance = imageStatistics.GetCovariance(f64Covariance)

		if res.IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 상관계수를 구하는 함수 # Function that calculate the correlation coefficient of the pixel value of the image(or the region of ROI)
		res, f64CorrelationCoeff = imageStatistics.GetCorrelationCoefficient(f64CorrelationCoeff)

		if res.IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 상관관계를 구할 채널을 설정 # Set the Correlation channel
		imageStatistics.SetCorrelatedChannel(0, 2)

		# 결과값을 받아올 double 변수 생성 # Create the variable to save the result
		f64Covariance2 = 0
		f64CorrelationCoeff2 = 0

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 공분산을 구하는 함수 # Function that calculate the covariance of the pixel value of the image(or the region of ROI)
		res, f64Covariance2 = imageStatistics.GetCovariance(f64Covariance2)

		if res.IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 상관계수를 구하는 함수 # Function that calculate the correlation coefficient of the pixel value of the image(or the region of ROI)
		res, f64CorrelationCoeff2 = imageStatistics.GetCorrelationCoefficient(f64CorrelationCoeff2)
		if res.IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()


		strCorrChannel = 'Correlation Channel: Channel 0 - Channel 1'
		strCovarianceValue = 'Covariance : {}'.format(f64Covariance)
		strCorrelationCoeffValue = 'Correlation Coefficient : {}'.format(f64CorrelationCoeff)

		strCorrChannel2 = 'Correlation Channel: Channel 0 - Channel 2'
		strCovarianceValue2 = 'Covariance : {}'.format(f64Covariance2)
		strCorrelationCoeffValue2 = 'Correlation Coefficient : {}'.format(f64CorrelationCoeff2)

		Console.WriteLine(strCorrChannel)
		Console.WriteLine(strCovarianceValue)
		Console.WriteLine(strCorrelationCoeffValue)
		Console.WriteLine(strCorrChannel2)
		Console.WriteLine(strCovarianceValue2)
		Console.WriteLine(strCorrelationCoeffValue2)

		flpPoint = CFLPoint[Double](0, 0)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strCorrChannel, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strCovarianceValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strCorrelationCoeffValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strCorrChannel2, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strCovarianceValue2, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strCorrelationCoeffValue2, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable():
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