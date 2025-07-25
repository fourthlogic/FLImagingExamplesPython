from FLImagingClrPy import *

CLibraryUtilities.Initialize()

def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

def main():
	# 이미지 객체 선언 // Declare the image object
	fliLearnImage = CFLImage()
	fliFindImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageFind = CGUIViewImage()

	res = CResult()

	while True:
		# 이미지 로드 // Load image
		res = fliLearnImage.Load("../../ExampleImages/Matching/Geometric Single Learn.flif")
		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		res = fliFindImage.Load("../../ExampleImages/Matching/Geometric Single Find.flif")
		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		# 이미지 뷰 생성 // Create image view
		if (res := viewImageLearn.Create(400, 0, 912, 384)).IsFail():
			ErrorPrint(res, "Failed to create the image view.")
			break

		if (res := viewImageFind.Create(912, 0, 1680, 576)).IsFail():
			ErrorPrint(res, "Failed to create the image view.")
			break

		# 이미지 뷰에 이미지를 디스플레이 // Display the image in the imageview
		if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.")
			break

		if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.")
			break

		# 이미지 뷰 윈도우 동기화 // Synchronize window positions
		if (res := viewImageLearn.SynchronizeWindow(viewImageFind)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window.")
			break

		layerLearn = viewImageLearn.GetLayer(0)
		layerFind = viewImageFind.GetLayer(1)

		layerLearn.Clear()
		layerFind.Clear()

		tpPosition00 = TPoint[Double](0, 0)

		if (res := layerLearn.DrawTextCanvas(tpPosition00, "LEARN", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, "Failed to draw text")
			break

		if (res := layerFind.DrawTextCanvas(tpPosition00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, "Failed to draw text")
			break

		# Geometric Match 객체 생성 // Create Geometric Match object
		geometricMatch = CGeometricMatch()

		# 학습할 이미지 설정 // Set the image to learn
		geometricMatch.SetLearnImage(fliLearnImage)

		# 학습할 영역을 설정합니다. // Set the area to learn.
		learnRegion = CFLRect[Double](110.77276, 97.42619, 747.46519, 752.33384)
		flpLearnPivot = CFLPoint[Double](learnRegion.GetCenter())
		geometricMatch.SetLearnROI(learnRegion)
		geometricMatch.SetLearnPivot(flpLearnPivot)

		# 학습 파라미터 설정 // Set the learning parameters
		# 추출할 특징점 개수를 설정합니다. // Set the number of feature points to be extracted.
		geometricMatch.SetFeatureCount(2048)
		#추출할 특징점 처리과정에서의 노이즈 필터링 정도를 설정합니다. // Set the noise filtering degree in the process of processing the feature points to be extracted.
		geometricMatch.SetFeatureFiltering(0.5)
		#추출할 특징점 처리과정에서의 허용 임계값을 설정합니다. // Set the allowable threshold in the feature point processing process to be extracted.
		geometricMatch.SetLearnThresholdCoefficient(1.0)

		# 알고리즘 수행 // Execute the algorithm
		if (res := geometricMatch.Learn()).IsFail():
			ErrorPrint(res, "Failed to execute Learn.")
			break

		# 학습 영역 디스플레이 // Display the learning region
		if (res := layerLearn.DrawFigureImage(learnRegion, EColor.BLACK, 3)).IsFail():
			ErrorPrint(res, "Failed to draw region border")
			break

		if (res := layerLearn.DrawFigureImage(learnRegion, EColor.CYAN)).IsFail():
			ErrorPrint(res, "Failed to draw region fill")
			break

		# 중심점 디스플레이 // Display the center point
		flfaPoint = flpLearnPivot.MakeCrossHair(3, False)

		if (res := layerLearn.DrawFigureImage(flfaPoint, EColor.BLACK, 3)).IsFail():
			ErrorPrint(res, "Failed to draw pivot figure")
			break

		if (res := layerLearn.DrawFigureImage(flfaPoint, EColor.LIME)).IsFail():
			ErrorPrint(res, "Failed to draw pivot figure")
			break

		# 학습한 특징점 디스플레이 // Display learned feature points
		flfaFeaturePoints = CFLFigureArray()

		res, flfaFeaturePoints = geometricMatch.GetLearnedFeature(flfaFeaturePoints);

		if res.IsFail():
			ErrorPrint(res, "Failed to get learned features.")
			break

		layerLearn.DrawFigureImage(flfaFeaturePoints, EColor.BLUE)

		# 학습 정보 출력 // Print learning info
		print(" ▷ Learn Information")
		print("  1. ROI Shape Type : Rectangle")
		print(f"    left   : {learnRegion.left}")
		print(f"    right  : {learnRegion.right}")
		print(f"    top    : {learnRegion.top}")
		print(f"    bottom : {learnRegion.bottom}")
		print(f"    angle  : {learnRegion.angle}")
		print(f"  2. Interest Pivot : ({flpLearnPivot.x}, {flpLearnPivot.y})")
		print("")

		# 검출 이미지 설정 // Set source image
		geometricMatch.SetSourceImage(fliFindImage)

		# 검출 파라미터 설정 // Set matching parameters
		# 검출 시 사용될 파라미터를 설정합니다. // Set the parameters to be used for detection.
		# 검출 시 사용될 기본 각도를 설정합니다. // Set the default angle to be used for detection.
		geometricMatch.SetAngleBias(0.0);
		# 검출 시 사용될 각도의 탐색범위를 설정합니다. // Set the search range of the angle to be used for detection.
		# 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 // The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
		geometricMatch.SetAngleTolerance(180.0);
		# 검출 시 사용될 스케일 탐색범위를 설정합니다. // Set the scale search range to be used for detection.
		geometricMatch.SetScaleRange(0.98, 1.02);
		# 검출 시 사용될 최소 탐색점수를 설정합니다. // Set the minimum search score to be used for detection.
		geometricMatch.SetMinimumDetectionScore(0.7);
		# 검출 시 사용될 최대 탐색객체 수를 설정합니다. // Set the maximum number of search objects to be used for detection.
		geometricMatch.SetMaxObject(5);		
		# 검출 시 보간법 사용 유무에 대해 설정합니다. // Set whether to use interpolation when detecting.
		geometricMatch.EnableInterpolation(True);
		# 검출 시 최적화 정도에 대해 설정합니다. // Set the degree of optimization for detection.
		geometricMatch.SetOptimizationOption(CGeometricMatch.EOptimizationOption.Fast);
		# 검출 시 대비정도에 대해 설정합니다. // Set the contrast level for detection.
		geometricMatch.SetContrastOption(EMatchContrastOption.Normal);
		# 검출 시 이미지 영역밖의 탐색 정도를 설정합니다. // Set the degree of search outside the image area when detecting.
		geometricMatch.SetInvisibleRegionEstimation(1.25);
		# 검출 시 처리과정에서의 허용 임계값을 설정합니다. // Set the allowable threshold in the process of detection.
		geometricMatch.SetFindThresholdCoefficient(1.0);
		# 검출 시 겹쳐짐 허용 정도를 설정합니다. // Set the allowable degree of overlap during detection.
		geometricMatch.SetObjectOverlap(0.5);

		# 알고리즘 수행 // Execute
		if (res := geometricMatch.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute")
			break

		# 결과 가져오기 // Get results
		i64ResultCount = geometricMatch.GetResultCount()
		print(" ▶ Find Information")

		for i in range(i64ResultCount):
			results = CGeometricMatch.SResult()
			flfaResultPoints = CFLFigureArray()

			geometricMatch.GetResult(i, results)
			geometricMatch.GetResultDetectedFeature(i, flfaResultPoints)

			f32Score = results.f32Score
			f32Angle = results.f32Angle
			f32Scale = results.f32Scale
			pFlfRegion = results.pFlfRegion
			flpPivot = results.pFlpPivot

			pFlrResultRegion = CFLRect[Double](pFlfRegion)

			print(f" < Instance : {i} >")
			print("  1. ROI Shape Type : Rectangle")
			print(f"    left   : {pFlrResultRegion.left}")
			print(f"    right  : {pFlrResultRegion.right}")
			print(f"    top    : {pFlrResultRegion.top}")
			print(f"    bottom : {pFlrResultRegion.bottom}")
			print(f"    angle  : {f32Angle:.3f}")
			print(f"  2. Interest Pivot : ({flpPivot.x}, {flpPivot.y})")
			print(f"  3. Score : {f32Score:.3f}\n  4. Angle : {f32Angle:.3f}\n  5. Scale : x{f32Scale:.3f}")

			# 결과 중심점 디스플레이 // Display center point
			flfaPointPivot = flpPivot.MakeCrossHair(3, False)
			flfaPointPivot.Rotate(f32Angle, flpPivot)

			if (res := layerFind.DrawFigureImage(flfaPointPivot, EColor.BLACK, 3)).IsFail():
				ErrorPrint(res, "Failed to draw result pivot")
				break

			if (res := layerFind.DrawFigureImage(flfaPointPivot, EColor.LIME)).IsFail():
				ErrorPrint(res, "Failed to draw result pivot")
				break

			tpPosition = TPoint[Double](flpPivot.x, flpPivot.y)
			strText = f"Score : {f32Score:.3f}\nAngle : {f32Angle:.3f}\nScale : x{f32Scale:.3f}\n"

			layerFind.DrawFigureImage(flfaResultPoints, EColor.LIME)

			if (res := layerFind.DrawTextImage(tpPosition, strText, EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)).IsFail():
				ErrorPrint(res, "Failed to draw result text")
				break

		# 이미지 뷰 갱신 // Update image view
		viewImageLearn.Invalidate(True)
		viewImageFind.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait until view closes
		while viewImageLearn.IsAvailable():
			CThreadUtilities.Sleep(1)

		break

if __name__ == "__main__":
	main()
