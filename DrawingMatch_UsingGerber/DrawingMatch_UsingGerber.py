from FLImagingClrPy import *

def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")

def main():
    # 이미지 객체 선언 // Declare the image object
    fliFindImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageLearn = CGUIViewImage()
    viewImageFind = CGUIViewImage()

    # 이미지 파일 로드 // Load the image file
    if (res := fliFindImage.Load("../../ExampleImages/Matching/DrawingImage.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.")
        return

    # 이미지 뷰 생성 // Create image view
    if (res := viewImageLearn.Create(400, 0, 912, 384)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    if (res := viewImageFind.Create(912, 0, 1680, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    # 이미지 뷰에 이미지 디스플레이 // Display image in the image view
    if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        return

    # 이미지 뷰 동기화 // Synchronize window positions
    if (res := viewImageLearn.SynchronizeWindow(viewImageFind)[0]).IsFail():
        ErrorPrint(res, "Failed to synchronize window.")
        return

    # 각 뷰의 레이어 가져오기 // Get layers of the views
    layerLearn = viewImageLearn.GetLayer(0)
    layerFind = viewImageFind.GetLayer(1)

    # 레이어 초기화 // Clear previous drawings
    layerLearn.Clear()
    layerFind.Clear()

    pos0 = TPoint[Double](0, 0)

    # 텍스트 표시 // Draw "LEARN" and "FIND"
    if (res := layerLearn.DrawTextCanvas(pos0, "LEARN", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text")
        return

    if (res := layerFind.DrawTextCanvas(pos0, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text")
        return

    # 도면 매칭 객체 생성 // Create DrawingMatch object
    drawingMatch = CDrawingMatch()

    # 학습할 도면을 설정합니다. // Set the drawing to learn.
    drawingMatch.SetDrawing("../../ExampleImages/Matching/Drawing.gbr")
    # 도면에 대한 분해능 단위를 설정합니다. // Set unit of pixel accuracy.
    drawingMatch.SetDistanceUnit(CDrawingMatch.EDistanceUnit.Millimeter)
    # 도면에 대한 분해능을 설정합니다. // Set pixel accuracy.
    drawingMatch.SetPixelAccuracy(0.05, 0.05)

    # 특징점 추출 파라미터 설정 // Set feature extraction parameters
    # 추출할 특징점 개수를 설정합니다. // Set the number of feature points to be extracted.
    drawingMatch.SetFeatureCount(10000)
    # 추출할 특징점 처리과정에서의 노이즈 필터링 정도를 설정합니다. // Set the noise filtering degree in the process of processing the feature points to be extracted.
    drawingMatch.SetFeatureFiltering(0.0)
    # 추출할 특징점 처리과정에서의 허용 임계값을 설정합니다. // Set the allowable threshold in the feature point processing process to be extracted.
    drawingMatch.SetLearnThresholdCoefficient(1.0)

    # 학습 수행 // Execute learning
    if (res := drawingMatch.Learn()).IsFail():
        ErrorPrint(res, "Failed to execute Learn.")
        return

    # 학습된 도형 표시 // Display learned figure
    flfLearnedDrawing = drawingMatch.GetLearnedDrawing()
    layerLearn.DrawFigureImage(flfLearnedDrawing, EColor.BLUE)

    # 검출용 이미지 설정 // Set source image
    drawingMatch.SetSourceImage(fliFindImage)
    
    # 검출 시 사용될 기본 각도를 설정합니다. // Set the default angle to be used for detection.
    drawingMatch.SetAngleBias(0.0)
    # 검출 시 사용될 각도의 탐색범위를 설정합니다. // Set the search range of the angle to be used for detection.
    # 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 // The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
    drawingMatch.SetAngleTolerance(5)
    # 검출 시 사용될 스케일 탐색범위를 설정합니다. // Set the scale search range to be used for detection.
    drawingMatch.SetScaleRange(0.9, 1.1)
    # 검출 시 사용될 최소 탐색점수를 설정합니다. // Set the minimum search score to be used for detection.
    drawingMatch.SetMinimumDetectionScore(0.5)
    # 검출 시 사용될 최대 탐색객체 수를 설정합니다. // Set the maximum number of search objects to be used for detection.
    drawingMatch.SetMaxObject(1)
    # 검출 시 보간법 사용 유무에 대해 설정합니다. // Set whether to use interpolation when detecting.
    drawingMatch.EnableInterpolation(True)
    # 검출 시 최적화 정도에 대해 설정합니다. // Set the degree of optimization for detection.
    drawingMatch.SetOptimizationOption(CGeometricMatch.EOptimizationOption.Fast)
    # 검출 시 대비정도에 대해 설정합니다. // Set the contrast level for detection.
    drawingMatch.SetContrastOption(EMatchContrastOption.Any)
    # 검출 시 이미지 영역밖의 탐색 정도를 설정합니다. // Set the degree of search outside the image area when detecting.
    drawingMatch.SetInvisibleRegionEstimation(1.25)
    # 검출 시 처리과정에서의 허용 임계값을 설정합니다. // Set the allowable threshold in the process of detection.
    drawingMatch.SetFindThresholdCoefficient(1.2)
    # 검출 시 겹쳐짐 허용 정도를 설정합니다. // Set the allowable degree of overlap during detection.
    drawingMatch.SetObjectOverlap(0.5)

    # 검출 알고리즘 실행 // Execute detection
    if (res := drawingMatch.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute")
        return

    # 결과 수집 및 출력 // Collect and display results
    count = drawingMatch.GetResultCount()
    print(" ▶ Find Information")

    for i in range(count):
        result = CGeometricMatch.SResult()
        drawingMatch.GetResult(i, result)

        score = result.f32Score
        angle = result.f32Angle
        scale = result.f32Scale
        region = result.pFlfRegion
        pivot = result.pFlpPivot

        bound = region.GetBoundaryRect()

        print(f" < Instance : {i} >")
        print(f"  1. ROI Shape Type : Rectangle")
        print(f"    left   : {bound.left}")
        print(f"    right  : {bound.right}")
        print(f"    top    : {bound.top}")
        print(f"    bottom : {bound.bottom}")
        print(f"    angle  : {angle}")
        print(f"  2. Interest Pivot : ({pivot.x}, {pivot.y})")
        print(f"  3. Score : {score:.3f}\n  4. Angle : {angle:.3f}\n  5. Scale : x{scale:.3f}")

        # 중심점 표시 // Draw center point crosshair
        cross = pivot.MakeCrossHair(3, False)
        cross.Rotate(angle, pivot)

        if (res := layerFind.DrawFigureImage(cross, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break
        if (res := layerFind.DrawFigureImage(cross, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        pos = TPoint[Double](pivot.x, pivot.y)
        text = f"Score : {score:.3f}\nAngle : {angle:.3f}\nScale : x{scale:.3f}\n"

        layerFind.DrawFigureImage(region, EColor.CYAN)
        if (res := layerFind.DrawTextImage(pos, text, EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

    # 이미지 뷰 갱신 // Refresh image view
    viewImageLearn.ZoomFitToLayer(0)
    viewImageLearn.Invalidate(True)
    viewImageFind.Invalidate(True)

    # 이미지 뷰 종료 대기 // Wait until view closed
    while viewImageLearn.IsAvailable():
        CThreadUtilities.Sleep(1)

if __name__ == "__main__":
    main()
