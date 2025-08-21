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
	fliLearnImageLowResolution = CFLImage()
	fliValidationImageLowResolution = CFLImage()
	fliLearnImageHighResolution = CFLImage()
	fliValidationImageHighResolution = CFLImage()
	fliResultSourceImage = CFLImage()
	
	#/ 이미지 뷰 선언 # Declare the image view
	viewImageLearnLowResolution = CGUIViewImage()
	viewImageLearnHighResolution = CGUIViewImage()
	viewImageValidationLowResolution = CGUIViewImage()
	viewImageValidationHighResolution = CGUIViewImage()
	viewImagesSource = CGUIViewImage()

	# 그래프 뷰 선언 # Declare the graph view
	viewGraph = CGUIViewGraph()
	bTerminated = False

	while True:
		# 라이브러리가 완전히 로드 될 때까지 기다림 # Wait for the library to fully load
		time.sleep(1)

		# 이미지 로드 # Load image
		if((res := fliLearnImageLowResolution.Load("../../ExampleImages/SuperResolution/SuperResolutionTrainDataLowResolution.flif")).IsFail()):
			ErrorPrint(res, "Failed to load the image file. ")
			break
		
		# 이미지 로드 # Load image
		if((res := fliLearnImageHighResolution.Load("../../ExampleImages/SuperResolution/SuperResolutionTrainDataHighResolution.flif")).IsFail()):
			ErrorPrint(res, "Failed to load the image file. ")
			break

		if((res := fliValidationImageLowResolution.Load("../../ExampleImages/SuperResolution/SuperResolutionValidationDataLowResolution.flif")).IsFail()):
			ErrorPrint(res, "Failed to load the image file.")
			break

		if((res := fliValidationImageHighResolution.Load("../../ExampleImages/SuperResolution/SuperResolutionValidationDataHighResolution.flif")).IsFail()):
			ErrorPrint(res, "Failed to load the image file.")
			break

		# 이미지 뷰 생성 # Create image view
		if((res := viewImageLearnLowResolution.Create(100, 0, 600, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view. ")
			break

		# 이미지 뷰 생성 # Create image view
		if((res := viewImageLearnHighResolution.Create(600, 0, 1100, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view. ")
			break
		

		if((res := viewImageValidationLowResolution.Create(100, 500, 600, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break
		

		if((res := viewImageValidationHighResolution.Create(600, 500, 1100, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break
		

		if((res := viewImagesSource.Create(1100, 0, 1600, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break
		

		# Graph 뷰 생성 # Create graph view
		if((res := viewGraph.Create(1100, 500, 1600, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break
		

		viewGraph.SetDarkMode()

		# 저차원 학습 이미지 뷰에 이미지를 디스플레이 # Display the image in the learn low resolution image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageLearnLowResolution.SetImagePtr(fliLearnImageLowResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view. ")
			break

		# 고차원 학습 이미지 뷰에 이미지를 디스플레이 # Display the image in the learn high resolution image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageLearnHighResolution.SetImagePtr(fliLearnImageHighResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view. ")
			break

		# 저차원 평가 이미지 뷰에 이미지를 디스플레이 # Display the image in the validation low resolution image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageValidationLowResolution.SetImagePtr(fliValidationImageLowResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view. ")
			break

		# 고차원 평가 이미지 뷰에 이미지를 디스플레이 # Display the image in the validation high resolution image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageValidationHighResolution.SetImagePtr(fliValidationImageHighResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view. ")
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImagesSource.SetImagePtr(fliResultSourceImage)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view.")
			break

		# 다섯 개의 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the four image view windows
		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewImageValidationLowResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. ")
			break

		# 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewImageLearnHighResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. ")
			break

		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewImageValidationLowResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		
		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewImageValidationHighResolution)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		
		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewImagesSource)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. ")
			break

		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewGraph)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. ")
			break

		if((res := viewImageLearnLowResolution.SynchronizeWindow(viewGraph)[0]).IsFail()):
		
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		
		# 이미지의 Page Index를 맞춤 # Synchronize the Page Index of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageLearnLowResolution.SynchronizePageIndex(viewImageLearnHighResolution)[0]).IsFail()):
		
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		
		if((res := viewImageValidationLowResolution.SynchronizePageIndex(viewImageValidationHighResolution)[0]).IsFail()):
		
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		
		if((res := viewImageValidationHighResolution.SynchronizePageIndex(viewImagesSource)[0]).IsFail()):
		
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		
		# 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if((res := viewImageValidationHighResolution.SynchronizePointOfView(viewImagesSource)[0]).IsFail()):
		
			ErrorPrint(res, "Failed to synchronize window. ")
			break
		

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLearnLowResolution = viewImageLearnLowResolution.GetLayer(0)
		layerLearnHighResolution = viewImageLearnHighResolution.GetLayer(0)
		layerValidationLowResolution = viewImageValidationLowResolution.GetLayer(0)
		layerValidationHighResolution = viewImageValidationHighResolution.GetLayer(0)
		layerResultSource = viewImagesSource.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLearnLowResolution.Clear()
		layerLearnHighResolution.Clear()
		layerValidationLowResolution.Clear()
		layerValidationHighResolution.Clear()
		layerResultSource.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpPoint = CFLPoint[Double](0, 0)

		if((res := layerLearnLowResolution.DrawTextCanvas(flpPoint, "LEARN LOW RESOLUTION", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		if((res := layerLearnHighResolution.DrawTextCanvas(flpPoint, "LEARN HIGH RESOLUTION", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		if((res := layerValidationLowResolution.DrawTextCanvas(flpPoint, "VALIDATION LOW RESOLUTION", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		if((res := layerValidationHighResolution.DrawTextCanvas(flpPoint, "VALIDATION HIGH RESOLUTION", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		if((res := layerResultSource.DrawTextCanvas(flpPoint, "INFERENCE RESULT", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		# 이미지 뷰를 갱신 # Update the image view.
		viewImageLearnLowResolution.Invalidate(True)
		viewImageLearnHighResolution.Invalidate(True)
		viewImageValidationLowResolution.Invalidate(True)
		viewImageValidationHighResolution.Invalidate(True)
		viewImagesSource.Invalidate(True)

		# SuperResolution 객체 생성 # Create SuperResolution object
		superResolution = CSuperResolutionDL()

		# OptimizerSpec 객체 생성 # Create OptimizerSpec object
		optSpec = COptimizerSpecAdamGradientDescent()
		
		# Optimizer의 학습률 설정 # Set learning rate of Optimizer
		optSpec.SetLearningRate(0.001)

		# 학습할 이미지 설정 # Set the image to learn
		superResolution.SetLearningLowResolutionImage(fliLearnImageLowResolution)
		superResolution.SetLearningHighResolutionImage(fliLearnImageHighResolution)

		# 검증할 이미지 설정 # Set the image to validation
		superResolution.SetLearningLowResolutionValidationImage(fliValidationImageLowResolution)
		superResolution.SetLearningHighResolutionValidationImage(fliValidationImageHighResolution)

		# 분류할 이미지 설정 # Set the image to classify
		superResolution.SetInferenceImage(fliValidationImageLowResolution)
		superResolution.SetInferenceResultImage(fliResultSourceImage)

		# 학습할 SuperResolution 모델 설정 # Set up the SuperResolution model to learn
		superResolution.SetModel(CSuperResolutionDL.EModel.SRCNN)
		# 학습할 SuperResolution 모델 Version 설정 # Set up the SuperResolution model version to learn
		superResolution.SetModelVersion(CSuperResolutionDL.EModelVersion.SRCNN_V1_128)
		# 학습 epoch 값을 설정 # Set the learn epoch value 
		superResolution.SetLearningEpoch(500)
		# 학습 이미지 Interpolation 방식 설정 # Set Interpolation method of learn image
		superResolution.SetInterpolationMethod(EInterpolationMethod.Bilinear)
		# 이미지 배율 설정 # Set Scale Ratio
		superResolution.SetScaleRatio(2)
		# 모델의 최적의 상태를 추적 후 마지막에 최적의 상태로 적용할 지 여부 설정 # Set whether to track the optimal state of the model and apply it as the optimal state at the end.
		superResolution.EnableOptimalLearningStatePreservation(True)

		# 설정한 Optimizer를 SuperResolution에 적용 # Apply Optimizer that we set up to SuperResolution
		superResolution.SetLearningOptimizerSpec(optSpec)

		# AugmentationSpec 설정 # Set the AugmentationSpec
		augSpec = CAugmentationSpec()

		augSpec.EnableAugmentation(True)
		augSpec.SetCommonActivationRate(0.5)
		augSpec.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)
		augSpec.EnableTranslation(True)
		augSpec.SetTranslationParam(0.0, 0.1, 0.0, 0.1, 1.0)
		augSpec.EnableHorizontalFlip(True)
		augSpec.EnableVerticalFlip(True)

		superResolution.SetLearningAugmentationSpec(augSpec)

		# 학습을 종료할 조건식 설정. accuracy값이 0.9 이상인 경우 학습 종료한다.
		# Set Conditional Expression to End Learning. If the accuracy value is 0.9 or more, end learning.
		superResolution.SetLearningStopCondition("accuracy >= 0.9")

		# 자동 저장 옵션 설정 # Set Auto-Save Options
		autoSaveSpec = CAutoSaveSpec()

		# 자동 저장 활성화 # Enable Auto-Save
		# 저장 때문에 발생하는 속도 저하를 막기 위해 예제에서는 코드 사용법만 표시하고 옵션은 끔 # To prevent performance degradation caused by saving, the examples only demonstrate how to use the code, with the saving option disabled.
		autoSaveSpec.EnableAutoSave(False)
		# 저장할 모델 경로 설정 # Set Model path to save
		autoSaveSpec.SetAutoSavePath("model.flsr")
		# 자동 저장 조건식 설정. 현재 cost값이 최소이고 accuracy값이 최대 값인 경우 저장 활성화
		# Set auto-save conditional expressions. Enable save if the current cost value is minimum and the accumulation value is maximum
		autoSaveSpec.SetAutoSaveCondition("cost < min('cost') & accuracy > max('accuracy')")

		# 자동 저장 옵션 설정 # Set Auto-Save Options
		superResolution.SetLearningAutoSaveSpec(autoSaveSpec)

		# SuperResolution learn function을 진행하는 스레드 생성 # Create the SuperResolution Learn function thread
		def Learn_thread():
			global eLearnResult, bTerminated
			eLearnResult = superResolution.Learn()
			bTerminated = True
		
		def Input_thread():
			global bEscape
			while True:
				if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':  # ESC key
					bEscape = True
					break
		
		threading.Thread(target=Learn_thread).start()
		threading.Thread(target=Input_thread, daemon=True).start()

		while not superResolution.IsRunning() and not bTerminated:
			time.sleep(0.001)

		i32MaxEpoch = superResolution.GetLearningEpoch()
		i32PrevEpoch = 0
		i32PrevCostCount = 0
		i32PrevPSNRCount = 0
		i32PrevSSIMCount = 0
		i32PrevValidationCount = 0

		while(True):
			time.sleep(0.001)

			# 마지막 미니 배치 반복 횟수 받기 # Get the last maximum number of iterations of the last mini batch 
			i32MiniBatchCount = superResolution.GetActualMiniBatchCount()
			# 마지막 미니 배치 반복 횟수 받기 # Get the last number of mini batch iterations
			i32Iteration = superResolution.GetLearningResultCurrentIteration()
			# 마지막 학습 횟수 받기 # Get the last epoch learning
			i32Epoch = superResolution.GetLastEpoch()

			# 미니 배치 반복이 완료되면 cost와 validation 값을 디스플레이 
			# Display cost and validation value if iterations of the mini batch is completed 
			if i32Epoch != i32PrevEpoch and i32Iteration == i32MiniBatchCount and i32Epoch > 0:
				# 학습 결과 비용과 검증 결과 기록을 받아 그래프 뷰에 출력  
				# Get the history of cost and validation and prit at graph view
				listCosts = List[Single]()
				listPSNRHistory = List[Single]()
				listSSIMHistory = List[Single]()
				listValidations = List[Single]()
				vctValidationEpoch = List[Int32]()

				superResolution.GetLearningResultAllHistory(listCosts, listValidations, listPSNRHistory, listSSIMHistory,  vctValidationEpoch)

				if listCosts.Count != 0:
					# 마지막 학습 결과 비용 받기 # Get the last cost of the learning result
					f32CurrCost = listCosts[listCosts.Count - 1]
					# 마지막 PSNR 결과 받기 # Get the last PSNR result
					f32PSNRPa = listPSNRHistory[listPSNRHistory.Count - 1]
					# 마지막 SSIM 결과 받기 # Get the last SSIM result
					f32SSIMPa = listSSIMHistory[listSSIMHistory.Count - 1]
					# 마지막 검증 결과 받기 # Get the last validation result
					f32ValidationPa = listValidations[listValidations.Count - 1]
					
					# 해당 epoch의 비용과 검증 결과 값 출력 # Prcost and validation value for the relevant epoch
					print("Cost : {:6f} PSNR : {:6f} SSIM : {:6f} Accuracy : {:6f}  Epoch {} / {}".format(f32CurrCost, f32PSNRPa, f32SSIMPa, f32ValidationPa, i32Epoch, i32MaxEpoch))

					# 비용 기록이나 검증 결과 기록이 있다면 출력 # Prresults if cost or validation history exists
					if (listCosts.Count != 0 and i32PrevCostCount != listCosts.Count) or (listPSNRHistory.Count != 0 and i32PrevPSNRCount != listPSNRHistory.Count) or (listSSIMHistory.Count != 0 and i32PrevSSIMCount != listSSIMHistory.Count) or (listValidations.Count != 0 and i32PrevValidationCount != listValidations.Count):
						viewGraph.LockUpdate()
					
						# 이전 그래프의 데이터를 삭제 # Clear previous grpah data
						viewGraph.Clear()
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listCosts, EChartType.Line, EColor.RED, "Cost")

						i32Step = superResolution.GetLearningValidationStep()
						listX = List[Single]()
						
						for i in range(listValidations.Count - 1):
							listX.Add((float)(i * i32Step))

						listX.Add((float)(listCosts.Count - 1))

						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listX, listPSNRHistory, EChartType.Line, EColor.BLUE, "PSNR")
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listX, listSSIMHistory, EChartType.Line, EColor.GREEN, "SSIM")
						# Graph View 데이터 입력 # Input Graph View Data
						viewGraph.Plot(listX, listValidations, EChartType.Line, EColor.CYAN, "Accuracy")

						# 이전 그래프의 데이터를 삭제 # Clear previous grpah data
						viewGraph.UnlockUpdate()
						viewGraph.Invalidate()

					# 검증 결과가 1.0일 경우 학습을 중단하고 분류 진행 
					# If the validation result is 1.0, stop learning and classify images 
					if (f32ValidationPa == 1.0 or bEscape):
						superResolution.Stop()

					i32PrevEpoch = i32Epoch
					i32PrevCostCount = listCosts.Count
					i32PrevValidationCount = listValidations.Count
			

			# epoch만큼 학습이 완료되면 종료 # End when learning progresses as much as epoch
			if(superResolution.IsRunning() == False):
				break
	
		if eLearnResult.IsFail():
			ErrorPrint(eLearnResult, 'Failed to execute.')
			break

		# Result Label Image에 피겨를 포함하지 않는 Execute
		# 분류할 이미지 설정 # Set the image to classify
		superResolution.SetInferenceImage(fliValidationImageLowResolution)
		# 추론 결과 이미지 설정 # Set the inference result Image
		superResolution.SetInferenceResultImage(fliResultSourceImage)

		# 알고리즘 수행 # Execute the algorithm
		if((res := superResolution.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute.")
			break

		# 결과 이미지를 이미지 뷰에 맞게 조정합니다. # Fit the result image to the image view.
		viewImagesSource.ZoomFit()

		# 이미지 뷰를 갱신 # Update the image view.
		viewImageLearnLowResolution.Invalidate(True)
		viewImageLearnHighResolution.Invalidate(True)
		viewImageValidationLowResolution.Invalidate(True)
		viewImageValidationHighResolution.Invalidate(True)
		viewImagesSource.Invalidate(True)

		# 그래프 뷰를 갱신 # Update the Graph view.
		viewGraph.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while(viewImageLearnLowResolution.IsAvailable() and viewImageValidationLowResolution.IsAvailable() and viewImageLearnHighResolution.IsAvailable() and viewImageValidationHighResolution.IsAvailable() and viewImagesSource.IsAvailable() and viewGraph.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()')

if __name__ == '__main__':
    main()