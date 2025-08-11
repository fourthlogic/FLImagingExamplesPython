from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 경고 코드 // Error print function
def ErrorPrint(res: CResult, msg: str):
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
    input()

# 이미지 객체 선언 // Declare the image object
fliLearnImage = [CFLImage(), CFLImage()]
fliFindImage = CFLImage()

# 이미지 뷰 선언 // Declare the image view
viewImageLearn = [CGUIViewImage(), CGUIViewImage()]
viewImageFind = CGUIViewImage()

res = CResult()

# Pattern Match Multi 객체 생성 // Create Pattern Match Multi object
patternMatchMultiSparseSave = CPatternMatchMultiSparse()
FLPatternMatchMultiSparseLoad = CPatternMatchMultiSparse()

while True:
    arrPath = ["../../ExampleImages/Matching/Pattern2 Single Learn.flif",
               "../../ExampleImages/Matching/Pattern2 Single Learn.flif"]

    arrClassName = ["A", "B"]
    arrColor = [EColor.LIME, EColor.RED]

    arrLearnRegion = [CFLRect[Double](326.6913, 372.2960, 477.5354, 521.5354),
                      CFLRect[Double](586.7185, 566.3427, 763.2982, 672.1134)]

    for i64DataIdx in range(2):
        # 이미지 로드 // Load image
        if (res := fliLearnImage[i64DataIdx].Load(arrPath[i64DataIdx])).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImageLearn[i64DataIdx].Create(int(400 + 512 * i64DataIdx), 0, int(400 + 512 * (i64DataIdx + 1)), 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
        if (res := viewImageLearn[i64DataIdx].SetImagePtr(fliLearnImage[i64DataIdx])[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        layerLearn = viewImageLearn[i64DataIdx].GetLayer(0)
        layerLearn.Clear()

        # 학습할 이미지 설정 // Set the image to learn
        patternMatchMultiSparseSave.SetLearnImage(fliLearnImage[i64DataIdx])

        # 학습할 영역을 설정합니다. // Set the area to learn.
        flpLearnPivot = CFLPoint[Double](arrLearnRegion[i64DataIdx].GetCenter())
        patternMatchMultiSparseSave.SetLearnROI(arrLearnRegion[i64DataIdx])
        patternMatchMultiSparseSave.SetLearnPivot(flpLearnPivot)
        patternMatchMultiSparseSave.SetSampleCount(256)

        # 알고리즘 수행 // Execute the Algorithm
        if (res := patternMatchMultiSparseSave.Learn(arrClassName[i64DataIdx])).IsFail():
            ErrorPrint(res, "Failed to Learn.")
            break

        # 측정 영역 디스플레이 // Display measurement area
        if (res := layerLearn.DrawFigureImage(arrLearnRegion[i64DataIdx], EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break
        if (res := layerLearn.DrawFigureImage(arrLearnRegion[i64DataIdx], arrColor[i64DataIdx])).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        # 중심점 디스플레이 // Display pivot point
        flfaPointPivot = flpLearnPivot.MakeCrossHair(3, False)
        if (res := layerLearn.DrawFigureImage(flfaPointPivot, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break
        if (res := layerLearn.DrawFigureImage(flfaPointPivot, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        strStatus = f"LEARN CLASS {arrClassName[i64DataIdx]}"
        flpPosition00 = CFLPoint[Double](0, 0)
        if (res := layerLearn.DrawTextCanvas(flpPosition00, strStatus, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        # 학습한 정보 출력 // Print learned info
        print(f"  < LEARN CLASS {arrClassName[i64DataIdx]} > ")
        print("  1. ROI Shape Type : Rectangle")
        print(f"    left   : {arrLearnRegion[i64DataIdx].left}")
        print(f"    right  : {arrLearnRegion[i64DataIdx].right}")
        print(f"    top    : {arrLearnRegion[i64DataIdx].top}")
        print(f"    bottom : {arrLearnRegion[i64DataIdx].bottom}")
        print(f"    angle  : {arrLearnRegion[i64DataIdx].angle}")
        print(f"  2. Interest Pivot : ({flpLearnPivot.x}, {flpLearnPivot.y})\n")

        # 이미지 뷰 갱신 // Update image view
        viewImageLearn[i64DataIdx].Invalidate(True)

    # Save 학습 데이터 저장 // Save learned data
    if (res := patternMatchMultiSparseSave.Save("../../ExampleImages/Matching/Pattern Multi Learn")).IsFail():
        ErrorPrint(res, "Failed to save\n")
        break

    # 이미지 로드 // Load image
    if (res := fliFindImage.Load("../../ExampleImages/Matching/Pattern2 Single Find2.flif")).IsFail():
        ErrorPrint(res, "Failed to load\n")
        break

    # 이미지 뷰 생성 // Create image view
    if (res := viewImageFind.Create(400, 384, 1168, 960)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        break

    # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
    if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        break

    for i64DataIdx in range(2):
        if (res := viewImageFind.SynchronizeWindow(viewImageLearn[i64DataIdx])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

    layerFind = viewImageFind.GetLayer(1)
    layerFind.Clear()

    flp00 = CFLPoint[Double](0, 0)
    if (res := layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text")
        break

    if (res := FLPatternMatchMultiSparseLoad.Load("../../ExampleImages/Matching/Pattern Multi Learn")).IsFail():
        ErrorPrint(res, "Failed to load\n")
        break

    # 검출할 이미지 설정 // Set image to detect
    FLPatternMatchMultiSparseLoad.SetSourceImage(fliFindImage)
    # 검출 시 사용될 파라미터를 설정합니다. // Set the parameters to be used for detection.
    # 검출 시 사용될 기본 각도를 설정합니다. // Set the default angle to be used for detection.
    FLPatternMatchMultiSparseLoad.SetAngleBias(0.0)
    # 검출 시 사용될 각도의 탐색범위를 설정합니다. // Set the search range of the angle to be used for detection.
    # 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 // The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
    FLPatternMatchMultiSparseLoad.SetAngleTolerance(15.0)
    # 검출 시 최적화 정도를 설정합니다. // Set the degree of optimization for detection.
    # 검출 시 사용될 최소 탐색점수를 설정합니다. // Set the minimum search score to be used for detection.
    FLPatternMatchMultiSparseLoad.SetMinimumDetectionScore(0.7)
    # 검출 시 사용될 탐색 방식을 설정합니다. // Set the search method to be used for detection.
    FLPatternMatchMultiSparseLoad.SetMaxObjectMode(CPatternMatchMultiSparse.EMaxObjectMode.Total)
    # 검출 시 사용될 최대 탐색객체 수를 설정합니다. // Set the maximum number of search objects to be used for detection.
    FLPatternMatchMultiSparseLoad.SetMaxObjectTotal(2)
    # 검출 시 보간법 사용 유무에 대해 설정합니다. // Set whether to use interpolation when detecting.
    FLPatternMatchMultiSparseLoad.EnableInterpolation(True)
    # 검출 시 서로 다른 클래스에 대해 영역 중복을 허용 유무에 대해 설정합니다. // Set whether to allow area overlap for different classes during detection.
    FLPatternMatchMultiSparseLoad.SetConflictDetectionMethod(CPatternMatchMultiSparse.EConflictDetectionMethod.HighestScore)


    # 알고리즘 수행 // Execute the Algorithm
    if (res := FLPatternMatchMultiSparseLoad.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute")
        break

    i64ResultCount = FLPatternMatchMultiSparseLoad.GetResultCount()

    for i in range(i64ResultCount):
        results = CPatternMatchMultiSparse.SResult()
        FLPatternMatchMultiSparseLoad.GetResult(i, results)

        f32Score = results.f32Score
        f32Angle = results.f32Angle
        f32Scale = results.f32Scale
        flpPivot = CFLPoint[Double](results.pFlpPivot)
        pFlfRegion = CFLRect[Double](results.pFlfRegion)
        flrResultRegion = CFLRect[Double](pFlfRegion)
        wstrClassName = results.pStrClassName

        i64Idx = 0
        for i64ResultIndex in range(3):
            if wstrClassName == arrClassName[i64ResultIndex]:
                i64Idx = i64ResultIndex
                break

        # 결과 출력 // Print results
        print(f" < Instance : {i} >")
        print(f" Class Name : {wstrClassName}")
        print("  1. ROI Shape Type : Rectangle")
        print(f"    left   : {flrResultRegion.left}")
        print(f"    right  : {flrResultRegion.right}")
        print(f"    top    : {flrResultRegion.top}")
        print(f"    bottom : {flrResultRegion.bottom}")
        print(f"    angle  : {flrResultRegion.angle}")
        print(f"  2. Interest Pivot : ({flpPivot.x}, {flpPivot.y})")
        print(f"  3. Score : {f32Score:.3f}\n  4. Angle : {f32Angle:.3f}\n  5. Scale : {f32Scale:.3f}\n")

        if (res := layerFind.DrawFigureImage(flrResultRegion, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break
        if (res := layerFind.DrawFigureImage(flrResultRegion, arrColor[i64Idx])).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        flfaPoint = flpPivot.MakeCrossHair(3, False)
        flfaPoint.Rotate(f32Angle, flpPivot)
        if (res := layerFind.DrawFigureImage(flfaPoint, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break
        if (res := layerFind.DrawFigureImage(flfaPoint, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        tpPosition = TPoint[Double]()
        tpPosition.x = flpPivot.x
        tpPosition.y = flpPivot.y

        if (res := layerFind.DrawTextImage(tpPosition, wstrClassName, EColor.YELLOW, EColor.BLACK, 30, False, 0, EGUIViewImageTextAlignment.CENTER)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        tpPosition.x += 10
        strText = f"Score : {f32Score:.3f}\nAngle : {f32Angle:.3f}\nScale : x{f32Scale:.3f}\n"
        if (res := layerFind.DrawTextImage(tpPosition, strText, EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

    viewImageFind.Invalidate(True)

    # 이미지 뷰 종료 대기 // Wait for the imageview to close
    while viewImageLearn[0].IsAvailable():
        CThreadUtilities.Sleep(1)

    break
