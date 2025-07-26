from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


def ErrorPrint(res, msg):
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
FLPatternMatchMulti = CPatternMatchMulti()

while True:
    arrPath = ["../../ExampleImages/Matching/Pattern Multi Learn.flif",
               "../../ExampleImages/Matching/Pattern Multi Learn.flif"]

    arrClassName = ["A", "B"]
    arrColor = [EColor.LIME, EColor.RED]
    arrLearnRegion = [
        CFLRect[Double](178.9984, 178.9984, 253.9842, 257.2094),
        CFLRect[Double](110.4629, 109.6566, 182.2236, 178.9984)
    ]

    for i64DataIdx in range(2):
        # 이미지 로드 // Load image
        if (res := fliLearnImage[i64DataIdx].Load(arrPath[i64DataIdx])).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImageLearn[i64DataIdx].Create(400 + 512 * i64DataIdx, 0, 400 + 512 * (i64DataIdx + 1), 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지를 디스플레이 // Display the image in the image view
        if (res := viewImageLearn[i64DataIdx].SetImagePtr(fliLearnImage[i64DataIdx])[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        layerLearn = viewImageLearn[i64DataIdx].GetLayer(0)
        layerLearn.Clear()

        # 학습할 이미지 설정 // Set the image to learn
        FLPatternMatchMulti.SetLearnImage(fliLearnImage[i64DataIdx])

        # 학습할 영역을 설정합니다. // Set the area to learn.
        flpLearnPivot = CFLPoint[Double](arrLearnRegion[i64DataIdx].GetCenter())
        FLPatternMatchMulti.SetLearnROI(arrLearnRegion[i64DataIdx])
        FLPatternMatchMulti.SetLearnPivot(flpLearnPivot)

        # 알고리즘 학습 수행 // Learn the Algoritm
        res = FLPatternMatchMulti.Learn(arrClassName[i64DataIdx])
        if res.IsFail():
            ErrorPrint(res, "Failed to Learn.")
            break

        # 측정 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the measurement area is
        res = layerLearn.DrawFigureImage(arrLearnRegion[i64DataIdx], EColor.BLACK, 3)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        res = layerLearn.DrawFigureImage(arrLearnRegion[i64DataIdx], arrColor[i64DataIdx])
        if res.IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        # 설정된 중심점의 위치를 디스플레이 한다 // Display the position of the set center point
        flfaPointPivot = flpLearnPivot.MakeCrossHair(3, False)

        res = layerLearn.DrawFigureImage(flfaPointPivot, EColor.BLACK, 3)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        res = layerLearn.DrawFigureImage(flfaPointPivot, EColor.LIME)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        strStatus = f"LEARN CLASS {arrClassName[i64DataIdx]}"
        flpPosition00 = CFLPoint[Double](0, 0)

        res = layerLearn.DrawTextCanvas(flpPosition00, strStatus, EColor.YELLOW, EColor.BLACK, 30)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        # 학습한 정보에 대해 Console창에 출력한다 // Print the learned information to the console window
        print(f"  < LEARN CLASS {arrClassName[i64DataIdx]} > ")
        print("  1. ROI Shape Type : Rectangle")
        print(f"    left   : {arrLearnRegion[i64DataIdx].left}")
        print(f"    right  : {arrLearnRegion[i64DataIdx].right}")
        print(f"    top    : {arrLearnRegion[i64DataIdx].top}")
        print(f"    bottom : {arrLearnRegion[i64DataIdx].bottom}")
        print(f"    angle  : {arrLearnRegion[i64DataIdx].angle}")
        print(f"  2. Interest Pivot : ({flpLearnPivot.x}, {flpLearnPivot.y})\n")

        # 이미지 뷰를 갱신 합니다. // Update the image view.
        viewImageLearn[i64DataIdx].Invalidate(True)

    # 이미지 로드 // Load image
    res = fliFindImage.Load("../../ExampleImages/Matching/Pattern Multi Find.flif")
    if res.IsFail():
        break

    # 이미지 뷰 생성 // Create image view
    if (res := viewImageFind.Create(400, 384, 1168, 960)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        break

    # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
    if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        break

    for i in range(2):
        if (res := viewImageFind.SynchronizeWindow(viewImageLearn[i])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

    layerFind = viewImageFind.GetLayer(1)
    layerFind.Clear()

    flp00 = CFLPoint[Double](0, 0)
    res = layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)
    if res.IsFail():
        ErrorPrint(res, "Failed to draw text")
        break

    # 검출 설정들
    # 찾을 이미지 설정 // Set the image to find
    FLPatternMatchMulti.SetSourceImage(fliFindImage)
    # 스케일 범위 설정 // Set the scale range
    FLPatternMatchMulti.SetScaleRange(1.0, 1.0)
    # 각도 바이어스 설정 // Set the angle bias
    FLPatternMatchMulti.SetAngleBias(0.0)
    # 각도 허용 오차 설정 // Set the angle tolerance
    FLPatternMatchMulti.SetAngleTolerance(15.0)
    # 정밀도 설정 // Set the accuracy
    FLPatternMatchMulti.SetAccuracy(0.5)
    # 최소 점수 설정 // Set the minimum detection score
    FLPatternMatchMulti.SetMinimumDetectionScore(0.7)
    # 최대 객체 모드 설정 // Set the maximum object mode
    FLPatternMatchMulti.SetMaxObjectMode(CPatternMatchMulti.EMaxObjectMode.Total)
    # 총 객체 최대 개수 설정 // Set the total maximum object count
    FLPatternMatchMulti.SetMaxObjectTotal(2)
    # 보간 사용 설정 // Enable interpolation
    FLPatternMatchMulti.EnableInterpolation(True)
    # 충돌 감지 방법 설정 // Set the conflict detection method
    FLPatternMatchMulti.SetConflictDetectionMethod(CPatternMatchMulti.EConflictDetectionMethod.HighestScore)

    res = FLPatternMatchMulti.Execute()
    if res.IsFail():
        ErrorPrint(res, "Failed to execute")
        break

    i64ResultCount = FLPatternMatchMulti.GetResultCount()
    print(" ▶ Find Information")

    for i in range(i64ResultCount):
        results = CPatternMatchMulti.SResult()
        FLPatternMatchMulti.GetResult(i, results)

        f32Score = results.f32Score
        f32Angle = results.f32Angle
        f32Scale = results.f32Scale
        flpPivot = CFLPoint[Double](results.pFlpPivot)
        flrResultRegion = CFLRect[Double](CFLRect[Double](results.pFlfRegion))
        wstrClassName = results.pStrClassName

        i64Idx = arrClassName.index(wstrClassName) if wstrClassName in arrClassName else 0

        print(f" < Instance : {i} >")
        print(f" Class Name); : {wstrClassName}")
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

    # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the imageview to close
    while viewImageLearn[0].IsAvailable():
        CThreadUtilities.Sleep(1)

    break
