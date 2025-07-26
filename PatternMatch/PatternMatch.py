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

def main():
    # 이미지 객체 선언 // Declare the image object
    fliLearnImage = CFLImage()
    fliFindImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageLearn = CGUIViewImage()
    viewImageFind = CGUIViewImage()

    res = CResult()

    # 이미지 로드 // Load image
    if (res := fliLearnImage.Load("../../ExampleImages/Matching/Pattern Single Learn.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.")
        return

    if (res := fliFindImage.Load("../../ExampleImages/Matching/Pattern Single Find.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.")
        return

    # 이미지 뷰 생성 // Create image view
    if (res := viewImageLearn.Create(400, 0, 912, 384)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    if (res := viewImageFind.Create(912, 0, 1680, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview 
    if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        return
    
    if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        return

    # 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
    if (res := viewImageLearn.SynchronizeWindow(viewImageFind)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        return

    layerLearn = viewImageLearn.GetLayer(0)
    layerFind = viewImageFind.GetLayer(1)

    layerLearn.Clear()
    layerFind.Clear()

    flp00 = CFLPoint[Double](0, 0)

    if (res := layerLearn.DrawTextCanvas(flp00, "LEARN", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text")
        return

    if (res := layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text")
        return

    # Pattern Match 객체 생성 // Create Pattern Match object
    FLPatternMatch = CPatternMatch()

    # 학습할 이미지 설정 // Set the image to learn
    FLPatternMatch.SetLearnImage(fliLearnImage)

    # 학습할 영역을 설정합니다. // Set the area to learn.
    learnRegion = CFLRect[Double](174.7086, 272.2204, 799.0551, 601.3228)
    flpLearnPivot = CFLPoint[Double](learnRegion.GetCenter())
    FLPatternMatch.SetLearnROI(learnRegion)
    FLPatternMatch.SetLearnPivot(flpLearnPivot)

    # 알고리즘 학습 // Learn the Algoritm
    if (res := FLPatternMatch.Learn()).IsFail():
        ErrorPrint(res, "Failed to Learn.")
        return

    # 측정 영역이 어떻게 되는지 알기 위해 디스플레이 한다 // Display to know where the measurement area is
    if (res := layerLearn.DrawFigureImage(learnRegion, EColor.BLACK, 3)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    if (res := layerLearn.DrawFigureImage(learnRegion, EColor.CYAN)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    # 설정된 중심점의 위치를 디스플레이 한다 // Display the position of the set center point
    flfaPointPivot = flpLearnPivot.MakeCrossHair(3, False)

    if (res := layerLearn.DrawFigureImage(flfaPointPivot, EColor.BLACK, 3)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    if (res := layerLearn.DrawFigureImage(flfaPointPivot, EColor.LIME)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    # 학습한 정보에 대해 Console창에 출력한다 // Print the learned information to the console window
    print(" ▷ Learn Information")
    print("  1. ROI Shape Type : Rectangle")
    print("    left   : {}".format(learnRegion.left))
    print("    right  : {}".format(learnRegion.right))
    print("    top    : {}".format(learnRegion.top))
    print("    bottom : {}".format(learnRegion.bottom))
    print("    angle  : {}".format(learnRegion.angle))
    print("  2. Interest Pivot : ({}, {})".format(flpLearnPivot.x, flpLearnPivot.y))
    print("")

    # 검출할 이미지 설정 // Set image to detect
    FLPatternMatch.SetSourceImage(fliFindImage)

    # 검출 시 사용될 파라미터를 설정합니다. // Set the parameters to be used for detection.
    FLPatternMatch.SetScaleRange(0.95, 1.05)
    FLPatternMatch.SetAngleBias(0.0)
    FLPatternMatch.SetAngleTolerance(10.0)
    FLPatternMatch.SetAccuracy(0.5)
    FLPatternMatch.SetMinimumDetectionScore(0.7)
    FLPatternMatch.SetMaxObject(1)
    FLPatternMatch.EnableInterpolation(True)

    # 알고리즘 수행 // Execute the Algoritm 
    if (res := FLPatternMatch.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute")
        return

    i64ResultCount = FLPatternMatch.GetResultCount()

    print(" ▶ Find Information")

    for i in range(i64ResultCount):
        results = CPatternMatch.SResult()
        FLPatternMatch.GetResult(i, results)

        f32Score = results.f32Score
        f32Angle = results.f32Angle
        f32Scale = results.f32Scale
        flpPivot = CFLPoint[Double](results.pFlpPivot)
        pFlfRegion = CFLRect[Double](results.pFlfRegion)
        flrResultRegion = pFlfRegion
        flpResultRegion = CFLPoint[Double](flrResultRegion.left, flrResultRegion.top)

        print(" < Instance : {} >".format(i))
        print("  1. ROI Shape Type : Rectangle")
        print("    left   : {}".format(flrResultRegion.left))
        print("    right  : {}".format(flrResultRegion.right))
        print("    top    : {}".format(flrResultRegion.top))
        print("    bottom : {}".format(flrResultRegion.bottom))
        print("    angle  : {}".format(flrResultRegion.angle))
        print("  2. Interest Pivot : ({}, {})".format(flpResultRegion.x, flpResultRegion.y))
        print("  3. Score : {:.3f}\n  4. Angle : {:.3f}\n  5. Scale : {:.3f}".format(f32Score, flrResultRegion.angle, f32Scale))
        print("")

        flfaPoint = flpPivot.MakeCrossHair(3, False)
        flfaPoint.Rotate(f32Angle, flpPivot)

        if (res := layerFind.DrawFigureImage(flfaPoint, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

        if (res := layerFind.DrawFigureImage(flfaPoint, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

        if (res := layerFind.DrawFigureImage(flrResultRegion, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

        if (res := layerFind.DrawFigureImage(flrResultRegion, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

        tpPosition = TPoint[Double]()
        tpPosition.x = flpPivot.x
        tpPosition.y = flpPivot.y

        strText = "Score : {:.3f}\nAngle : {:.3f}\nScale : x{:.3f}\n".format(f32Score, f32Angle, f32Scale)

        res = layerFind.DrawTextImage(tpPosition, strText, EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw text")
            return

    # 이미지 뷰를 갱신 합니다. // Update the image view.
    viewImageLearn.Invalidate(True)
    viewImageFind.Invalidate(True)

    # 이미지 뷰가 종료될 때 까지 기다린 // Wait for the imageview to close
    while viewImageLearn.IsAvailable():
        CThreadUtilities.Sleep(1)

if __name__ == '__main__':
    main()
