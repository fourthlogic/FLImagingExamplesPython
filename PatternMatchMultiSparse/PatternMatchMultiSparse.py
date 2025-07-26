from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import sys

# 경고 코드 // Error print function
def ErrorPrint(res: CResult, msg: str):
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
    input()


def main():
    # 이미지 객체 선언 // Declare the image object
    fliLearnImage = [CFLImage() for _ in range(2)]
    fliFindImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageLearn = [CGUIViewImage() for _ in range(2)]
    viewImageFind = CGUIViewImage()

    res = CResult()

    # Pattern Match Multi 객체 생성 // Create Pattern Match Multi object
    FLPatternMatchMultiSparse = CPatternMatchMultiSparse()

    while True:  # do~while(false) 구조
        arrPath = ["../../ExampleImages/Matching/Pattern2 Single Learn.flif",
                   "../../ExampleImages/Matching/Pattern2 Single Learn.flif"]

        arrClassName = ["A", "B"]
        arrColor = [EColor.LIME, EColor.RED]
        arrLearnRegion = [
            CFLRect[Double](326.6913, 372.2960, 477.5354, 521.5354),
            CFLRect[Double](586.7185, 566.3427, 763.2982, 672.1134),
        ]

        for i64DataIdx in range(2):
            # 이미지 로드 // Load image
            if (res := fliLearnImage[i64DataIdx].Load(arrPath[i64DataIdx])).IsFail():
                ErrorPrint(res, "Failed to load the image file.")
                break

            # 이미지 뷰 생성 // Create image view
            left = int(400 + 512 * i64DataIdx)
            top = 0
            right = int(400 + 512 * (i64DataIdx + 1))
            bottom = 384
            if (res := viewImageLearn[i64DataIdx].Create(left, top, right, bottom)).IsFail():
                ErrorPrint(res, "Failed to create the image view.")
                break

            # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
            if (res := viewImageLearn[i64DataIdx].SetImagePtr(fliLearnImage[i64DataIdx])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.")
                break

            layerLearn = viewImageLearn[i64DataIdx].GetLayer(0)
            layerLearn.Clear()

            # 학습할 이미지 설정 // Set the image to learn
            FLPatternMatchMultiSparse.SetLearnImage(fliLearnImage[i64DataIdx])

            # 학습할 영역을 설정합니다. // Set the area to learn.
            flpLearnPivot = CFLPoint[Double](arrLearnRegion[i64DataIdx].GetCenter())
            FLPatternMatchMultiSparse.SetLearnROI(arrLearnRegion[i64DataIdx])
            FLPatternMatchMultiSparse.SetLearnPivot(flpLearnPivot)
            FLPatternMatchMultiSparse.SetSampleCount(256)

            # 알고리즘 학습 수행 // Learn the Algoritm
            if (res := FLPatternMatchMultiSparse.Learn(arrClassName[i64DataIdx])).IsFail():
                ErrorPrint(res, "Failed to Learn.")
                break

            # 측정 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the measurement area is
            if (res := layerLearn.DrawFigureImage(arrLearnRegion[i64DataIdx], EColor.BLACK, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            if (res := layerLearn.DrawFigureImage(arrLearnRegion[i64DataIdx], arrColor[i64DataIdx])).IsFail():
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

            strStatus = f"LEARN CLASS {arrClassName[i64DataIdx]}"
            flpPosition00 = CFLPoint[Double](0, 0)

            if (res := layerLearn.DrawTextCanvas(flpPosition00, strStatus, EColor.YELLOW, EColor.BLACK, 30)).IsFail():
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
            print(f"  2. Interest Pivot : ({flpLearnPivot.x}, {flpLearnPivot.y})")
            print("")

            # 이미지 뷰를 갱신 합니다. // Update the image view.
            viewImageLearn[i64DataIdx].Invalidate(True)
        else:
            # 위 for문이 break 없이 끝난 경우에만 아래 실행됨
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
                # 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
                if (res := viewImageFind.SynchronizeWindow(viewImageLearn[i64DataIdx])[0]).IsFail():
                    ErrorPrint(res, "Failed to synchronize window.")
                    break
            else:
                layerFind = viewImageFind.GetLayer(1)
                layerFind.Clear()

                flp00 = CFLPoint[Double](0, 0)

                if (res := layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
                    ErrorPrint(res, "Failed to draw text")
                    break

                # 검출할 이미지 설정 // Set image to detect
                FLPatternMatchMultiSparse.SetSourceImage(fliFindImage)
                # 검출 시 사용될 파라미터를 설정합니다. // Set the parameters to be used for detection.
                # 검출 시 사용될 기본 각도를 설정합니다. // Set the default angle to be used for detection.
                FLPatternMatchMultiSparse.SetAngleBias(0.0)
                # 검출 시 사용될 각도의 탐색범위를 설정합니다. // Set the search range of the angle to be used for detection.
                # 각도는 기본 각도를 기준으로 (기본 각도 - AngleTolerance, 기본 각도 + AngleTolerance)가 최종 탐색범위 // The angle is based on the basic angle (default angle - AngleTolerance, basic angle + AngleTolerance) is the final search range
                FLPatternMatchMultiSparse.SetAngleTolerance(15.0)
                # 검출 시 최적화 정도를 설정합니다. // Set the degree of optimization for detection.
                # 검출 시 사용될 최소 탐색점수를 설정합니다. // Set the minimum search score to be used for detection.
                FLPatternMatchMultiSparse.SetMinimumDetectionScore(0.7)
                # 검출 시 사용될 탐색 방식을 설정합니다. // Set the search method to be used for detection.
                FLPatternMatchMultiSparse.SetMaxObjectMode(CPatternMatchMultiSparse.EMaxObjectMode.Total)
                # 검출 시 사용될 최대 탐색객체 수를 설정합니다. // Set the maximum number of search objects to be used for detection.
                FLPatternMatchMultiSparse.SetMaxObjectTotal(2)
                # 검출 시 보간법 사용 유무에 대해 설정합니다. // Set whether to use interpolation when detecting.
                FLPatternMatchMultiSparse.EnableInterpolation(True)
                # 검출 시 서로 다른 클래스에 대해 영역 중복을 허용 유무에 대해 설정합니다. // Set whether to allow area overlap for different classes during detection.
                FLPatternMatchMultiSparse.SetConflictDetectionMethod(CPatternMatchMultiSparse.EConflictDetectionMethod.HighestScore)

                # 알고리즘 수행 // Execute the Algoritm
                if (res := FLPatternMatchMultiSparse.Execute()).IsFail():
                    ErrorPrint(res, "Failed to execute")
                    break

                # 패턴 검출 결과를 가져옵니다. // Get the pattern detection result.
                i64ResultCount = FLPatternMatchMultiSparse.GetResultCount()

                print(" ▶ Find Information")

                for i in range(i64ResultCount):
                    results = CPatternMatchMultiSparse.SResult()
                    FLPatternMatchMultiSparse.GetResult(i, results)

                    f32Score = results.f32Score
                    f32Angle = results.f32Angle
                    f32Scale = results.f32Scale
                    flpPivot = CFLPoint[Double](results.pFlpPivot)
                    pFlfRegion = CFLRect[Double](results.pFlfRegion)
                    pFlrResultRegion = CFLRect[Double](pFlfRegion)

                    flrResultRegion = pFlrResultRegion
                    wstrClassName = results.pStrClassName

                    i64Idx = 0
                    for i64ResultIndex in range(3):
                        if wstrClassName == arrClassName[i64ResultIndex]:
                            i64Idx = i64ResultIndex
                            break
                        
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

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the imageview to close
        while viewImageLearn[0].IsAvailable():
            CThreadUtilities.Sleep(1)

        break

# 메인 호출 // Main call
if __name__ == "__main__":
    main()