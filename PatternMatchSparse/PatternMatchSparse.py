from FLImagingClrPy import *

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

    while True:
        # 이미지 로드 // Load image
        if (res := fliLearnImage.Load("../../ExampleImages/Matching/Pattern2 Single Learn.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        if (res := fliFindImage.Load("../../ExampleImages/Matching/Pattern2 Single Find.flif")).IsFail():
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

        # 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
        if (res := viewImageLearn.SynchronizeWindow(viewImageFind)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        layerLearn = viewImageLearn.GetLayer(0)
        layerFind = viewImageFind.GetLayer(1)

        layerLearn.Clear()
        layerFind.Clear()

        flp00 = CFLPoint[Double](0, 0)

        if (res := layerLearn.DrawTextCanvas(flp00, "LEARN", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        if (res := layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        # Pattern Match Sparse 객체 생성 // Create Pattern Match Sparse object
        FLPatternMatchSparse = CPatternMatchSparse()

        # 학습할 이미지 설정 // Set the image to learn
        FLPatternMatchSparse.SetLearnImage(fliLearnImage)

        # 학습할 영역을 설정합니다. // Set the area to learn
        learnRegion = CFLRect[Double](150, 150, 760, 840)
        flpLearnPivot = CFLPoint[Double](learnRegion.GetCenter())
        FLPatternMatchSparse.SetLearnROI(learnRegion)
        FLPatternMatchSparse.SetLearnPivot(flpLearnPivot)

        # 샘플링 개수를 설정합니다. // Set the sample count
        FLPatternMatchSparse.SetSampleCount(64)

        # 알고리즘 수행 // Execute the Algoritm
        if (res := FLPatternMatchSparse.Learn()).IsFail():
            ErrorPrint(res, "Failed to Learn.")
            break

        # 측정 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the measurement area is
        if (res := layerLearn.DrawFigureImage(learnRegion, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if (res := layerLearn.DrawFigureImage(learnRegion, EColor.CYAN)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        # 설정된 중심점의 위치를 디스플레이 한다 // Display the position of the set center point
        flfaPointPivot = flpLearnPivot.MakeCrossHair(3, False)

        if (res := layerLearn.DrawFigureImage(flfaPointPivot, EColor.BLACK, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if (res := layerLearn.DrawFigureImage(flfaPointPivot, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        # 학습한 정보에 대해 출력한다 // Print the learned information
        print(" ▷ Learn Information")
        print("  1. ROI Shape Type : Rectangle")
        print(f"    left   : {learnRegion.left}")
        print(f"    right  : {learnRegion.right}")
        print(f"    top    : {learnRegion.top}")
        print(f"    bottom : {learnRegion.bottom}")
        print(f"    angle  : {learnRegion.angle}")
        print(f"  2. Interest Pivot : ({flpLearnPivot.x}, {flpLearnPivot.y})\n")

        # 검출할 이미지 설정 // Set image to detect
        FLPatternMatchSparse.SetSourceImage(fliFindImage)

        # 검출 시 사용될 기본 각도를 설정합니다. // Set the default angle to be used for detection.
        FLPatternMatchSparse.SetAngleBias(0.0)
        # 검출 시 사용될 각도의 탐색범위를 설정합니다. // Set the search range of the angle to be used for detection.
        # 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 // The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
        FLPatternMatchSparse.SetAngleTolerance(10.0)
        # 검출 시 사용될 최소 탐색점수를 설정합니다. // Set the minimum search score to be used for detection.
        FLPatternMatchSparse.SetMinimumDetectionScore(0.7)
        # 검출 시 사용될 최대 탐색객체 수를 설정합니다. // Set the maximum number of search objects to be used for detection.
        FLPatternMatchSparse.SetMaxObject(1)
        # 검출 시 보간법 사용 유무에 대해 설정합니다. // Set whether to use interpolation when detecting.
        FLPatternMatchSparse.EnableInterpolation(True)

        # 알고리즘 수행 // Execute the Algoritm
        if (res := FLPatternMatchSparse.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute")
            break

        # 기하학적 패턴 검출 결과를 가져옵니다. // Get geometric pattern detection results
        resultCount = FLPatternMatchSparse.GetResultCount()

        print(" ▶ Find Information")

        for i in range(resultCount):
            results = CPatternMatchSparse.SResult()
            FLPatternMatchSparse.GetResult(i, results)

            f32Score = results.f32Score
            f32Angle = results.f32Angle
            f32Scale = results.f32Scale
            flpPivot = CFLPoint[Double](results.pFlpPivot)
            pFlfRegion = CFLRect[Double](results.pFlfRegion)
            flrResultRegion = CFLRect[Double](pFlfRegion)

            flpResultRegion = CFLPoint[Double](flrResultRegion.left, flrResultRegion.top)

            # 패턴 검출 결과를 출력합니다. // Output the pattern detection result
            print(f" < Instance : {i} >")
            print("  1. ROI Shape Type : Rectangle")
            print(f"    left   : {flrResultRegion.left:.3f}")
            print(f"    right  : {flrResultRegion.right:.3f}")
            print(f"    top    : {flrResultRegion.top:.3f}")
            print(f"    bottom : {flrResultRegion.bottom:.3f}")
            print(f"    angle  : {flrResultRegion.angle:.3f}")
            print(f"  2. Interest Pivot : ({flpResultRegion.x:.3f}, {flpResultRegion.y:.3f})")
            print(f"  3. Score : {f32Score:.3f}\n  4. Angle : {f32Angle:.3f}\n  5. Scale : {f32Scale:.3f}\n")

            # 검출 결과의 중심점을 디스플레이 한다 // Display the center point of the detection result
            flfaPoint = flpPivot.MakeCrossHair(3, False)
            flfaPoint.Rotate(f32Angle, flpPivot)

            if (res := layerFind.DrawFigureImage(flfaPoint, EColor.BLACK, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            if (res := layerFind.DrawFigureImage(flfaPoint, EColor.LIME)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            # 결과 영역을 디스플레이 한다 // Display the result area
            if (res := layerFind.DrawFigureImage(flrResultRegion, EColor.BLACK, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            if (res := layerFind.DrawFigureImage(flrResultRegion, EColor.LIME)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            tpPosition = TPoint[Double]()
            tpPosition.x = flpPivot.x
            tpPosition.y = flpPivot.y

            strText = f"Score : {f32Score:.3f}\nAngle : {f32Angle:.3f}\nScale : x{f32Scale:.3f}\n"

            if (res := layerFind.DrawTextImage(tpPosition, strText, EColor.YELLOW, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_CENTER)).IsFail():
                ErrorPrint(res, "Failed to draw text")
                break

        # 이미지 뷰를 갱신 합니다. // Update the image view
        viewImageLearn.Invalidate(True)
        viewImageFind.Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the imageview to close
        while viewImageLearn.IsAvailable():
            CThreadUtilities.Sleep(1)
        break

if __name__ == "__main__":
    main()
