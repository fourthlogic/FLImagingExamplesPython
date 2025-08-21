from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)
	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

def main():
	# 이미지 객체 선언 # Declare the image object
	fliFindImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLearn = CGUIViewImage()
	viewImageFind = CGUIViewImage()

	# 이미지 로드 # Load image
	res = fliFindImage.Load("../../ExampleImages/Matching/DrawingImage.flif")
	if res.IsFail():
		ErrorPrint(res, "Failed to load the image file.")
		return

	# 이미지 뷰 생성 # Create image views
	if (res := viewImageLearn.Create(400, 0, 912, 384)).IsFail():
		ErrorPrint(res, "Failed to create the image view.")
		return

	if (res := viewImageFind.Create(912, 0, 1680, 576)).IsFail():
		ErrorPrint(res, "Failed to create the image view.")
		return

	# 이미지 디스플레이 # Display image in the imageview
	if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
		ErrorPrint(res, "Failed to set image object on the image view.")
		return

	# 이미지 뷰 윈도우 동기화 # Synchronize window positions
	if (res := viewImageLearn.SynchronizeWindow(viewImageFind)[0]).IsFail():
		ErrorPrint(res, "Failed to synchronize window.")
		return

	layerLearn = viewImageLearn.GetLayer(0)
	layerFind = viewImageFind.GetLayer(1)

	layerLearn.Clear()
	layerFind.Clear()

	# 텍스트 출력 # Draw labels
	tpPosition00 = TPoint[Double](0, 0)

	if (res := layerLearn.DrawTextCanvas(tpPosition00, "LEARN", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
		ErrorPrint(res, "Failed to draw text")
		return

	if (res := layerFind.DrawTextCanvas(tpPosition00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
		ErrorPrint(res, "Failed to draw text")
		return

	# 도면 매칭 객체 생성 # Create drawing match object
	drawingMatch = CDrawingMatch()

	pFlfDrawing = CFLFigureArray()
	pFlfDrawing.Load("../../ExampleImages/Matching/Drawing.fig")

	# 학습 설정 # Set drawing and learning parameters
	drawingMatch.SetDrawing(pFlfDrawing)
	drawingMatch.SetDistanceUnit(CDrawingMatch.EDistanceUnit.Millimeter)
	drawingMatch.SetPixelAccuracy(1.0, 1.0)
	drawingMatch.SetFeatureCount(10000)
	drawingMatch.SetFeatureFiltering(0.0)
	drawingMatch.SetLearnThresholdCoefficient(1.0)

	# 학습 실행 # Execute learning
	if (res := drawingMatch.Learn()).IsFail():
		ErrorPrint(res, "Failed to execute Learn.")
		return

	# 학습된 특징 디스플레이 # Display learned drawing
	flfLearnedDrawing = drawingMatch.GetLearnedDrawing()
	layerLearn.DrawFigureImage(flfLearnedDrawing, EColor.BLUE)

	# 소스 이미지 설정 # Set image to detect
	drawingMatch.SetSourceImage(fliFindImage)

	# 검출 파라미터 설정 # Detection parameters

	# 검출 시 사용될 기본 각도를 설정합니다. # Set the default angle to be used for detection.
	drawingMatch.SetAngleBias(0.0)
	# 검출 시 사용될 각도의 탐색범위를 설정합니다. # Set the search range of the angle to be used for detection.
	# 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 # The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
	drawingMatch.SetAngleTolerance(5)
	# 검출 시 사용될 스케일 탐색범위를 설정합니다. # Set the scale search range to be used for detection.
	drawingMatch.SetScaleRange(0.9, 1.1)
	# 검출 시 사용될 최소 탐색점수를 설정합니다. # Set the minimum search score to be used for detection.
	drawingMatch.SetMinimumDetectionScore(0.5)
	# 검출 시 사용될 최대 탐색객체 수를 설정합니다. # Set the maximum number of search objects to be used for detection.
	drawingMatch.SetMaxObject(1)
	# 검출 시 보간법 사용 유무에 대해 설정합니다. # Set whether to use interpolation when detecting.
	drawingMatch.EnableInterpolation(True)
	# 검출 시 최적화 정도에 대해 설정합니다. # Set the degree of optimization for detection.
	drawingMatch.SetOptimizationOption(CGeometricMatch.EOptimizationOption.Fast)
	# 검출 시 대비정도에 대해 설정합니다. # Set the contrast level for detection.
	drawingMatch.SetContrastOption(EMatchContrastOption.Any)
	# 검출 시 이미지 영역밖의 탐색 정도를 설정합니다. # Set the degree of search outside the image area when detecting.
	drawingMatch.SetInvisibleRegionEstimation(1.25)
	# 검출 시 처리과정에서의 허용 임계값을 설정합니다. # Set the allowable threshold in the process of detection.
	drawingMatch.SetFindThresholdCoefficient(1.2)
	# 검출 시 겹쳐짐 허용 정도를 설정합니다. # Set the allowable degree of overlap during detection.
	drawingMatch.SetObjectOverlap(0.5)

	# 알고리즘 실행 # Execute detection
	if (res := drawingMatch.Execute()).IsFail():
		ErrorPrint(res, "Failed to execute detection.")
		return

	# 결과 출력 및 디스플레이 # Print and display results

	# 기하학적 패턴 검출 결과를 가져옵니다. # Get the geometric pattern detection result.
	resultCount = drawingMatch.GetResultCount()
	print(" ▶ Find Information")

	for i in range(resultCount):
		result = CGeometricMatch.SResult()
		drawingMatch.GetResult(i, result)

		score = result.f32Score
		angle = result.f32Angle
		scale = result.f32Scale
		region = result.pFlfRegion
		location = result.pFlpLocation
		pivot = result.pFlpPivot
		boundary = region.GetBoundaryRect()

		# 기하학적 패턴 검출 결과를 Console창에 출력합니다. # Output the geometric pattern detection result to the console window.
		print(f" < Instance : {i} >")
		print(f"  1. ROI Shape Type : Rectangle")
		print(f"    left   : {boundary.left}")
		print(f"    right  : {boundary.right}")
		print(f"    top    : {boundary.top}")
		print(f"    bottom : {boundary.bottom}")
		print(f"    angle  : {angle}")
		print(f"  2. Interest Pivot : ({pivot.x}, {pivot.y})")
		print(f"  3. Score : {score:.3f}\n  4. Angle : {angle:.3f}\n  5. Scale : x{scale:.3f}")

		# 중심점 표시 # Draw pivot
		crossHair = pivot.MakeCrossHair(3, False)
		crossHair.Rotate(angle, pivot)
		if (res := layerFind.DrawFigureImage(crossHair, EColor.BLACK, 3)).IsFail():
			ErrorPrint(res, "Failed to draw figure")
			return
		if (res := layerFind.DrawFigureImage(crossHair, EColor.LIME)).IsFail():
			ErrorPrint(res, "Failed to draw figure")
			return

		# 특징점 및 텍스트 표시 # Draw features and text
		layerFind.DrawFigureImage(region, EColor.CYAN)
		pos = TPoint[Double](pivot.x, pivot.y)
		text = f"Score : {score:.3f}\nAngle : {angle:.3f}\nScale : x{scale:.3f}\n"

		if (res := layerFind.DrawTextImage(pos, text, EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)).IsFail():
			ErrorPrint(res, "Failed to draw text")
			return

	# 뷰 갱신 # Refresh views
	viewImageLearn.ZoomFitToLayer(0)
	viewImageLearn.Invalidate(True)
	viewImageFind.Invalidate(True)

	# 뷰 종료 대기 # Wait for view to close
	while viewImageLearn.IsAvailable():
		CThreadUtilities.Sleep(1)

if __name__ == "__main__":
	main()
