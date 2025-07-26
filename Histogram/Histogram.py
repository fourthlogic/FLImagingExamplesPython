# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = CGUIViewImage()
	viewGraph = CGUIViewGraph()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSrcImage.Load('../../ExampleImages/Histogram/Escherichia coli.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImage.Create(100, 0, 100 + 440, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Graph 뷰 생성 # Create graph view
		if (res := viewGraph.Create(100 + 440 * 1, 0, 100 + 440 * 2, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SynchronizeWindow(viewGraph)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Histogram 객체 생성 # Create Histogram object
		Histogram = CHistogram()
		
		# ROI 지정 # Create ROI
		flrSrcROI = CFLRect[Double](161, 181, 293, 302)

		# Source 이미지 설정 # Set the source image
		Histogram.SetSourceImage(fliSrcImage)
		
		# Source ROI 영역 지정 # set Source ROI 
		Histogram.SetSourceROI(flrSrcROI)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := Histogram.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Histogram.')
			break
		
		# Result 결과 갯수 확인 # get result count
		i64IndexCount = Histogram.GetResultCount()

		# Channel 값 표기를 위한 String 변수 # string variable to indicate Channel value
		strChannel = ""

		# 그래프 선 색상 # Graph line color
		arrColor = [EColor.BLUE, EColor.LIGHTRED, EColor.GREEN]

		# Histogram 결과값 # Histogram Result Object
		listResult = List[UInt64]()

		for i in range(i64IndexCount):
			# 이전 데이터 삭제 # data clear
			listResult.Clear()
			
			# Histogram 결과 값 가져오기 # get projection result
			if (res := Histogram.GetResult(i, listResult)[0]).IsFail():
				ErrorPrint(res, "Failed to Get Result.")
				break

			# 채널 String # Channel String
			strChannel = f"Ch{i}"

			# Graph View 데이터 입력 # Input Graph View Data
			viewGraph.Plot(listResult, EChartType.Bar, arrColor[i], strChannel)

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImage.GetLayer(0)

		if (res := layerSource.DrawFigureImage(flrSrcROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImage.Invalidate(True)
		
		mvMean = CMultiVar[Double]()
		mvVariance = CMultiVar[Double]()
		mvStdDev = CMultiVar[Double]()
		mvMedian = CMultiVar[Double]()

		# 평균, 분산, 표준편차, 중앙값 받기 # get mean, variance, standard deviation, median
		Histogram.GetResultMean(mvMean)
		Histogram.GetResultVariance(mvVariance)
		Histogram.GetResultStdDev(mvStdDev)
		Histogram.GetResultMedian(mvMedian)

		# 출력 갯수 # get count
		i32ResultCount = mvMean.GetCount()

		# 평균, 분산, 표준편차, 중앙값 출력 # display Mean, variance, standard deviation, median
		for i in range(i32ResultCount):
			print(f"Channel {i}")
			print(f"Mean {mvMean.GetAt(i)}")
			print(f"Variance {mvVariance.GetAt(i)}")
			print(f"Standard Deviation {mvStdDev.GetAt(i)}")
			print(f"Median {mvMedian.GetAt(i)}\n")

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImage.IsAvailable() and viewGraph.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()