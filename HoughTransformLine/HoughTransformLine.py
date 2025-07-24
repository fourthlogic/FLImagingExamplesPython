# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSrcImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImage = CGUIViewImage()

	while True:
		# 이미지 로드 // Load image
		if (res := fliSrcImage.Load('../../ExampleImages/HoughTransform/Sudoku.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 이미지 뷰 생성 // Create image view
		if (res := viewImage.Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		

		# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# HoughTransform 객체 생성 // Create HoughTransform  object
		houghTransform = CHoughTransform()

		# Source 이미지 설정 // Set the source image
		houghTransform.SetSourceImage(fliSrcImage)

		# HoughTransform Line 변환 선택 // Select HoughTransform Line transform
		houghTransform.SetHoughShape(CHoughTransform.EHoughShape.Line)

		# 이미지로 임계값으로 동작하는 모드 적용 // Apply the mode that operates as a threshold to the image
		houghTransform.SetExecuteMode(CHoughTransform.EExecuteMode.Image)

		# Threshold 값 설정 // Set Threshold value
		houghTransform.SetPixelThreshold(10)

		# 조건 타입 설정 Less (Threshold 값 이하의 픽셀) // Set the condition type Less (pixels below the Threshold value)
		houghTransform.SetLogicalCondition(ELogicalCondition.Less)

		# 최소 픽셀 카운터 수 (픽셀 카운터 기준보다 낮을 경우 필터링) // Minimum number of pixel counters (Filter if lower than pixel counter criteria)
		houghTransform.SetMinPixelCount(200);

		# 인접 거리 필터링 설정 (거리 +-5, 각도 +-5 기준 가장 카운팅이 많이된 픽셀 값을 Line으로 선정) 
		# Neighbor Distance Filtering Settings(Based on distance +-5, angle +-5, the most counted pixel value is selected as a line)
		houghTransform.SetNearbyLineFilter(5);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := (houghTransform.Execute())).IsFail():
		
			ErrorPrint(res, 'Failed to execute HoughTransform.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layer = viewImage.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer.Clear()

		# Result 갯수 가져오기 // Get the number of results
		i64ResultCount = houghTransform.GetResultLinesCount()

		flcResult = CFLLine[Double]()

		for i in range(0, i64ResultCount):
			houghTransform.GetResultLine(i, flcResult)

			# 이미지 뷰에 검출된 원 객체 출력 // Output the detected original object to the image view
			if (res := (layer.DrawFigureImage(flcResult, EColor.LIGHTGREEN, 1))).IsFail():
			
				ErrorPrint(res, 'Failed to draw Figure')
				break

		# 이미지 뷰를 갱신 합니다. // Update image view
		viewImage.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		while viewImage.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()