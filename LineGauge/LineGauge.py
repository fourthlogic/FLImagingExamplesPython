# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

import math

# 메인 함수 // Main function
def main():
    arrViewText = [
        "Dark To Bright Or Bright To Dark\nBegin 0",
        "Dark To Bright Or Bright To Dark\nBegin 1",
        "Dark To Bright Or Bright To Dark\nBegin 2",
        "Dark To Bright Or Bright To Dark\nLargest Area",
        "Dark To Bright Or Bright To Dark\nEnd 0",
        "Dark To Bright Or Bright To Dark\nEnd 1",
        "Dark To Bright Or Bright To Dark\nEnd 2",
        "Dark To Bright Or Bright To Dark\nLargest Amplitude",
        "Dark To Bright Or Bright To Dark\nClosest",
        "Dark To Bright\nClosest",
        "Bright To Dark\nClosest",
        "Dark To Bright To Dark\nClosest",
    ]

    arrTransitionType = [
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CLineGauge.ETransitionType.DarkToBright,
        CLineGauge.ETransitionType.BrightToDark,
        CLineGauge.ETransitionType.DarkToBrightToDark,
    ]

    arrTransitionChoice = [
        CLineGauge.ETransitionChoice.Begin,
        CLineGauge.ETransitionChoice.Begin,
        CLineGauge.ETransitionChoice.Begin,
        CLineGauge.ETransitionChoice.LargestArea,
        CLineGauge.ETransitionChoice.End,
        CLineGauge.ETransitionChoice.End,
        CLineGauge.ETransitionChoice.End,
        CLineGauge.ETransitionChoice.LargestAmplitude,
        CLineGauge.ETransitionChoice.Closest,
        CLineGauge.ETransitionChoice.Closest,
        CLineGauge.ETransitionChoice.Closest,
        CLineGauge.ETransitionChoice.Closest,
    ]

    i32ExampleCount = len(arrViewText)

    arrTolerance = [
        200.0,
        200.0,
        200.0,
        200.0,
        200.0,
        200.0,
        200.0,
        200.0,
        100.0,
        100.0,
        100.0,
        100.0,
    ]
    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for v in range(i32ExampleCount)]
    res = CResult()

    # 이미지 로드 // Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/stripe.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 // Create image view
    for i in range(i32ExampleCount):
        i32X = 300 * (i % 4)
        i32Y = 300 * int(i / 4)

        if (res := arrViewImage[i].Create(i32X, i32Y, i32X + 300, i32Y + 300)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
        if (res := arrViewImage[i].SetImagePtr(fliImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            break

        # 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the all image views.
        if i > 0:
            if (
                res := arrViewImage[i].SynchronizePointOfView(arrViewImage[0])[0]
            ).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                break

    # Line Gauge 객체 생성 // Create Line Gauge Object
    lineGauge = CLineGauge()

    # 처리할 이미지 설정 // Set the image to process
    lineGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. // Set the area to measure.
    measureRegion = CFLLine[Double](250.0, 480.0, 250.0, 80.0)

    # 추출하기위한 파라미터를 설정합니다. // Set parameters for extraction.
    # 선을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. // Set the threshold change of the boundary point to be extracted to estimate the line.
    lineGauge.SetThreshold(20)
    # 선을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. // Set the correction value to the threshold change of the boundary point to be extracted to estimate the line.
    lineGauge.SetMinimumAmplitude(10)
    # 선을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. // Set the number of representative sample values ??of the boundary points to be extracted to estimate the line.
    lineGauge.SetThickness(1)
    # 선을 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. // Set the extraction interval of boundary points to be extracted to estimate the line.
    lineGauge.SetSamplingStep(1)
    # 선을 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. // Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the line.
    lineGauge.SetOutliersThreshold(1)
    # 선을 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. // Set the number of outlier adjustments for boundary points to be extracted to estimate the line.
    lineGauge.SetOutliersThresholdCount(3)

    for i in range(i32ExampleCount):        
        # 측정할 영역을 설정합니다. // Set the area to measure.
        lineGauge.SetMeasurementRegion(measureRegion, arrTolerance[i])

        # 선을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. // Set the boundary point change direction to extract to estimate the line.
        lineGauge.SetTransitionType(arrTransitionType[i])
        # 선을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. // Select the boundary point type to use among the boundary points extracted to estimate the line.
        lineGauge.SetTransitionChoice(arrTransitionChoice[i])

        # 알고리즘 수행 // Execute the Algoritm
        if (res := lineGauge.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Line gauge.")
            break

        # 실행 결과를 가져옵니다. // Get the execution result.
        fllResult = CFLLine[Double]()
        flfaResultsValid = CFLFigureArray()
        flfaResultsInvalid = CFLFigureArray()

        # 실행 결과를 가져옵니다. // Get the execution result. // Get the execution result.
        res = lineGauge.GetMeasuredObject(fllResult, i % 4)[0]
        # 추정된 선을 추출에 사용된 유효 경계점을 가져옵니다. // Get the effective boundary point used to extract the estimated line.
        lineGauge.GetMeasuredValidPoints(flfaResultsValid, i % 4)
        # 추정된 선을 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. // Get an invalid boundary point that is not used to extract the estimated line.
        lineGauge.GetMeasuredInvalidPoints(flfaResultsInvalid, i % 4)

        layer = arrViewImage[i].GetLayer(0)

        layer.Clear()

        if (
            res := layer.DrawTextImage(
                CFLPoint[Double](0, 0),
                arrViewText[i],
                EColor.YELLOW,
                EColor.BLUE,
                20,
                True,
            )
        ).IsFail():
            ErrorPrint(res, "Failed to draw figure\n")
            break
        
        # 선의 방향을 디스플레이 합니다. // Display the direction of the line.
        flpCenter = CFLPoint[Double]()
        f64Angle = 0
        fllCenter = CFLLine[Double]()

        flpCenter = measureRegion.GetCenter()
        f64Angle = measureRegion.GetAngle()

        fllCenter.flpPoints[0].Set(flpCenter)
        fllCenter.flpPoints[1].Set(flpCenter)
        fllCenter.Rotate(f64Angle, flpCenter)

        flpCenter1 = CFLPoint[Double](flpCenter.x - 1.5, flpCenter.y - math.sqrt(1.5) * .5 * 1.5)
        flpCenter2 = CFLPoint[Double](flpCenter.x + 1.5, flpCenter.y - math.sqrt(1.5) * .5 * 1.5)
        flpCenter3 = CFLPoint[Double](flpCenter.x, flpCenter.y + math.sqrt(1.5) * .5 * 1.5)

        flTriangle = CFLRegion()
        flTriangle.PushBack(flpCenter1)
        flTriangle.PushBack(flpCenter2)
        flTriangle.PushBack(flpCenter3)
        flTriangle.Rotate(f64Angle, flpCenter)

        if (res := layer.DrawFigureImage(fllCenter, EColor.BLUE)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if (res := layer.DrawFigureImage(flTriangle, EColor.LIGHTRED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        # 설정된 ROI에 대해 측정영역을 디스플레이 합니다. // Display the measurement area for the set ROI.
        flqDraw = CFLQuad[Double]()
        res, f64ToleranceLeft, f64ToleranceRight= lineGauge.GetTolerance(0, 0)
        
        fllNorm = measureRegion.GetNormalVector()
        flqDraw.flpPoints[0].x = measureRegion.flpPoints[0].x + fllNorm.x * f64ToleranceLeft
        flqDraw.flpPoints[0].y = measureRegion.flpPoints[0].y + fllNorm.y * f64ToleranceLeft
        flqDraw.flpPoints[1].x = measureRegion.flpPoints[1].x + fllNorm.x * f64ToleranceLeft
        flqDraw.flpPoints[1].y = measureRegion.flpPoints[1].y + fllNorm.y * f64ToleranceLeft
        flqDraw.flpPoints[2].x = measureRegion.flpPoints[1].x - fllNorm.x * f64ToleranceRight
        flqDraw.flpPoints[2].y = measureRegion.flpPoints[1].y - fllNorm.y * f64ToleranceRight
        flqDraw.flpPoints[3].x = measureRegion.flpPoints[0].x - fllNorm.x * f64ToleranceRight
        flqDraw.flpPoints[3].y = measureRegion.flpPoints[0].y - fllNorm.y * f64ToleranceRight

        if (res := layer.DrawFigureImage(flqDraw, EColor.BLUE)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break
        
        if (res := layer.DrawFigureImage(measureRegion, EColor.YELLOW)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if res.IsOK():
            # 추정된 선을 디스플레이 합니다. // Display the estimated line.
            if (res := layer.DrawFigureImage(fllResult, EColor.BLACK, 5)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            if (res := layer.DrawFigureImage(fllResult, EColor.CYAN, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            # 선의 정보를 Console창에 출력합니다. // Output the original information to the console window.
            
            f64Angle = fllResult.GetAngle()
            flpLineCenter = CFLPoint[Double]()
            fllResult.GetCenter(flpLineCenter)
            print("Line Center : ({}, {})\nAngle : {}˚".format(flpLineCenter.x, flpLineCenter.y, f64Angle))

        # 추출된 유효점이 어디인지 알기 위해 디스플레이 한다 // Display to know where the extracted valid point is
        for i64Index in range(flfaResultsValid.GetCount()):
            if flfaResultsValid.GetAt(i64Index).GetDeclType() != EFigureDeclType.Point:
                break

            if isinstance(flfaResultsValid.GetAt(i64Index), CFLPoint[Double]):
                flp = flfaResultsValid.GetAt(i64Index)
            else:
                flp = None

            flfaPoint = flp.MakeCrossHair(1, True)

            if (res := layer.DrawFigureImage(flfaPoint, EColor.LIME)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

        # 추출된 유효하지 않은 점이 어디인지 알기 위해 디스플레이 한다 // Display to see where the extracted invalid points are
        for i64Index in range(flfaResultsInvalid.GetCount()):
            if (
                flfaResultsInvalid.GetAt(i64Index).GetDeclType()
                != EFigureDeclType.Point
            ):
                break

            if isinstance(flfaResultsInvalid.GetAt(i64Index), CFLPoint[Double]):
                flp = flfaResultsInvalid.GetAt(i64Index)
            else:
                flp = None

            flfaPoint = flp.MakeCrossHair(1, True)

            if (res := layer.DrawFigureImage(flfaPoint, EColor.RED)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

        # 이미지 뷰를 갱신 합니다. // Update the image view.
        arrViewImage[i].Invalidate()

    bAvailable = True

    while bAvailable:
        for i in range(i32ExampleCount):
            bAvailable &= arrViewImage[i].IsAvailable()

        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()