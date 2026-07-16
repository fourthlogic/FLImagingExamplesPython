# FLImagingClrPy 선언 # Declare FLImagingClrPy
from tokenize import Single, String
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import threading
import time
import msvcrt

bEscape = False
bTerminated = False
eLearnResult = CResult()

# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliLearnImage = CFLImage()
	fliValidationImage = CFLImage()
	fliResultLabelImage = CFLImage()
	fliResultLabelFigureImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageValidation = CGUIViewImage()
	viewImagesLabel = CGUIViewImage()
	viewImagesLabelFigure = CGUIViewImage()
	
	# 그래프 뷰 선언 # Declare the graph view
	viewGraph = CGUIViewGraph()
	bTerminated = False

	while True:
		# 학습 이미지 로드 # Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/SemanticSegmentation/Cityscape.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 평가 이미지 로드 # Load the validation image
		if (res := fliValidationImage.Load('../../ExampleImages/SemanticSegmentation/Cityscape.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# learn 이미지 뷰 생성 # Create learn image view
		if (res := viewImageLearn.Create(100, 0, 600, 500)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if((res := viewImageValidation.Create(600, 0, 1100, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		if((res := viewImagesLabel.Create(100, 500, 600, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		if((res := viewImagesLabelFigure.Create(600, 500, 1100, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		# Graph 뷰 생성 # Create graph view
		if((res := viewGraph.Create(1100, 0, 1600, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		viewGraph.SetDarkMode()

		# 이미지 뷰에 이미지를 디스플레이 # display the image in the imageview
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		if (res := viewImageValidation.SetImagePtr(fliValidationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImagesLabel.SetImagePtr(fliResultLabelImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		viewImagesLabel.EnablePixelSegmentationMode(True)

		if (res := viewImagesLabelFigure.SetImagePtr(fliResultLabelFigureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageValidation.SynchronizePointOfView(viewImagesLabel)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

			# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageValidation.SynchronizePointOfView(viewImagesLabelFigure)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageValidation)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImagesLabel)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImagesLabelFigure)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewGraph)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLearn = viewImageLearn.GetLayer(0)
		layerValidation = viewImageValidation.GetLayer(0)
		layerResultLabel = viewImagesLabel.GetLayer(0)
		layerResultLabelFigure = viewImagesLabelFigure.GetLayer(0)
	
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLearn.Clear()
		layerValidation.Clear()
		layerResultLabel.Clear()
		layerResultLabelFigure.Clear()
		
		# View 정보를 디스플레이 합니다. # Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpPoint = CFLPoint[Double](0, 0)

		if((res := layerLearn.DrawTextCanvas(flpPoint, "LEARN", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break
		
		if((res := layerValidation.DrawTextCanvas(flpPoint, "VALIDATION", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		if((res := layerResultLabel.DrawTextCanvas(flpPoint, "RESULT", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		if((res := layerResultLabelFigure.DrawTextCanvas(flpPoint, "RESULT FIGURE", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		# 이미지 뷰를 갱신 # Update the image view.
		viewImageLearn.Invalidate(True)
		viewImageValidation.Invalidate(True)
		viewImagesLabel.Invalidate(True)
		viewImagesLabelFigure.Invalidate(True)
		
		# SemanticSegmentation 객체 생성 # Create SemanticSegmentation object
		semanticSegmentationDL = CSemanticSegmentationDL()

		# OptimizerSpec 객체 생성 # Create OptimizerSpec object
		optSpec = COptimizerSpecAdamGradientDescentDL()

		# 학습할 이미지 설정 # Set the image to learn
		semanticSegmentationDL.SetLearningImage(fliLearnImage)
		# 검증할 이미지 설정 # Set the image to validation
		semanticSegmentationDL.SetLearningValidationImage(fliValidationImage)
		# 분류할 이미지 설정 # Set the image to classify
		semanticSegmentationDL.SetInferenceImage(fliValidationImage)
		semanticSegmentationDL.SetInferenceResultImage(fliResultLabelFigureImage)

		# 학습할 SemanticSegmentation 모델 설정 # Set up the SemanticSegmentation model to learn
		semanticSegmentationDL.SetModel(CSemanticSegmentationDL.EModel.FLSegNet)
		# 학습할 SemanticSegmentation 모델 Version 설정 # Set up the SemanticSegmentation model version to learn
		semanticSegmentationDL.SetModelVersion(CSemanticSegmentationDL.EModelVersion.FLSegNet_V1_256_B1)
		# 학습 epoch 값을 설정 # Set the learn epoch value 
		semanticSegmentationDL.SetLearningEpoch(1000)
		# 학습 이미지 Interpolation 방식 설정 # Set Interpolation method of learn image
		semanticSegmentationDL.SetInterpolationMethod(EInterpolationMethod.Bilinear)
		
		# Optimizer의 학습률 설정 # Set learning rate of Optimizer
		optSpec.SetLearningRate(0.001)
		# 설정한 Optimizer를 SemanticSegmentation에 적용 # Apply Optimizer that we set up to SemanticSegmentation
		semanticSegmentationDL.SetLearningOptimizerSpec(optSpec)

		# 학습을 종료할 조건식 설정. miou.ze값이 0.85 이상인 경우 학습 종료한다. metric.ze와 동일한 값입니다.
		# Set Conditional Expression to End Learning. If the miou.ze value is 0.85 or higher, end the learning. Same value as metric.ze.
		semanticSegmentationDL.SetLearningStopCondition("mIoU.ze >= 0.85")

		# 학습 이미지 분할 모드 설정.
		# 정사각형 비율을 유지하여 모델 크기로 이미지를 나누어 처리한다.
		# Set the training image segmentation mode.
		# The original image is divided and processed by the model size by maintaining the square ratio.
		semanticSegmentationDL.SetImageTilingMode(ETilingMode.SingleAxisTiling_ProportionalFit)
		# 학습 이미지 분할 모드의 겹치는 비율을 설정 # Set the overlap ratio of the learning image in tiling mode
		semanticSegmentationDL.SetLearningImageTilingOverlapRatio(0.25)
		# 자동 저장 옵션 설정 # Set Auto-Save Options
		autoSaveSpec = CAutoSaveSpecDL()

		# 자동 저장 활성화 # Enable Auto-Save
		# 저장 때문에 발생하는 속도 저하를 막기 위해 예제에서는 코드 사용법만 표시하고 옵션은 끔 # To prevent performance degradation caused by saving, the examples only demonstrate how to use the code, with the saving option disabled.
		autoSaveSpec.EnableAutoSave(False)
		# 저장할 모델 경로 설정 # Set Model path to save
		autoSaveSpec.SetAutoSavePath("model.flss")
		# 자동 저장 조건식 설정. 현재 cost값이 최소이고 accuracy값이 최대 값인 경우 저장 활성화
		# Set auto-save conditional expressions. Enable save if the current cost value is minimum and the accumulation value is maximum
		autoSaveSpec.SetAutoSaveCondition("miou.ze > max('miou.ze')")

		# 자동 저장 옵션 설정 # Set Auto-Save Options
		semanticSegmentationDL.SetLearningAutoSaveSpec(autoSaveSpec)

		# SemanticSegmentation learn function을 진행하는 스레드 생성 # Create the SemanticSegmentation Learn function thread
		def Learn_thread():
			global eLearnResult, bTerminated
			eLearnResult = semanticSegmentationDL.Learn()
			bTerminated = True
		
		def Input_thread():
			global bEscape
			while True:
				if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':  # ESC key
					bEscape = True
					break
		
		threading.Thread(target=Learn_thread).start()
		threading.Thread(target=Input_thread, daemon=True).start()

		while not semanticSegmentationDL.IsRunning() and not bTerminated:
			time.sleep(0.001)

		i32MaxEpoch = semanticSegmentationDL.GetLearningEpoch()
		i32PrevEpoch = 0
		i32PrevCostCount = 0
		i32PrevValidationCount = 0

		while(True):
			time.sleep(0.001)

			# 마지막 미니 배치 반복 횟수 받기 # Get the last maximum number of iterations of the last mini batch 
			i32MiniBatchCount = semanticSegmentationDL.GetActualMiniBatchCount()
			# 마지막 미니 배치 반복 횟수 받기 # Get the last number of mini batch iterations
			i32Iteration = semanticSegmentationDL.GetLearningResultCurrentIteration()
			# 마지막 학습 횟수 받기 # Get the last epoch learning
			i32Epoch = semanticSegmentationDL.GetLastEpoch()
			
			# 미니 배치 반복이 완료되면 cost와 validation 값을 디스플레이 
			# Display cost and validation value if iterations of the mini batch is completed 
			if i32Epoch != i32PrevEpoch and i32Iteration == i32MiniBatchCount and i32Epoch > 0:
				# 마지막 학습 결과 비용 받기 # Get the last cost of the learning result
				f32CurrCost = semanticSegmentationDL.GetLearningResultLastCost()
				# 마지막 검증 결과 받기 # Get the last validation result
				f32ValidationPa = semanticSegmentationDL.GetLearningResultLastAccuracy()
				f32ValidationPaMeanIoU = semanticSegmentationDL.GetLearningResultLastMeanIoU()

				# 해당 epoch의 비용과 검증 결과 값 출력 # Prcost and validation value for the relevant epoch
				print("Cost : {:6f} Pixel Accuracy : {:6f} mIoU : {:6f} Epoch {} / {}".format(f32CurrCost, f32ValidationPa, f32ValidationPaMeanIoU, i32Epoch, i32MaxEpoch))

				# 학습 결과 비용과 검증 결과 기록을 받아 그래프 뷰에 출력  
				# Get the history of cost and validation and prit at graph view
				listCostHistory = List[Single]()
				listValidationHistory = List[Single]()
				listMeanIoUHistory = List[Single]()
				listValidationsZEHistory = List[Single]()
				listMeanIoUZEHistory = List[Single]()
				vctValidationEpoch = List[Int32]()

				semanticSegmentationDL.GetLearningResultAllHistory(listCostHistory, listValidationHistory, listMeanIoUHistory, listValidationsZEHistory, listMeanIoUZEHistory, vctValidationEpoch)

				# 비용 기록이나 검증 결과 기록이 있다면 출력 # Prresults if cost or validation history exists
				if((listCostHistory.Count != 0 and i32PrevCostCount != listCostHistory.Count) or (listValidationHistory.Count != 0 and i32PrevValidationCount != listValidationHistory.Count)):
					i32Step = semanticSegmentationDL.GetLearningValidationStep()
					listX = List[Single]()

					for i in range(listValidationHistory.Count - 1):
						listX.Add((i * i32Step))

					listX.Add((listCostHistory.Count - 1))

					# 이전 그래프의 데이터를 삭제 # Clear previous graph data
					viewGraph.LockUpdate()
					viewGraph.Clear()

					# Graph View 데이터 입력 # Input Graph View Data
					viewGraph.Plot(listCostHistory, EChartType.Line, EColor.RED, "Cost")
					# Graph View 데이터 입력 # Input Graph View Data
					viewGraph.Plot(listX, listValidationHistory, EChartType.Line, EColor.CYAN, "Validation")
					viewGraph.Plot(listX, listMeanIoUHistory, EChartType.Line, EColor.BLUE, "mIoU")
					viewGraph.UnlockUpdate()

					viewGraph.UpdateWindow()
					viewGraph.Invalidate()

				# 검증 결과가 1.0일 경우 학습을 중단하고 분류 진행 
				# If the validation result is 1.0, stop learning and classify images 
				if(f32ValidationPa == 1.0 or bEscape):
					semanticSegmentationDL.Stop()

				i32PrevEpoch = i32Epoch
				i32PrevCostCount = listCostHistory.Count
				i32PrevValidationCount = listValidationHistory.Count

			# epoch만큼 학습이 완료되면 종료 # End when learning progresses as much as epoch
			if(semanticSegmentationDL.IsRunning() == False):
				break
			
		if eLearnResult.IsFail():
			ErrorPrint(eLearnResult, 'Failed to execute.')
			break

		# Result Label Image에 피겨를 포함하지 않는 Execute
		# 분류할 이미지 설정 # Set the image to classify
		semanticSegmentationDL.SetInferenceImage(fliValidationImage)
		# 추론 결과 이미지 설정 # Set the inference result Image
		semanticSegmentationDL.SetInferenceResultImage(fliResultLabelImage)
		# 추론 결과 옵션 설정 # Set the inference result options
		# Result 결과를 Label Image로 받을지 여부 설정 # Set whether to receive the result as a Label Image
		semanticSegmentationDL.EnableInferenceResultLabelImage(True)
		# Result 결과에 Region Figure를 포함 여부 설정 # Set whether to include region figure in result
		semanticSegmentationDL.EnableInferenceResultIncludingRegionFigures(False)

		# 알고리즘 수행 # Execute the algorithm
		if((res := semanticSegmentationDL.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute.")
			break
		
		# Result Label Image에 피겨를 포함한 Execute
		# 추론 결과 이미지 설정 # Set the inference result Image
		semanticSegmentationDL.SetInferenceResultImage(fliResultLabelFigureImage)
		# 추론 결과 옵션 설정 # Set the inference result options
		# Result 결과를 Label Image로 받을지 여부 설정 # Set whether to receive the result as a Label Image
		semanticSegmentationDL.EnableInferenceResultLabelImage(False)
		# Result 결과에 Region Figure를 포함 여부 설정 # Set whether to include region figure in result
		semanticSegmentationDL.EnableInferenceResultIncludingRegionFigures(True)
		# Result item settings enum 설정 # Set the result item settings
		semanticSegmentationDL.SetInferenceResultItemSettings(CSemanticSegmentationDL.EInferenceResultItemSettings.ClassNum_ClassName_ConfidenceScore)
		# 결과 도형 타입 설정 # Set the result figure type
		semanticSegmentationDL.SetInferenceResultRegionFigureType(CSemanticSegmentationDL.EInferenceResultRegionFigureType.Region)

		# 알고리즘 수행 # Execute the algorithm
		if((res := semanticSegmentationDL.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute.")
			break

		# ResultLabl 뷰에 Floating Value Range를 설정
		viewImagesLabel.SetFloatingImageValueRange(0, semanticSegmentationDL.GetLearningResultClassCount())

		# 결과 이미지를 이미지 뷰에 맞게 조정합니다. # Fit the result image to the image view.
		viewImagesLabel.ZoomFit()
		viewImagesLabelFigure.ZoomFit()

		# 이미지 뷰를 갱신 # Update the image view.
		viewImageLearn.RedrawWindow()
		viewImageValidation.RedrawWindow()
		viewImagesLabel.RedrawWindow()
		viewImagesLabelFigure.RedrawWindow()
			
		# 그래프 뷰를 갱신 # Update the Graph view.
		viewGraph.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageLearn.IsAvailable() and viewImageValidation.IsAvailable() and viewImagesLabel.IsAvailable() and viewImagesLabelFigure.IsAvailable() and viewGraph.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()