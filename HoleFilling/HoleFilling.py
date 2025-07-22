# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	
	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/HoleFilling/TodoList.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		
		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSrc.Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		if (res := viewImageDst.Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		# 알고리즘 객체 생성 # Create algorithm object
		alg = CHoleFilling()

		# Source 이미지 설정 # Set the source image
		if (res := alg.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# Destination 이미지 설정 # Set the destination image
		if (res := alg.SetDestinationImage(fliDstImage)[0]).IsFail():
			break
		# 처리할 Hole Area 넓이 범위 설정 # Set hole area range to process
		if (res := alg.SetMinimumHoleArea(10)).IsFail():
			break
		# 처리할 Hole Area 넓이 범위 설정 # Set hole area range to process
		if (res := alg.SetMaximumHoleArea(99999999999)).IsFail():
			break
		# 이미지 경계와 맞닿은 hole 의 처리 여부 설정 # Set whether to process holes that touch the image boundary
		if (res := alg.EnableIgnoreBoundaryHole(True)).IsFail():
			break
		# Threshold 를 통과한 픽셀이 hole 인지 object 인지 설정 # Set whether the pixel that passed the threshold is a hole or an object
		if (res := alg.SetThresholdPassTarget(CHoleFilling.EThresholdPassTarget.Object)).IsFail():
			break
		# Threshold 수와 결합 방식을 의미하는 Threshold 모드 설정 # Threshold mode setting, which refers to the number of threshold and combination method
		if (res := alg.SetThresholdMode(EThresholdMode.Dual_And)).IsFail():
			break
		# 각 Threshold 내에서 채널 별 논리 결과 간의 결합 방식을 의미하는 Logical Condition Of Channels 설정 # Set the Logical Condition Of Channels, which refers to the combination method between logical results for each channel within each Threshold
		if (res := alg.SetLogicalConditionOfChannels(ELogicalConditionOfChannels.And)).IsFail():
			break
		# Hole 영역을 채우는 방식을 설정 # Set the method of filling the hole area
		if (res := alg.SetFillingMethod(CHoleFilling.EFillingMethod.HarmonicInterpolation)).IsFail():
			break
		# Harmonic Interpolation 의 Precision 값 설정 # Set precision value for Harmonic Interpolation
		if (res := alg.SetPrecision(0.1)).IsFail():
			break
		# Harmonic Interpolation 의 Max Iteration 값 설정 # Set max iteration value for Harmonic Interpolation
		if (res := alg.SetMaxIteration(100)).IsFail():
			break
		# 첫 번째 Threshold 의 채널 별 논리 연산자와 값 설정 # Set the logical operator and value for each channel of the first Threshold
		mvThresholdCondition1 = CMultiVar[UInt64](Convert.ToUInt64(ELogicalCondition.GreaterEqual), Convert.ToUInt64(ELogicalCondition.GreaterEqual), Convert.ToUInt64(ELogicalCondition.GreaterEqual))
		if (res := alg.SetThresholdCondition(EThresholdIndex.First, mvThresholdCondition1)).IsFail():
			break
		mvThresholdValue1U64 = CMultiVar[UInt64](175, 230, 240)
		if (res := alg.SetThresholdValue(EThresholdIndex.First, mvThresholdValue1U64)).IsFail():
			break
		# 두 번째 Threshold 의 채널 별 논리 연산자와 값 설정 # Set the logical operator and value for each channel of the second Threshold
		mvThresholdCondition2 = CMultiVar[UInt64](Convert.ToUInt64(ELogicalCondition.Less), Convert.ToUInt64(ELogicalCondition.Less), Convert.ToUInt64(ELogicalCondition.Less))
		if (res := alg.SetThresholdCondition(EThresholdIndex.Second, mvThresholdCondition2)).IsFail():
			break
		mvThresholdValue2U64 = CMultiVar[UInt64](200, 240, 255)
		if (res := alg.SetThresholdValue(EThresholdIndex.Second, mvThresholdValue2U64)).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := (alg.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break
		

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpTemp = CFLPoint[Double](0, 0)
		if (res := layerSrc.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := layerDst.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		flfHoleContour = alg.GetSelectedPageFigureObject()
		if (res := layerSrc.DrawFigureImage(flfHoleContour, EColor.CYAN)).IsFail():
			ErrorPrint(res, "Failed to draw figure.\n")
			break

		# 이미지 뷰를 Zoom fit # Zoom fit image view
		viewImageSrc.ZoomFit()
		viewImageDst.ZoomFit()

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)
		
		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
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