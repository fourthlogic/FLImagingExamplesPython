from FLImagingClrPy import *

CLibraryUtilities.Initialize()

# 경고 코드 // Error print function
def ErrorPrint(res: CResult, msg: str):
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
    input()

# 메인 함수 시작 // Main function start
def main():
    # 이미지 객체 선언 // Declare the image object
    fliLearnImage = [CFLImage(), CFLImage()]
    fliFindImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageLearn = [CGUIViewImage(), CGUIViewImage()]
    viewImageFind = CGUIViewImage()

    res = CResult()

    # Pattern Match Multi 객체 생성 // Create Pattern Match Multi object
    FLPatternMatchMultiSave = CPatternMatchMulti()
    FLPatternMatchMultiLoad = CPatternMatchMulti()

    while True:
        arrPath = ["../../ExampleImages/Matching/Pattern Multi Learn.flif"] * 2
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

            # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
            if (res := viewImageLearn[i64DataIdx].SetImagePtr(fliLearnImage[i64DataIdx])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.")
                break

            layerLearn = viewImageLearn[i64DataIdx].GetLayer(0)
            layerLearn.Clear()

            # 학습할 이미지 설정 // Set the image to learn
            FLPatternMatchMultiSave.SetLearnImage(fliLearnImage[i64DataIdx])[0]

            # 학습할 영역 설정 // Set the area to learn
            flpLearnPivot = CFLPoint[Double](arrLearnRegion[i64DataIdx].GetCenter())
            FLPatternMatchMultiSave.SetLearnROI(arrLearnRegion[i64DataIdx])
            FLPatternMatchMultiSave.SetLearnPivot(flpLearnPivot)

            # 알고리즘 수행 // Execute the Algoritm
            if FLPatternMatchMultiSave.Learn(arrClassName[i64DataIdx]).IsFail():
                ErrorPrint(res, "Failed to Learn.")
                break

            # 측정 영역 디스플레이 // Display learning region
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
            print(f"    left   : {arrLearnRegion[i64DataIdx].left:.3f}")
            print(f"    right  : {arrLearnRegion[i64DataIdx].right:.3f}")
            print(f"    top    : {arrLearnRegion[i64DataIdx].top:.3f}")
            print(f"    bottom : {arrLearnRegion[i64DataIdx].bottom:.3f}")
            print(f"    angle  : {arrLearnRegion[i64DataIdx].angle:.3f}")
            print(f"  2. Interest Pivot : ({flpLearnPivot.x:.3f}, {flpLearnPivot.y:.3f})\n")

            # 이미지 뷰 갱신 // Update image view
            viewImageLearn[i64DataIdx].Invalidate(True)

        # 학습 정보 저장 // Save learning data
        if (res := FLPatternMatchMultiSave.Save("../../ExampleImages/Matching/Pattern Multi Learn")).IsFail():
            ErrorPrint(res, "Failed to save\n")
            break

        # 이미지 로드 // Load image
        if (res := fliFindImage.Load("../../ExampleImages/Matching/Pattern Multi Find.flif")).IsFail():
            ErrorPrint(res, "Failed to load\n")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImageFind.Create(400, 384, 1168, 960)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지 설정 // Set image on image view
        if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        for i64DataIdx in range(2):
            # 윈도우 동기화 // Synchronize window
            if (res := viewImageFind.SynchronizeWindow(viewImageLearn[i64DataIdx])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize window.")
                break

        layerFind = viewImageFind.GetLayer(1)
        layerFind.Clear()

        flp00 = CFLPoint[Double](0, 0)
        if (res := layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        if (res := FLPatternMatchMultiLoad.Load("../../ExampleImages/Matching/Pattern Multi Learn")).IsFail():
            ErrorPrint(res, "Failed to load\n")
            break

        # 검출 이미지 설정 및 파라미터 설정 // Set detection parameters
        # 찾을 이미지 설정 // Set the image to find
        FLPatternMatchMultiLoad.SetSourceImage(fliFindImage)
        # 스케일 범위 설정 // Set the scale range
        FLPatternMatchMultiLoad.SetScaleRange(1.0, 1.0)
        # 각도 바이어스 설정 // Set the angle bias
        FLPatternMatchMultiLoad.SetAngleBias(0.0)
        # 각도 허용 오차 설정 // Set the angle tolerance
        FLPatternMatchMultiLoad.SetAngleTolerance(15.0)
        # 정밀도 설정 // Set the accuracy
        FLPatternMatchMultiLoad.SetAccuracy(0.5)
        # 최소 점수 설정 // Set the minimum detection score
        FLPatternMatchMultiLoad.SetMinimumDetectionScore(0.7)
        # 최대 객체 모드 설정 // Set the maximum object mode
        FLPatternMatchMultiLoad.SetMaxObjectMode(CPatternMatchMulti.EMaxObjectMode.Total)
        # 총 객체 최대 개수 설정 // Set the total maximum object count
        FLPatternMatchMultiLoad.SetMaxObjectTotal(2)
        # 보간 사용 설정 // Enable interpolation
        FLPatternMatchMultiLoad.EnableInterpolation(True)
        # 충돌 감지 방법 설정 // Set the conflict detection method
        FLPatternMatchMultiLoad.SetConflictDetectionMethod(CPatternMatchMulti.EConflictDetectionMethod.HighestScore)

        # 알고리즘 수행 // Execute the Algoritm
        if (res := FLPatternMatchMultiLoad.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute")
            break

        i64ResultCount = FLPatternMatchMultiLoad.GetResultCount()

        for i in range(i64ResultCount):
            results = CPatternMatchMulti.SResult()
            FLPatternMatchMultiLoad.GetResult(i, results)

            f32Score = results.f32Score
            f32Angle = results.f32Angle
            f32Scale = results.f32Scale
            flpPivot = CFLPoint[Double](results.pFlpPivot)
            pFlfRegion = CFLRect[Double](results.pFlfRegion)
            flrResultRegion = pFlfRegion
            wstrClassName = results.pStrClassName

            i64Idx = 0
            for idx, name in enumerate(arrClassName):
                if wstrClassName == name:
                    i64Idx = idx
                    break

            # 검출 결과 출력 // Output result
            print(f" < Instance : {i} >")
            print(f" Class Name : {wstrClassName}")
            print("  1. ROI Shape Type : Rectangle")
            print(f"    left   : {flrResultRegion.left:.3f}")
            print(f"    right  : {flrResultRegion.right:.3f}")
            print(f"    top    : {flrResultRegion.top:.3f}")
            print(f"    bottom : {flrResultRegion.bottom:.3f}")
            print(f"    angle  : {flrResultRegion.angle:.3f}")
            print(f"  2. Interest Pivot : ({flpPivot.x:.3f}, {flpPivot.y:.3f})")
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

if __name__ == "__main__":
    main()
