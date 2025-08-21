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
		if (res := fliSourceImage.Load('../../ExampleImages/Statistics/StatisticsSource.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Statistics 객체 생성 # Create Statistics object
		statistics = CImageStatistics()

		# ROI 범위 설정 # Set the ROI value
		flrROI = CFLRect[int](264, 189, 432, 364)

		# Source 이미지 설정 # Set the source image
		statistics.SetSourceImage(fliSourceImage)

		# Source ROI 설정 # Set the Source ROI
		statistics.SetSourceROI(flrROI)

		# 결과값을 받아올 CMultiVar[Double] 컨테이너 생성 # Create the CMultiVar[Double] object to push the result
		mvMedian = CMultiVar[Double]()
		mvUpperQuartile = CMultiVar[Double]()
		mvLowerQuartile = CMultiVar[Double]()

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 중간값을 구하는 함수 # Function that calculate the median of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetMedian(mvMedian)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 75사분위수를 구하는 함수 # Function that calculate the upper quartile of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetUpperQuartile(mvUpperQuartile)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 25사분위수를 구하는 함수 # Function that calculate the lower quartile of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetLowerQuartile(mvLowerQuartile)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# trimming 옵션 설정(Lower:0.2, Upper:0.4) # Set the trimming value(Lower:0.2, Upper:0.4)
		statistics.SetTrimming(0.2, CImageStatistics.ETrimmingLocation.Lower)
		statistics.SetTrimming(0.4, CImageStatistics.ETrimmingLocation.Upper)

		# trimming 된 결과값을 받아올 CMultiVar[Double] 컨테이너 생성 # Create the CMultiVar[Double] object to push the trimmed result
		mvTrimmingMedian = CMultiVar[Double]()
		mvTrimmingUpperQuartile = CMultiVar[Double]()
		mvTrimmingLowerQuartile = CMultiVar[Double]()

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 중간값을 구하는 함수 # Function that calculate the median of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetMedian(mvTrimmingMedian)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 75사분위수를 구하는 함수 # Function that calculate the upper quartile of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetUpperQuartile(mvTrimmingUpperQuartile)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 25사분위수를 구하는 함수 # Function that calculate the lower quartile of the pixel value of the image(or the region of ROI)
		if (res := statistics.GetLowerQuartile(mvTrimmingLowerQuartile)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 # Display to find out where ROI is
		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break


		strMedianValue = 'Median Of Region : {}'.format(mvMedian)
		strLowerQuartileValue = '1st Quartile Of Region : {}'.format(mvLowerQuartile)
		strUpperQuartileValue = '3rd Quartile Of Region : {}'.format(mvUpperQuartile)

		strTrimmingMedianValue = 'Median Of Trimmed Region : {}'.format(mvTrimmingMedian)
		strTrimmingLowerQuartileValue = '1st Quartile Of Trimmed Region : {}'.format(mvTrimmingLowerQuartile)
		strTrimmingUpperQuartileValue = '3rd Quartile Of Trimmed Region : {}'.format(mvTrimmingUpperQuartile)

		strTrimming = 'Trimming Lower : {}, Upper : {}'.format(statistics.GetTrimming(CImageStatistics.ETrimmingLocation.Lower), statistics.GetTrimming(CImageStatistics.ETrimmingLocation.Upper))

		Console.WriteLine(strMedianValue)
		Console.WriteLine(strLowerQuartileValue)
		Console.WriteLine(strUpperQuartileValue)
		Console.WriteLine(strTrimming)
		Console.WriteLine(strTrimmingMedianValue)
		Console.WriteLine(strTrimmingLowerQuartileValue)
		Console.WriteLine(strTrimmingUpperQuartileValue)


		flpPoint = CFLPoint[Double](0, 0)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strMedianValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strLowerQuartileValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strUpperQuartileValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimming, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimmingMedianValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimmingLowerQuartileValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		flpPoint.Offset(0, 20)

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(flpPoint, strTrimmingUpperQuartileValue, EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
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