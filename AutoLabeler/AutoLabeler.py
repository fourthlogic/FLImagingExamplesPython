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
	fliResultAutotLabelImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageValidation = CGUIViewImage()
	viewImagesAutoLabel = CGUIViewImage()
	
	# 그래프 뷰 선언 # Declare the graph view
	viewGraph = CGUIViewGraph()
	bTerminated = False

	while True:
		# 학습 이미지 로드 # Load the learn image
		if (res := fliLearnImage.Load('../../ExampleImages/SemanticSegmentation/Train.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 평가 이미지 로드 # Load the validation image
		if (res := fliValidationImage.Load('../../ExampleImages/SemanticSegmentation/Validation.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 평가 이미지 로드 # Load the validation image
		if (res := fliResultAutotLabelImage.Load('../../ExampleImages/SemanticSegmentation/Validation.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# learn 이미지 뷰 생성 # Create learn image view
		if (res := viewImageLearn.Create(100, 0, 600, 500)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if((res := viewImageValidation.Create(600, 0, 1100, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.")
			break

		if((res := viewImagesAutoLabel.Create(100, 500, 600, 1000)).IsFail()):
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

		if (res := viewImagesAutoLabel.SetImagePtr(fliResultAutotLabelImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		fliResultAutotLabelImage.ClearFigures()

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageValidation.SynchronizePointOfView(viewImagesAutoLabel)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImagesAutoLabel)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [0], ... [n-1] 형태로 tuple 을 반환한다. # A function that receives parameters returns a tuple structured as [return], [0], ... [n-1].
		if (res := viewImageLearn.SynchronizeWindow(viewImageValidation)[0]).IsFail():
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
		layerResultLabel = viewImagesAutoLabel.GetLayer(0)
	
		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLearn.Clear()
		layerValidation.Clear()
		layerResultLabel.Clear()

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

		if((res := layerResultLabel.DrawTextCanvas(flpPoint, "RESULT AUTO LABEL", EColor.YELLOW, EColor.BLACK, 30)).IsFail()):
			ErrorPrint(res, "Failed to draw text")
			break

		# 이미지 뷰를 갱신 # Update the image view.
		viewImageLearn.Invalidate(True)
		viewImageValidation.Invalidate(True)
		viewImagesAutoLabel.Invalidate(True)
		
		# SemanticSegmentation 객체 생성 # Create SemanticSegmentation object
		semanticSegmentationDL = CSemanticSegmentationDL()

		# OptimizerSpec 객체 생성 # Create OptimizerSpec object
		optSpec = COptimizerSpecAdamGradientDescent()

		# 학습할 이미지 설정 # Set the image to learn
		semanticSegmentationDL.SetLearningImage(fliLearnImage)
		# 검증할 이미지 설정 # Set the image to validation
		semanticSegmentationDL.SetLearningValidationImage(fliValidationImage)
		# 분류할 이미지 설정 # Set the image to classify
		semanticSegmentationDL.SetInferenceImage(fliValidationImage)
		semanticSegmentationDL.SetInferenceResultImage(fliResultAutotLabelImage)

		# 학습할 SemanticSegmentation 모델 설정 # Set up the SemanticSegmentation model to learn
		semanticSegmentationDL.SetModel(CSemanticSegmentationDL.EModel.FLSegNet)
		# 학습할 SemanticSegmentation 모델 Version 설정 # Set up the SemanticSegmentation model version to learn
		semanticSegmentationDL.SetModelVersion(CSemanticSegmentationDL.EModelVersion.FLSegNet_V1_512_B3)
		# 학습 epoch 값을 설정 # Set the learn epoch value 
		semanticSegmentationDL.SetLearningEpoch(120)
		# 학습 이미지 Interpolation 방식 설정 # Set Interpolation method of learn image
		semanticSegmentationDL.SetInterpolationMethod(EInterpolationMethod.Bilinear)

		# Optimizer의 학습률 설정 # Set learning rate of Optimizer
		optSpec.SetLearningRate(0.0001)

		# 설정한 Optimizer를 SemanticSegmentation에 적용 # Apply Optimizer that we set up to SemanticSegmentation
		semanticSegmentationDL.SetLearningOptimizerSpec(optSpec)
		
		# AugmentationSpec 설정 # Set the AugmentationSpec
		augSpec = CAugmentationSpec()

		augSpec.SetCommonActivationRate(0.5)
		augSpec.SetCommonInterpolationMethod(EInterpolationMethod.Bilinear)
		augSpec.EnableRotation(True)
		augSpec.SetRotationParam(-180.0, 180.0, False, True, 1.0)
		augSpec.EnableHorizontalFlip(True)
		augSpec.EnableVerticalFlip(True)
		augSpec.EnableGaussianNoise(True)
		semanticSegmentationDL.SetLearningAugmentationSpec(augSpec)

		semanticSegmentationDL.SetLearningAugmentationSpec(augSpec)

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

					# 이전 그래프의 데이터를 삭제 # Clear previous grpah data
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
		# 오토라벨러 객체 생성 # Create AutoLabelerDL Object
		autoLabelerDL = CAutoLabelerDL()

		# 오토라벨러에 모델을 로드 # Load model into autolabeler
		if((res := autoLabelerDL.Load(semanticSegmentationDL)[0]).IsFail()):
			ErrorPrint(res, "Failed to execute.")
			break

		# 파라미터 설정 # Parameter settings
		autoLabelerDL.SetSourceImage(fliResultAutotLabelImage)
		autoLabelerDL.EnableOverwriting(True)
		autoLabelerDL.EnableBatchProcessing(True)
		autoLabelerDL.SetLabelOptions(CAutoLabelerDL.ELabelOptions.None)
		autoLabelerDL.SetRegionFigureType(CAutoLabelerDL.ERegionFigureType.BoundaryRectangle)
		autoLabelerDL.SetMinimumScore(0.5)
		autoLabelerDL.SetMinimumArea(50.0)
		autoLabelerDL.SetMaximumArea(50000.0)

		# 알고리즘 수행 # Execute the algorithm
		if((res := autoLabelerDL.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute.")
			break

		# 결과 이미지를 이미지 뷰에 맞게 조정합니다. # Fit the result image to the image view.
		viewImagesAutoLabel.ZoomFit()

		# 이미지 뷰를 갱신 # Update the image view.
		viewImageLearn.RedrawWindow()
		viewImageValidation.RedrawWindow()
		viewImagesAutoLabel.RedrawWindow()
		
		# 그래프 뷰를 갱신 # Update the Graph view.
		viewGraph.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageLearn.IsAvailable() and viewImageValidation.IsAvailable() and viewImagesAutoLabel.IsAvailable() and viewGraph.IsAvailable():
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