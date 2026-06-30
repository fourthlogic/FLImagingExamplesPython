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
	fliValidateImage = CFLImage()
	fliSourceImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageValidate = CGUIViewImage()
	viewImageSource = CGUIViewImage()

	# 그래프 뷰 선언 # Declare the graph view
	viewGraph = CGUIViewGraph()
	bTerminated = False

	while True:
		# 라이브러리가 완전히 로드 될 때까지 기다림 # Wait for the library to fully load
		time.sleep(1)

		# Learn 이미지 로드 # Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/StringBasedOCR/Learn.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Validation 이미지 로드 # Load the validation image
		if (res := fliValidateImage.Load('../../ExampleImages/StringBasedOCR/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/StringBasedOCR/Source.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Learn 이미지 뷰 생성 # Create learn image view
		if (res := viewImageLearn.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Validation 이미지 뷰 생성 # Create the validation image view
		if (res := viewImageValidate.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSource.Create(1124, 0, 1636, 512)).IsFail():
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

		# Validation 이미지 뷰에 이미지를 디스플레이 # Display the image in the validation image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageValidate.SetImagePtr(fliValidateImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSource.SynchronizePointOfView(viewImageValidate)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageLearn.SynchronizeWindow(viewImageValidate)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageSource)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLearn = viewImageLearn.GetLayer(0)
		layerValidate = viewImageValidate.GetLayer(0)
		layerSource = viewImageSource.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLearn.Clear()
		layerValidate.Clear()
		layerSource.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerLearn.DrawTextCanvas(flpPoint, 'LEARN', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerValidate.DrawTextCanvas(flpPoint, 'VALIDATE', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerSource.DrawTextCanvas(flpPoint, 'INFERENCE', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 객체 생성 # Create object
		stringBasedOCRDL = CStringBasedOCRDL()

		# 학습할 이미지 설정 # Set the image to learn
		stringBasedOCRDL.SetLearningImage(fliLearnImage)

		# 검증할 이미지 설정 # Set the image to validate
		stringBasedOCRDL.SetLearningValidationImage(fliValidateImage)

		# 학습할 StringBasedOCR 모델 설정 # Set up the StringBasedOCR model to learn
		stringBasedOCRDL.SetModel(CStringBasedOCRDL.EModel.FLOcrNet_S)
		# 학습할 StringBasedOCR 모델 버전 설정 # Set up the StringBasedOCR model version to learn
		stringBasedOCRDL.SetModelVersion(CStringBasedOCRDL.EModelVersion.FLOcrNet_S_V1_32_256_B2)
		# 학습 epoch 값을 설정 # Set the learn epoch value 
		stringBasedOCRDL.SetLearningEpoch(500)
		# 학습 이미지 Interpolation 방식 설정 # Set Interpolation method of learn image
		stringBasedOCRDL.SetInterpolationMethod(EInterpolationMethod.Bilinear)

		# OptimizerSpec 객체 생성 # Create OptimizerSpec object
		optSpec = COptimizerSpecAdamGradientDescent()
		# Optimizer의 학습률 설정 # Set learning rate of Optimizer
		optSpec.SetLearningRate(0.0001)
		# 설정한 Optimizer를 StringBasedOCR에 적용 # Apply Optimizer that we set up to StringBasedOCR
		stringBasedOCRDL.SetLearningOptimizerSpec(optSpec)

		# AugmentationSpec 설정 # Set the AugmentationSpec
		augSpec = CAugmentationSpec()

		augSpec.EnableAugmentation(True)
		augSpec.SetCommonActivationRate(1.0)
		augSpec.SetCommonIoUThreshold(0.8)
		augSpec.EnableRotation(True)
		augSpec.SetRotationParam(-15.0, 15.0, False, False, 1.0)
		augSpec.EnableScale(True)
		augSpec.SetScaleParam(.8, 1.2, .8, 1.2, False, 1.0)
		augSpec.EnableTranslation(True)
		augSpec.SetTranslationParam(0.0, 0.1, 0.0, 0.1, 1.0)

		# 설정한 Augmentation을 StringBasedOCR에 적용 # Apply Augmentation that we set up to StringBasedOCR
		stringBasedOCRDL.SetLearningAugmentationSpec(augSpec)

		# 학습을 종료할 조건식 설정. metric값이 1.0 이상인 경우 학습 종료한다. metric와 동일한 값입니다.
		# Set Conditional Expression to End Learning. If the metric value is 1.0 or higher, end the learning. Same value as metric.
		stringBasedOCRDL.SetLearningStopCondition('metric >= 1.0')
		
		# 자동 저장 옵션 설정 # Set Auto-Save Options
		autoSaveSpec = CAutoSaveSpec()

		# 자동 저장 활성화 # Enable Auto-Save
		# 저장 때문에 발생하는 속도 저하를 막기 위해 예제에서는 코드 사용법만 표시하고 옵션은 끔 # To prevent performance degradation caused by saving, the examples only demonstrate how to use the code, with the saving option disabled.
		autoSaveSpec.EnableAutoSave(False)
		# 저장할 모델 경로 설정 # Set Model path to save
		autoSaveSpec.SetAutoSavePath('model.flsbocrdl')
		# 자동 저장 조건식 설정. 현재 f1score값이 최대 값인 경우 저장 활성화
		# Set auto-save conditional expressions. Enable save if the current f1score value is the maximum value
		autoSaveSpec.SetAutoSaveCondition("epoch >= 10 & metric > max('metric')")

		# 자동 저장 옵션 설정 # Set Auto-Save Options
		stringBasedOCRDL.SetLearningAutoSaveSpec(autoSaveSpec)

		# StringBasedOCR learn function을 진행하는 스레드 생성 # Create the StringBasedOCR Learn function thread
		def Learn_thread():
			global eLearnResult, bTerminated
			eLearnResult = stringBasedOCRDL.Learn()
			bTerminated = True
		
		def Input_thread():
			global bEscape
			while True:
				if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':  # ESC key
					bEscape = True
					break
		
		threading.Thread(target=Learn_thread).start()
		threading.Thread(target=Input_thread, daemon=True).start()

		while not stringBasedOCRDL.IsRunning() and not bTerminated:
			time.sleep(0.001)

		i32MaxEpoch = stringBasedOCRDL.GetLearningEpoch()
		i32PrevEpoch = 0
		i32PrevCostCount = 0
		i32PrevValidationCount = 0

		while True:
			time.sleep(0.001)

			# 마지막 미니 배치 최대 반복 횟수 받기 # Get the last maximum number of iterations of the last mini batch 
			i32MaxIteration = stringBasedOCRDL.GetActualMiniBatchCount()
			# 마지막 미니 배치 반복 횟수 받기 # Get the last number of mini batch iterations
			i32Iteration = stringBasedOCRDL.GetLearningResultCurrentIteration()
			# 마지막 학습 횟수 받기 # Get the last epoch learning
			i32Epoch = stringBasedOCRDL.GetLastEpoch()

			if i32Epoch != i32PrevEpoch and i32Iteration == i32MaxIteration and i32Epoch > 0:
				# 학습 결과 비용과 검증 결과 기록을 받아 그래프 뷰에 출력  
				# Get the history of cost and validation and print it at graph view
				listCosts = List[Single]()
				list1MNED = List[Single]()
				listMeanAP = List[Single]()
				listValidationEpoch = List[Int32]()

				res = stringBasedOCRDL.GetLearningResultAllHistory(listCosts, list1MNED, listMeanAP, listValidationEpoch)[0]
				
				if listCosts.Count != 0:
					# 마지막 학습 결과 비용 받기 # Get the last cost of the learning result
					f32CurrCost = listCosts[listCosts.Count - 1]
					# 마지막 1-NED 결과 받기 # Get the last 1-NED result
					f321MNED = list1MNED[list1MNED.Count - 1] if list1MNED.Count != 0 else 0
					# 마지막 mAP 결과 받기 # Get the last mAP result
					f32MeanAP = listMeanAP[listMeanAP.Count - 1] if listMeanAP.Count != 0 else 0

					# 해당 epoch의 비용과 검증 결과 값 출력 # Print cost and validation value for the relevant epoch
					print("Cost : {:.6f} 1-NED : {:.6f} mAP : {:.6f} Epoch {} / {}".format(f32CurrCost, f321MNED, f32MeanAP, i32Epoch, i32MaxEpoch))

					# 비용 기록이나 검증 결과 기록이 있다면 출력 # Print results if cost or validation history exists
					if (listCosts.Count != 0 and i32PrevCostCount != listCosts.Count) or (list1MNED.Count != 0 and i32PrevValidationCount != list1MNED.Count):
						viewGraph.LockUpdate()

						# 이전 그래프의 데이터를 삭제 # Clear previous graph data
						viewGraph.Clear()
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listCosts, EChartType.Line, EColor.RED, "Cost")

						i32Step = stringBasedOCRDL.GetLearningValidationStep()
						listV1 = List[Single]()

						for i in range(list1MNED.Count - 1):
							listV1.Add((float)(i * i32Step))

						listV1.Add((float)(listCosts.Count - 1))
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listV1, list1MNED, EChartType.Line, EColor.BLUE, "1-NED")

						listV2 = List[Single]()

						for i in range(listMeanAP.Count - 1):
							listV2.Add((float)(i * i32Step))

						listV2.Add((float)(listCosts.Count - 1))
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listV2, listMeanAP, EChartType.Line, EColor.GREEN, "mAP")

						viewGraph.UnlockUpdate()
						viewGraph.Invalidate()

					# 검증 결과가 1.0일 경우 학습을 중단하고 인식 진행 
					# If the validation result is 1.0, stop learning and classify images 
					if f321MNED == 1.0 and f32MeanAP == 1.0 or bEscape:
						stringBasedOCRDL.Stop()

					i32PrevEpoch = i32Epoch
					i32PrevCostCount = listCosts.Count
					i32PrevValidationCount = list1MNED.Count

			if stringBasedOCRDL.IsRunning() == False:
				break
			
		if eLearnResult.IsFail():
			ErrorPrint(eLearnResult, 'Failed to learn.')
			break

		# 인식할 이미지 설정 # Set the image to recognize
		stringBasedOCRDL.SetInferenceImage(fliSourceImage)
		stringBasedOCRDL.SetInferenceResultImage(fliSourceImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := stringBasedOCRDL.Execute()).IsFail():
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
