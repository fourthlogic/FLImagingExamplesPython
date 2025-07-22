# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Statistics/StatisticsSource.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Statistics 객체 생성 // Create Statistics object
		statistics = CImageStatistics()

		# ROI 범위 설정 // Set the ROI value
		flrROI = CFLRect[int](264, 189, 432, 364)

		# Source 이미지 설정 // Set the source image
		statistics.SetSourceImage(fliSourceImage)

		# Source ROI 설정 // Set the Source ROI
		statistics.SetSourceROI(flrROI)

		# 결과값을 받아올 CMultiVarD 컨테이너 생성 // Create the CMultiVarD object to push the result
		mvSum = CMultiVar[Double]()
		mvSumOfSquares = CMultiVar[Double]()


		# 이미지 전체(혹은 ROI 영역) 픽셀값의 합을 구하는 함수 // Function that calculate the sum of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetSum(mvSum)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 제곱합을 구하는 함수
		if (res := statistics.GetSumOfSquares(mvSumOfSquares)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# trimming 옵션 설정(Lower:0.2, Upper:0.4) // Set the trimming value(Lower:0.2, Upper:0.4)
		statistics.SetTrimming(0.2, CImageStatistics.ETrimmingLocation.Lower)
		statistics.SetTrimming(0.4, CImageStatistics.ETrimmingLocation.Upper)

		# trimming 된 결과값을 받아올 CMultiVarD 컨테이너 생성 // Create the CMultiVarD object to push the trimmed result
		mvTrimmingSum = CMultiVar[Double]()
		mvTrimmingSumOfSquares = CMultiVar[Double]()

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 합을 구하는 함수 // Function that calculate the sum of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetSum(mvTrimmingSum)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 제곱합을 구하는 함수 // Function that calculate the sum of squares of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetSumOfSquares(mvTrimmingSumOfSquares)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break


		strSumValue = 'Sum Of Region : {}'.format(mvSum)
		strSumOfSquaresValue = 'Sum of Squares Of Region : {}'.format(mvSumOfSquares)

		strTrimmingSumValue = 'Sum Of Trimmed Region : {}'.format(mvTrimmingSum)
		strTrimmingSumOfSquaresValue = 'Sum of Squares Of Trimmed Region : {}'.format(mvTrimmingSumOfSquares)

		strTrimming = 'Trimming Lower : {}, Upper : {}'.format(statistics.GetTrimming(CImageStatistics.ETrimmingLocation.Lower), statistics.GetTrimming(CImageStatistics.ETrimmingLocation.Upper))

		Console.WriteLine(strSumValue)
		Console.WriteLine(strSumOfSquaresValue)
		Console.WriteLine(strTrimming)
		Console.WriteLine(strTrimmingSumValue)
		Console.WriteLine(strTrimmingSumOfSquaresValue)


		flpPoint = CFLPoint[Double](0, 0)

		# 이미지 뷰 정보 표시 // Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strSumValue, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 30)

		# 이미지 뷰 정보 표시 // Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strSumOfSquaresValue, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 30)

		# 이미지 뷰 정보 표시 // Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimming, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 30)

		# 이미지 뷰 정보 표시 // Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimmingSumValue, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 30)

		# 이미지 뷰 정보 표시 // Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimmingSumOfSquaresValue, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable():
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