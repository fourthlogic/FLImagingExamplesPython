# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from enum import Enum

class EType(Enum):
	Source = 0
	Destination = 1
	ETypeCount = 2

# 메인 함수 # Main function
def main():
	
	# 이미지 객체 선언 # Declare the image object
	arrFliImage = List[CFLImage]()
	for i in range(0, (EType.ETypeCount.value)):
		arrFliImage.Add(CFLImage())

	# 이미지 뷰 선언 # Declare the image view
	arrViewImage = List[CGUIViewImage]()
	for i in range(0, (EType.ETypeCount.value)):
		arrViewImage.Add(CGUIViewImage())

	res = CResult()

	while True:
		# Source 이미지 로드 # Load the source image
		if (res := arrFliImage[(EType.Source.value)].Load("../../ExampleImages/HoleFilling/TodoList.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		# Destination1 이미지를 16-bit 이미지로 로드 # Load the 16-bit destination image
		if (res := arrFliImage[(EType.Destination.value)].Assign(arrFliImage[(EType.Source.value)])).IsFail():
			ErrorPrint(res, "Failed to assign the image file.\n")
			break


		bError = False
		
		for i in range(0, (EType.ETypeCount.value)):
			# 이미지 뷰 생성 # Create image view
			if (res := (arrViewImage[i].Create(i * 512 + 100, 0, i * 512 + 100 + 512, 512))).IsFail():
				ErrorPrint(res, "Failed to create the image view.\n")
				bError = True
				break


			# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
			if (res := (arrViewImage[i].SetImagePtr(arrFliImage[i])))[0].IsFail():
				ErrorPrint(res, "Failed to set image object on the image view.\n")
				bError = True
				break


			if i == (EType.Source.value):
				continue

			# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
			if (res := (arrViewImage[(EType.Source.value)].SynchronizePointOfView(arrViewImage[i])))[0].IsFail():
				ErrorPrint(res, "Failed to synchronize view\n")
				bError = True
				break


			# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
			if (res := (arrViewImage[(EType.Source.value)].SynchronizeWindow(arrViewImage[i])))[0].IsFail():
				ErrorPrint(res, "Failed to synchronize window.\n")
				bError = True
				break

		if bError:
			break

		# 알고리즘 객체 생성 # Create Algorithm object
		alg = CHoleFilling()

		# Source 이미지 설정 # Set the source image
		if (res := alg.SetSourceImage(arrFliImage[(EType.Source.value)]))[0].IsFail():
			break
		# Destination 이미지 설정 # Set the destination image
		if (res := alg.SetDestinationImage(arrFliImage[(EType.Destination.value)]))[0].IsFail():
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

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := (alg.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute HoleFilling.")
			break


		arrLayer = List[CGUIViewImageLayer]()
		for i in range(0, (EType.ETypeCount.value)):
			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
			arrLayer.Add(arrViewImage[i].GetLayer(0))

			# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
			arrLayer[i].Clear()

		# View 정보를 디스플레이 한다. # Display view information
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. # The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다. # If the color parameter is added as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by processing it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#				 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#				  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpZero = CFLPoint[Double](0, 0)

		if (res := (arrLayer[(EType.Source.value)].DrawTextCanvas(flpZero, "Source Image", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		if (res := (arrLayer[(EType.Destination.value)].DrawTextCanvas(flpZero, "Destination Image", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		flfHoleContour = alg.GetSelectedPageFigureObject()

		if (res := (arrLayer[(EType.Source.value)].DrawFigureImage(flfHoleContour, EColor.CYAN))).IsFail():
			ErrorPrint(res, "Failed to draw figure.\n")
			break


		# 이미지 뷰를 갱신 합니다. # Update image view
		for i in range(0, (EType.ETypeCount.value)):
			arrViewImage[i].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		bAvailable = True
		while bAvailable:			
			for i in range(0, (EType.ETypeCount.value)):
				bAvailable = arrViewImage[i].IsAvailable()

				if not bAvailable:
					break

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