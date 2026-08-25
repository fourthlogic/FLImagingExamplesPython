from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


def ErrorPrint(res: CResult, message: str):
	if len(message) > 1:
		print(message)
	print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")

def main():
	# 이미지 객체 선언 # Declare the image object
	fliLearnImage = [CFLImage() for _ in range(3)]
	fliFindImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = [CGUIViewImage() for _ in range(3)]
	viewImageFind = CGUIViewImage()

	# Geometric Match Multi 객체 생성 # Create Geometric Match Multi object
	geometricMatchMulti = CGeometricMatchMulti()

	res = CResult()

	do_once = True
	while do_once:
		do_once = False

		arrPath = [
			"../../ExampleImages/Matching/Geometric Multi Learn.flif",
			"../../ExampleImages/Matching/Geometric Multi Learn.flif",
			"../../ExampleImages/Matching/Geometric Multi Learn.flif",
		]

		arrClassName = ["A", "B", "C"]

		arrColor = [EColor.LIME, EColor.RED, EColor.CYAN]

		print(" ▷ Learn Information")

		for i in range(3):
			# 이미지 로드 # Load image
			if fliLearnImage[i].Load(arrPath[i]).IsFail():
				break

			# 이미지 뷰 생성 # Create image view
			if (res := viewImageLearn[i].Create(400 + 512 * i, 0, 400 + 512 * (i + 1), 384)).IsFail():
				ErrorPrint(res, "Failed to create image view.")
				break

			# 이미지 뷰에 이미지를 디스플레이 # Display the image in the imageview
			if (res := viewImageLearn[i].SetImagePtr(fliLearnImage[i])[0]).IsFail():
				ErrorPrint(res, "Failed to set image.")
				break

			layerLearn = viewImageLearn[i].GetLayer(0)
			layerLearn.Clear()

			# 학습 이미지 설정 # Set learning image
			geometricMatchMulti.SetLearnImage(fliLearnImage[i])

			# 학습할 영역 설정 # Set the area to learn
			learnRegion = CFLRect[Double]()
			if i == 0:
				learnRegion.Set(402.23622, 165.22834, 541.73228, 610.803149)
			elif i == 1:
				learnRegion.Set(257.32283, 476.72440, 396.81889, 688.00)
			else:
				learnRegion.Set(549.85826, 476.72440, 689.35433, 688.00)

			flpLearnPivot = CFLPoint[Double](learnRegion.GetCenter())
			geometricMatchMulti.SetLearnROI(learnRegion)
			geometricMatchMulti.SetLearnPivot(flpLearnPivot)

			# 학습 파라미터 설정 # Set the learning parameters
			# 추출할 특징점 개수를 설정합니다. # Set the number of feature points to be extracted.
			geometricMatchMulti.SetFeatureCount(2048)
			#추출할 특징점 처리과정에서의 노이즈 필터링 정도를 설정합니다. # Set the noise filtering degree in the process of processing the feature points to be extracted.
			geometricMatchMulti.SetFeatureFiltering(0.5)
			#추출할 특징점 처리과정에서의 허용 임계값을 설정합니다. # Set the allowable threshold in the feature point processing process to be extracted.
			geometricMatchMulti.SetLearnThresholdCoefficient(1.3)

			# 알고리즘 수행 # Execute the algorithm
			if geometricMatchMulti.Learn(arrClassName[i]).IsFail():
				ErrorPrint(res, "Failed to learn.")
				break

			if (res := layerLearn.DrawFigureImage(learnRegion, EColor.BLACK, 3)).IsFail():
				ErrorPrint(res, "Failed to draw region.")
				break
			layerLearn.DrawFigureImage(learnRegion, arrColor[i])

			flfaPointPivot = flpLearnPivot.MakeCrossHair(3, False)
			layerLearn.DrawFigureImage(flfaPointPivot, EColor.BLACK, 3)
			layerLearn.DrawFigureImage(flfaPointPivot, EColor.LIME)

			# 학습한 특징점 디스플레이 # Display learned feature points
			flfaFeaturePoints = CFLFigureArray()
			geometricMatchMulti.GetLearnedFeature(flfaFeaturePoints)
			layerLearn.DrawFigureImage(flfaFeaturePoints, arrColor[i])

			strStatus = f"LEARN CLASS {arrClassName[i]}"
			flpPosition00 = CFLPoint[Double](0, 0)
			layerLearn.DrawTextCanvas(flpPosition00, strStatus, EColor.YELLOW, EColor.BLACK, 30)

			print(f"  < LEARN CLASS {arrClassName[i]} > ")
			print("  1. ROI Shape Type : Rectangle")
			print(f"    left   : {learnRegion.left}")
			print(f"    right  : {learnRegion.right}")
			print(f"    top    : {learnRegion.top}")
			print(f"    bottom : {learnRegion.bottom}")
			print(f"    angle  : {learnRegion.angle}")
			print(f"  2. Interest Pivot : ({flpLearnPivot.x}, {flpLearnPivot.y})\n")

			viewImageLearn[i].Invalidate(True)


		# 학습 데이터 저장 # Learn data save
		if (res := geometricMatchMulti.Save("../../ExampleImages/Matching/Geometric Multi Learn")).IsFail():
			ErrorPrint(res, "Failed to save")
			break

		# 검출 이미지 로드 및 뷰 설정 # Load find image and setup view
		if (res := fliFindImage.Load("../../ExampleImages/Matching/Geometric Multi Find.flif")).IsFail():
			ErrorPrint(res, "Failed to load find image.")
			break

		if (res := viewImageFind.Create(400, 384, 1168, 960)).IsFail():
			ErrorPrint(res, "Failed to create find view.")
			break

		if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set find image.")
			break

		for i in range(3):
			viewImageFind.SynchronizeWindow(viewImageLearn[i])

		layerFind = viewImageFind.GetLayer(1)
		layerFind.Clear()

		if (res := layerFind.DrawTextCanvas(CFLPoint[Double](0, 0), "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, "Failed to draw text")
			break

		# 학습 데이터 로드 # Learn data Load
		if (res := geometricMatchMulti.Load("../../ExampleImages/Matching/Geometric Multi Learn")).IsFail():
			ErrorPrint(res, "Failed to Load")
			break

		# 검출 파라미터 설정 # Set matching parameters
		# 검출 이미지 설정 # Set source image
		geometricMatchMulti.SetSourceImage(fliFindImage)
		# 검출 파라미터 설정 # Set matching parameters
		# 검출 시 사용될 파라미터를 설정합니다. # Set the parameters to be used for detection.
		# 검출 시 사용될 기본 각도를 설정합니다. # Set the default angle to be used for detection.
		geometricMatchMulti.SetAngleBias(0.0)
		# 검출 시 사용될 각도의 탐색범위를 설정합니다. # Set the search range of the angle to be used for detection.
		# 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 # The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
		geometricMatchMulti.SetAngleTolerance(180.0)
		# 검출 시 사용될 스케일 탐색범위를 설정합니다. # Set the scale search range to be used for detection.
		geometricMatchMulti.SetScaleRange(0.98, 1.02)
		# 검출 시 사용될 최소 탐색점수를 설정합니다. # Set the minimum search score to be used for detection.
		geometricMatchMulti.SetMinimumDetectionScore(0.5)
		# 검출 시 사용될 탐색 방식을 설정합니다. # Set the search method to be used for detection.
		geometricMatchMulti.SetMaxObjectMode(CGeometricMatchMulti.EMaxObjectMode.Total)
		# 검출 시 사용될 최대 탐색객체 수를 설정합니다. # Set the maximum number of search objects to be used for detection.
		geometricMatchMulti.SetMaxObjectTotal(16)		
		# 검출 시 보간법 사용 유무에 대해 설정합니다. # Set whether to use interpolation when detecting.
		geometricMatchMulti.EnableInterpolation(True)
		# 검출 시 최적화 정도에 대해 설정합니다. # Set the degree of optimization for detection.
		geometricMatchMulti.SetOptimizationOption(CGeometricMatchMulti.EOptimizationOption.Fastest)
		# 검출 시 대비정도에 대해 설정합니다. # Set the contrast level for detection.
		geometricMatchMulti.SetContrastOption(EMatchContrastOption.Normal)
		# 검출 시 이미지 영역밖의 탐색 정도를 설정합니다. # Set the degree of search outside the image area when detecting.
		geometricMatchMulti.SetInvisibleRegionEstimation(1.25)
		# 검출 시 처리과정에서의 허용 임계값을 설정합니다. # Set the allowable threshold in the process of detection.
		geometricMatchMulti.SetFindThresholdCoefficient(1.0)
		# 검출 시 겹쳐짐 허용 정도를 설정합니다. # Set the allowable degree of overlap during detection.
		geometricMatchMulti.SetObjectOverlap(0.8)

		# 알고리즘 수행 # Execute the Algoritm
		if geometricMatchMulti.Execute().IsFail():
			ErrorPrint(res, "Failed to execute match.")
			break

		# 기하학적 패턴 검출 결과를 가져옵니다. # Get the geometric pattern detection result.
		i64ResultCount = geometricMatchMulti.GetResultCount()

		for i in range(i64ResultCount):
			result = CGeometricMatchMulti.SResult()
			flfaResultPoints = CFLFigureArray()
			geometricMatchMulti.GetResult(i, result)
			geometricMatchMulti.GetResultDetectedFeature(i, flfaResultPoints)

			className = result.pStrClassName
			flr = CFLRect[Double](result.pFlfRegion)
			flp = CFLPoint[Double](result.pFlpPivot)

			# 색상 인덱스 찾기 # Find color index
			idx = arrClassName.index(className)

			# 기하학적 패턴 검출 결과를 Console창에 출력합니다. # Output the geometric pattern detection result to the console window.
			print(f" < Instance : {i} >")
			print(f" Class Name : {className}")
			print("  1. ROI Shape Type : Rectangle")
			print(f"    left   : {flr.left}")
			print(f"    right  : {flr.right}")
			print(f"    top    : {flr.top}")
			print(f"    bottom : {flr.bottom}")
			print(f"    angle  : {flr.angle}")
			print(f"  2. Interest Pivot : ({flp.x}, {flp.y})")
			print(f"  3. Score : {result.f32Score:.3f}\n  4. Angle : {result.f32Angle:.3f}\n  5. Scale : x{result.f32Scale:.3f}\n")

			# 검출 결과의 중심점을 디스플레이 한다 # Display the center point of the detection result // Display the center point of the detection result
			flfaPoint = flp.MakeCrossHair(3, False)
			flfaPoint.Rotate(result.f32Angle, flp)
			layerFind.DrawFigureImage(flfaPoint, EColor.BLACK, 3)
			layerFind.DrawFigureImage(flfaPoint, EColor.LIME)

			tp = TPoint[Double](flp.x + 10, flp.y)

			# 결과 특징점을 디스플레이 한다 # Display the resulting feature point
			layerFind.DrawFigureImage(flfaResultPoints, arrColor[idx])
			layerFind.DrawTextImage(tp, f"Score : {result.f32Score:.3f}\nAngle : {result.f32Angle:.3f}\nScale : x{result.f32Scale:.3f}", EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)

			tp.x -= 10
			layerFind.DrawTextImage(tp, className, EColor.YELLOW, EColor.BLACK, 30, False, 0, EGUIViewImageTextAlignment.CENTER)

			viewImageFind.Invalidate(True)

		# 이미지 뷰 종료까지 대기 # Wait for window close
		while viewImageLearn[0].IsAvailable():
			CThreadUtilities.Sleep(1)

		for i in range(3):
			viewImageLearn[i].Destroy()

		viewImageFind.Destroy()

if __name__ == '__main__':
	main()
