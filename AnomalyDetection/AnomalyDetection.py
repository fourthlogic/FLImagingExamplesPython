# FLImagingClrPy 선언 // Declare FLImagingClrPy
from tokenize import Single
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

# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliLearnImage = CFLImage()
	fliValidationImage = CFLImage()
	fliResultLabelFigureImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageInference = CGUIViewImage()
	viewImagesLabelFigure = CGUIViewImage()
	
	# 그래프 뷰 선언 // Declare the graph view
	viewGraph = CGUIViewGraph()
	bTerminated = False

	while True:
		
		# 학습 이미지 로드 // Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/AnomalyDetection/AnomalyDetectionTrainData.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 평가 이미지 로드 // Load the validation image
		if (res := fliValidationImage.Load('../../ExampleImages/AnomalyDetection/AnomalyDetectionValidationData.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# learn 이미지 뷰 생성 // Create learn image view
		if (res := viewImageLearn.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if((res := viewImageInference.Create(600, 0, 1100, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		if((res := viewImagesLabelFigure.Create(100, 500, 600, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		# Graph 뷰 생성 // Create graph view
		if((res := viewGraph.Create(600, 500, 1100, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		viewGraph.SetDarkMode()

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. // A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizePointOfView(viewImagesLabelFigure)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Learn 이미지 뷰에 이미지를 디스플레이 // Display the image in the learn image view
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. // A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Inference 이미지 뷰에 이미지를 디스플레이 // Display the image in the Inference image view
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. // A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageInference.SetImagePtr(fliValidationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Label 이미지 뷰에 이미지를 디스플레이 // Display the image in the label image view
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. // A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImagesLabelFigure.SetImagePtr(fliResultLabelFigureImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. // A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImagesLabelFigure)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerLearn = viewImageLearn.GetLayer(0)
		layerValidation = viewImageInference.GetLayer(0)
		layerResultLabelFigure = viewImagesLabelFigure.GetLayer(0)
	
		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerLearn.Clear()
		layerValidation.Clear()
		layerResultLabelFigure.Clear()
		
		# View 정보를 디스플레이 합니다. // Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.// The function DrawTextCanvas below draws a String based on the screen coordinates.
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

		if((res := layerResultLabelFigure.DrawTextCanvas(flpPoint, "RESULT", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		# 이미지 뷰를 갱신 // Update the image view.
		viewImageLearn.Invalidate(True)
		viewImageInference.Invalidate(True)
		viewImagesLabelFigure.Invalidate(True)
		
		# AnomalyDetection 객체 생성 // Create AnomalyDetection object
		anomalyDetection = CAnomalyDetectionDL()

		# OptimizerSpec 객체 생성 // Create OptimizerSpec object
		optSpec = COptimizerSpecAdamGradientDescent()

		# 학습할 이미지 설정 // Set the image to learn
		anomalyDetection.SetLearningImage(fliLearnImage)
		# 검증할 이미지 설정 // Set the image to validation
		anomalyDetection.SetLearningValidationImage(fliValidationImage)
		# 분류할 이미지 설정 // Set the image to classify
		anomalyDetection.SetInferenceImage(fliValidationImage)
		anomalyDetection.SetInferenceResultImage(fliResultLabelFigureImage)

		# 학습할 AnomalyDetection 모델 설정 // Set up the AnomalyDetection model to learn
		anomalyDetection.SetModel(CAnomalyDetectionDL.EModel.FLDefNet)
		# 학습할 AnomalyDetection 모델 Version 설정 // Set up the AnomalyDetection model version to learn
		anomalyDetection.SetModelVersion(CAnomalyDetectionDL.EModelVersion.FLDefNet_V1_32)
		# 학습 epoch 값을 설정 // Set the learn epoch value 
		anomalyDetection.SetLearningEpoch(1000)
		# 학습 이미지 Interpolation 방식 설정 // Set Interpolation method of learn image
		anomalyDetection.SetInterpolationMethod(EInterpolationMethod.Bilinear)
		# 모델의 최적의 상태를 추적 후 마지막에 최적의 상태로 적용할 지 여부 설정 // Set whether to track the optimal state of the model and apply it as the optimal state at the end.
		anomalyDetection.EnableOptimalLearningStatePreservation(True)
		
		# Optimizer의 학습률 설정 // Set learning rate of Optimizer
		optSpec.SetLearningRate(0.001)
		# 설정한 Optimizer를 AnomalyDetection에 적용 // Apply Optimizer that we set up to AnomalyDetection
		anomalyDetection.SetLearningOptimizerSpec(optSpec)

		# AugmentationSpec 설정 // Set the AugmentationSpec
		augSpec = CAugmentationSpec()

		augSpec.EnableAugmentation(True)
		augSpec.SetCommonActivationRate(0.5)
		augSpec.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)
		augSpec.EnablePerspective(True)
		augSpec.SetPerspectiveParam(0.0, 0.1, 1.0)
		augSpec.EnableHorizontalFlip(True)
		augSpec.EnableVerticalFlip(True)

		anomalyDetection.SetLearningAugmentationSpec(augSpec)

		# 학습을 종료할 조건식 설정. accuracy값이 0.9 이상인 경우 학습 종료한다.
		# Set Conditional Expression to End Learning. If the accuracy value is 0.9 or more, end learning.
		anomalyDetection.SetLearningStopCondition("accuracy >= 0.9")

		# 자동 저장 옵션 설정 // Set Auto-Save Options
		autoSaveSpec = CAutoSaveSpec()

		# 자동 저장 활성화 // Enable Auto-Save
		# 저장 때문에 발생하는 속도 저하를 막기 위해 예제에서는 코드 사용법만 표시하고 옵션은 끔 // To prevent performance degradation caused by saving, the examples only demonstrate how to use the code, with the saving option disabled.
		autoSaveSpec.EnableAutoSave(False)
		# 저장할 모델 경로 설정 // Set Model path to save
		autoSaveSpec.SetAutoSavePath("model.listd")
		# 자동 저장 조건식 설정. 현재 cost값이 최소이고 accuracy값이 최대 값인 경우 저장 활성화
		# Set auto-save conditional expressions. Enable save if the current cost value is minimum and the accumulation value is maximum
		autoSaveSpec.SetAutoSaveCondition("cost < min('cost') & accuracy > max('accuracy')")

		# 자동 저장 옵션 설정 // Set Auto-Save Options
		anomalyDetection.SetLearningAutoSaveSpec(autoSaveSpec)

		# AnomalyDetection learn function을 진행하는 스레드 생성 // Create the AnomalyDetection Learn function thread
		def Learn_thread():
			global eLearnResult, bTerminated
			eLearnResult = anomalyDetection.Learn()
			bTerminated = True
		
		def Input_thread():
			global bEscape
			while True:
				if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':  # ESC key
					bEscape = True
					break
		
		threading.Thread(target=Learn_thread).start()
		threading.Thread(target=Input_thread, daemon=True).start()

		while not anomalyDetection.IsRunning() and not bTerminated:
			time.sleep(0.001)

		i32MaxEpoch = anomalyDetection.GetLearningEpoch()
		i32PrevEpoch = 0
		i32PrevCostCount = 0
		i32PrevValidationCount = 0

		while(True):
			time.sleep(0.001)

			# 마지막 미니 배치 반복 횟수 받기 // Get the last maximum number of iterations of the last mini batch 
			i32MiniBatchCount = anomalyDetection.GetActualMiniBatchCount()
			# 마지막 미니 배치 반복 횟수 받기 // Get the last number of mini batch iterations
			i32Iteration = anomalyDetection.GetLearningResultCurrentIteration()
			# 마지막 학습 횟수 받기 // Get the last epoch learning
			i32Epoch = anomalyDetection.GetLastEpoch()
			
			# 미니 배치 반복이 완료되면 cost와 validation 값을 디스플레이 
			# Display cost and validation value if iterations of the mini batch is completed 
			if i32Epoch != i32PrevEpoch and i32Iteration == i32MiniBatchCount and i32Epoch > 0:
				# 마지막 학습 결과 비용 받기 // Get the last cost of the learning result
				f32CurrCost = anomalyDetection.GetLearningResultLastCost()
				# 마지막 검증 결과 받기 // Get the last validation result
				f32ValidationPa = anomalyDetection.GetLearningResultLastAccuracy()

				# 해당 epoch의 비용과 검증 결과 값 출력 // Prcost and validation value for the relevant epoch
				print("Cost : {:6f} Accuracy : {:6f}  Epoch {} / {}", f32CurrCost, f32ValidationPa, i32Epoch, i32MaxEpoch)

				# 학습 결과 비용과 검증 결과 기록을 받아 그래프 뷰에 출력  
				# Get the history of cost and validation and prit at graph view
				listCostHistory = List[Single]()
				listValidationHistory = List[Single]()
				vctValidationEpoch = List[Int32]()

				anomalyDetection.GetLearningResultAllHistory(listCostHistory, listValidationHistory, vctValidationEpoch)

				# 비용 기록이나 검증 결과 기록이 있다면 출력 // Prresults if cost or validation history exists
				if((listCostHistory.Count != 0 and i32PrevCostCount != listCostHistory.Count) or (listValidationHistory.Count != 0 and i32PrevValidationCount != listValidationHistory.Count)):
					i32Step = anomalyDetection.GetLearningValidationStep()
					listX = List[Single]()

					for i in range(listValidationHistory.Count - 1):
						listX.Add((i * i32Step))

					listX.Add((listCostHistory.Count - 1))

					# 이전 그래프의 데이터를 삭제 // Clear previous grpah data
					viewGraph.LockUpdate()
					viewGraph.Clear()

					# Graph View 데이터 입력 // Input Graph View Data
					viewGraph.Plot(listCostHistory, EChartType.Line, EColor.RED, "Cost")
					# Graph View 데이터 입력 // Input Graph View Data
					viewGraph.Plot(listX, listValidationHistory, EChartType.Line, EColor.CYAN, "Accuracy")
					viewGraph.UnlockUpdate()

					viewGraph.UpdateWindow()
					viewGraph.Invalidate()

				# 검증 결과가 1.0일 경우 학습을 중단하고 분류 진행 
				# If the validation result is 1.0, stop learning and classify images 
				if(f32ValidationPa == 1.0 or bEscape):
					anomalyDetection.Stop()

				i32PrevEpoch = i32Epoch
				i32PrevCostCount = listCostHistory.Count
				i32PrevValidationCount = listValidationHistory.Count

			# epoch만큼 학습이 완료되면 종료 // End when learning progresses as much as epoch
			if(anomalyDetection.IsRunning() == False):
				break
			
		if eLearnResult.IsFail():
			ErrorPrint(eLearnResult, 'Failed to execute.')
			break

		# Result Label Image에 피겨를 포함하지 않는 Execute
		# 분류할 이미지 설정 // Set the image to classify
		anomalyDetection.SetInferenceImage(fliValidationImage)
		# 추론 결과 이미지 설정 // Set the inference result Image
		anomalyDetection.SetInferenceResultImage(fliResultLabelFigureImage)
		# 추론 결과 옵션 설정 // Set the inference result options
		# 비정상 결과 비교 Threshold 설정 // Set Anomaly Threshold
		anomalyDetection.SetInferenceAnomalyThreshold(0.5)
		# 비정상 최소 크기 설정 // Set Minimum Anomaly Area
		anomalyDetection.SetInferenceMinimumAnomalyArea(4)

		# 알고리즘 수행 // Execute the algorithm
		if((res := anomalyDetection.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute.")
			break
		
		# 결과 이미지를 이미지 뷰에 맞게 조정합니다. // Fit the result image to the image view.
		viewImagesLabelFigure.ZoomFit()

		# 이미지 뷰를 갱신 // Update the image view.
		viewImageLearn.Invalidate(True)
		viewImageInference.Invalidate(True)
		viewImagesLabelFigure.Invalidate(True)
			
		# 그래프 뷰를 갱신 // Update the Graph view.
		viewGraph.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageLearn.IsAvailable() and viewImagesLabelFigure.IsAvailable()and viewImageInference.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()