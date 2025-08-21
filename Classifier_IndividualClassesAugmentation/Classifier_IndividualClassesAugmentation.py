
# FLImagingClrPy 선언 # Declare FLImagingClrPy
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

# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliLearnImage = CFLImage()
	fliSourceImage = CFLImage()
	fliValidateImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageSource = CGUIViewImage()
	viewImageValidate = CGUIViewImage()

	# 그래프 뷰 선언 # Declare the graph view
	viewGraph = CGUIViewGraph()
	bTerminated = False

	while True:
		# 라이브러리가 완전히 로드 될 때까지 기다림 # Wait for the library to fully load
		time.sleep(1)

		# Learn 이미지 로드 # Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/Classifier/mnist100.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Classifier/mnist20.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Validation 이미지 로드 # Load the validation image
		if (res := fliValidateImage.Load('../../ExampleImages/Classifier/mnist20.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Learn 이미지 뷰 생성 # Create learn image view
		if (res := viewImageLearn.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSource.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Validation 이미지 뷰 생성 # Create the validation image view
		if (res := viewImageValidate.Create(1124, 0, 1636, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Graph 뷰 생성 # Create graph view
		if (res := viewGraph.Create(100, 512, 612, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the graph view.')
			break

		# Learn 이미지 뷰에 이미지를 디스플레이 # Display the image in the learn image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Validation 이미지 뷰에 이미지를 디스플레이 # Display the image in the validation image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageValidate.SetImagePtr(fliValidateImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizePointOfView(viewImageValidate)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageSource)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		if (res := viewImageLearn.SynchronizeWindow(viewImageValidate)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLearn = viewImageLearn.GetLayer(0)
		layerSource = viewImageSource.GetLayer(0)
		layerValidate = viewImageValidate.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLearn.Clear()
		layerSource.Clear()
		layerValidate.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerLearn.DrawTextCanvas(flpPoint, 'LEARN', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerSource.DrawTextCanvas(flpPoint, 'INFERENCE', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerValidate.DrawTextCanvas(flpPoint, 'VALIDATE', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 객체 생성 # Create object
		classifierDL = CClassifierDL()

		# OptimizerSpec 객체 생성 # Create OptimizerSpec object
		optSpec = COptimizerSpecAdamGradientDescent()

		# 학습할 이미지 설정 # Set the image to learn
		classifierDL.SetLearningImage(fliLearnImage)

		# 검증할 이미지 설정 # Set the image to validate
		classifierDL.SetLearningValidationImage(fliValidateImage)

		# 분류할 이미지 설정 # Set the image to classify
		classifierDL.SetInferenceImage(fliSourceImage)
		classifierDL.SetInferenceResultImage(fliSourceImage)

		# 학습할 Classifier 모델 설정 # Set up the Classifier model to learn
		classifierDL.SetModel(CClassifierDL.EModel.FL_CF_C)
		# 학습할 Classifier 모델 버전 설정 # Set up the Classifier model version to learn
		classifierDL.SetModelVersion(CClassifierDL.EModelVersion.FL_CF_C_V1_32)
		# 학습 epoch 값을 설정 # Set the learn epoch value 
		classifierDL.SetLearningEpoch(150)
		# 학습 이미지 Interpolation 방식 설정 # Set Interpolation method of learn image
		classifierDL.SetInterpolationMethod(EInterpolationMethod.Bilinear)

		# Optimizer의 학습률 설정 # Set learning rate of Optimizer
		optSpec.SetLearningRate(0.001)
		# 설정한 Optimizer를 Classifier에 적용 # Apply Optimizer that we set up to Classifier
		classifierDL.SetLearningOptimizerSpec(optSpec)
		# 모델의 최적의 상태를 추적 후 마지막에 최적의 상태로 적용할 지 여부 설정 # Set whether to track the optimal state of the model and apply it as the optimal state at the end.
		classifierDL.EnableOptimalLearningStatePreservation(True)

		# 학습을 종료할 조건식 설정. f1score값이 0.999 이상인 경우 학습 종료한다. metric와 동일한 값입니다.
		# Set Conditional Expression to End Learning. If the f1score value is 0.999 or higher, end the learning. Same value as metric.
		classifierDL.SetLearningStopCondition('f1score >= 0.999')

		# 자동 저장 옵션 설정 # Set Auto-Save Options
		autoSaveSpec = CAutoSaveSpec()

		# 자동 저장 활성화 # Enable Auto-Save
		# 저장 때문에 발생하는 속도 저하를 막기 위해 예제에서는 코드 사용법만 표시하고 옵션은 끔 # To prevent performance degradation caused by saving, the examples only demonstrate how to use the code, with the saving option disabled.
		autoSaveSpec.EnableAutoSave(False)
		# 저장할 모델 경로 설정 # Set Model path to save
		autoSaveSpec.SetAutoSavePath('model.flcf')
		# 자동 저장 조건식 설정. 현재 f1score값이 최대 값인 경우 저장 활성화
		# Set auto-save conditional expressions. Enable save if the current f1score value is the maximum value
		autoSaveSpec.SetAutoSaveCondition("f1score > max('f1score')")

		# 자동 저장 옵션 설정 # Set Auto-Save Options
		classifierDL.SetLearningAutoSaveSpec(autoSaveSpec)

		# Augmentation Preset 설정 # Set Augmentation Preset
		augSpec1 = CAugmentationSpec()

		augSpec1.EnableAugmentation(True)
		augSpec1.SetCommonActivationRate(1.000000)
		augSpec1.SetCommonIoUThreshold(0.000000)
		augSpec1.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)

		augSpec1.EnableRotation(True)
		augSpec1.SetRotationParam(-30.000000, 30.000000, False, False, 1.000000)

		augmentationPreset1 = CAugmentationPreset()
		flaClassNum1 = List[int]()
		flaClassNum1.Add(0)
		flaClassNum1.Add(1)
		augmentationPreset1.SetClassNumbers(flaClassNum1)
		augmentationPreset1.SetName("Class 0")
		augmentationPreset1.SetAugmentationSpec(augSpec1)
		classifierDL.AddLearningAugmentationPreset(augmentationPreset1)
		augSpec2 = CAugmentationSpec()

		augSpec2.EnableAugmentation(True)
		augSpec2.SetCommonActivationRate(0.500000)
		augSpec2.SetCommonIoUThreshold(0.000000)
		augSpec2.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)

		augSpec2.EnableRotation(True)
		augSpec2.SetRotationParam(-180.000000, 180.000000, False, False, 1.000000)

		augmentationPreset2 = CAugmentationPreset()
		flaClassNum2 = List[int]()
		flaClassNum2.Add(2)
		augmentationPreset2.SetClassNumbers(flaClassNum2)
		augmentationPreset2.SetName("Class 2")
		augmentationPreset2.SetAugmentationSpec(augSpec2)
		classifierDL.AddLearningAugmentationPreset(augmentationPreset2)
		augSpec3 = CAugmentationSpec()

		augSpec3.EnableAugmentation(True)
		augSpec3.SetCommonActivationRate(1.000000)
		augSpec3.SetCommonIoUThreshold(0.000000)
		augSpec3.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)

		augSpec3.EnableScale(True)
		augSpec3.SetScaleParam(0.670000, 1.500000, 0.670000, 1.500000, True, 1.000000)

		augmentationPreset3 = CAugmentationPreset()
		flaClassNum3 = List[int]()
		flaClassNum3.Add(3)
		augmentationPreset3.SetClassNumbers(flaClassNum3)
		augmentationPreset3.SetName("Class 3")
		augmentationPreset3.SetAugmentationSpec(augSpec3)
		classifierDL.AddLearningAugmentationPreset(augmentationPreset3)
		augSpec4 = CAugmentationSpec()

		augSpec4.EnableAugmentation(True)
		augSpec4.SetCommonActivationRate(1.000000)
		augSpec4.SetCommonIoUThreshold(0.000000)
		augSpec4.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)

		augSpec4.EnableQuarterRotation(True)
		augSpec4.SetQuarterRotationParam(True, True, True, True, 1.000000)

		augmentationPreset4 = CAugmentationPreset()
		flaClassNum4 = List[int]()
		flaClassNum4.Add(4)
		flaClassNum4.Add(5)
		augmentationPreset4.SetClassNumbers(flaClassNum4)
		augmentationPreset4.SetName("Class 4,5")
		augmentationPreset4.SetAugmentationSpec(augSpec4)
		classifierDL.AddLearningAugmentationPreset(augmentationPreset4)

		# Classifier learn function을 진행하는 스레드 생성 # Create the Classifier Learn function thread
		def Learn_thread():
			global eLearnResult, bTerminated
			eLearnResult = classifierDL.Learn()
			bTerminated = True
		
		def Input_thread():
			global bEscape
			while True:
				if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':  # ESC key
					bEscape = True
					break
		
		threading.Thread(target=Learn_thread).start()
		threading.Thread(target=Input_thread, daemon=True).start()

		while not classifierDL.IsRunning() and not bTerminated:
			time.sleep(0.001)

		i32MaxEpoch = classifierDL.GetLearningEpoch()
		i32PrevEpoch = 0
		i32PrevCostCount = 0
		i32PrevValidationCount = 0

		while True:
			time.sleep(0.001)

			# 마지막 미니 배치 최대 반복 횟수 받기 # Get the last maximum number of iterations of the last mini batch 
			i32MaxIteration = classifierDL.GetActualMiniBatchCount()
			# 마지막 미니 배치 반복 횟수 받기 # Get the last number of mini batch iterations
			i32Iteration = classifierDL.GetLearningResultCurrentIteration()
			# 마지막 학습 횟수 받기 # Get the last epoch learning
			i32Epoch = classifierDL.GetLastEpoch()

			if i32Epoch != i32PrevEpoch and i32Iteration == i32MaxIteration and i32Epoch > 0:
				# 학습 결과 비용과 검증 결과 기록을 받아 그래프 뷰에 출력  
				# Get the history of cost and validation and print it at graph view
				listCosts = List[Single]()
				listValidations = List[Single]()
				listF1Score = List[Single]()
				listValidationEpoch = List[int]()

				res, listCosts, listValidations, listF1Score, listValidationEpoch = classifierDL.GetLearningResultAllHistory(listCosts, listValidations, listF1Score, listValidationEpoch)
				
				if listCosts.Count != 0:
					# 마지막 학습 결과 비용 받기 # Get the last cost of the learning result
					f32CurrCost = listCosts[listCosts.Count - 1]
					# 마지막 검증 결과 받기 # Get the last validation result
					f32Validation = listValidations[listValidations.Count - 1] if listValidations.Count != 0 else 0
					# 마지막 F1점수 결과 받기 # Get the last F1 Score result
					f32F1Score = listF1Score[listF1Score.Count - 1] if listF1Score.Count != 0 else 0

					# 해당 epoch의 비용과 검증 결과 값 출력 # Print cost and validation value for the relevant epoch
					print("Cost : {:.6f} Validation : {:.6f} F1 Score : {:.6f} Epoch {} / {}".format(f32CurrCost, f32Validation, f32F1Score, i32Epoch, i32MaxEpoch))

					# 비용 기록이나 검증 결과 기록이 있다면 출력 # Print results if cost or validation history exists
					if (listCosts.Count != 0 and i32PrevCostCount != listCosts.Count) or (listValidations.Count != 0 and i32PrevValidationCount != listValidations.Count):
						viewGraph.LockUpdate()

						# 이전 그래프의 데이터를 삭제 # Clear previous grpah data
						viewGraph.Clear()
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listCosts, EChartType.Line, EColor.RED, "Cost")

						i32Step = classifierDL.GetLearningValidationStep()
						listX = List[Single]()

						for i in range(listValidations.Count - 1):
							listX.Add((float)(i * i32Step))

						listX.Add((float)(listCosts.Count - 1))
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listX, listValidations, EChartType.Line, EColor.BLUE, "Validation")

						viewGraph.UnlockUpdate()
						viewGraph.Invalidate()

					# 검증 결과가 1.0일 경우 학습을 중단하고 분류 진행 
					# If the validation result is 1.0, stop learning and classify images 
					if f32Validation == 1.0 or bEscape:
						classifierDL.Stop()

					i32PrevEpoch = i32Epoch
					i32PrevCostCount = listCosts.Count
					i32PrevValidationCount = listValidations.Count

			if classifierDL.IsRunning() == False:
				break
			
		if eLearnResult.IsFail():
			ErrorPrint(eLearnResult, 'Failed to execute.')
			break

		# 추론 결과 정보에 대한 설정 # Set for the inference result information
		classifierDL.SetInferenceResultItemSettings(CClassifierDL.EInferenceResultItemSettings.ClassNum_ClassName_ConfidenceScore)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := classifierDL.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageLearn.Invalidate(True)
		viewImageSource.Invalidate(True)
		viewImageValidate.Invalidate(True)

		# 그래프 뷰를 갱신 # Update the Graph view.
		viewGraph.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageLearn.IsAvailable() and viewImageSource.IsAvailable() and viewImageValidate.IsAvailable() and viewGraph.IsAvailable():
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