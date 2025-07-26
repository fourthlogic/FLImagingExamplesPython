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
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CPointGauge.ETransitionType.DarkToBright,
        CPointGauge.ETransitionType.BrightToDark,
        CPointGauge.ETransitionType.DarkToBrightToDark,
    ]

    arrTransitionChoice = [
        CPointGauge.ETransitionChoice.Begin,
        CPointGauge.ETransitionChoice.Begin,
        CPointGauge.ETransitionChoice.Begin,
        CPointGauge.ETransitionChoice.LargestArea,
        CPointGauge.ETransitionChoice.End,
        CPointGauge.ETransitionChoice.End,
        CPointGauge.ETransitionChoice.End,
        CPointGauge.ETransitionChoice.LargestAmplitude,
        CPointGauge.ETransitionChoice.Closest,
        CPointGauge.ETransitionChoice.Closest,
        CPointGauge.ETransitionChoice.Closest,
        CPointGauge.ETransitionChoice.Closest,
    ]

    i32ExampleCount = len(arrViewText)

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

    # Point Gauge 객체 생성 // Create Point Gauge Object
    pointGauge = CPointGauge()

    # 처리할 이미지 설정 // Set the image to process
    pointGauge.SetSourceImage(fliImage)

    # 추출하기위한 파라미터를 설정합니다. // Set parameters for extraction.
    # 점을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. // Set the threshold change of the boundary point to be extracted to estimate the point.
    pointGauge.SetThreshold(20)
    # 점을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. // Set the correction value to the threshold change of the boundary point to be extracted to estimate the point.
    pointGauge.SetMinimumAmplitude(10)
    # 점을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. // Set the number of representative sample values ??of the boundary points to be extracted to estimate the point.
    pointGauge.SetThickness(1)
    
    # 측정할 영역을 설정합니다. // Set the area to measure.
    measureCenter = CFLPoint[Double](267.0, 240.0);
    tolerance = 400.0;
    angle = 25.0;
    pointGauge.SetMeasurementRegion(measureCenter, tolerance, angle)

    for i in range(i32ExampleCount):        

        # 점을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. // Set the boundary point change direction to extract to estimate the point.
        pointGauge.SetTransitionType(arrTransitionType[i])
        # 점을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. // Select the boundary point type to use among the boundary points extracted to estimate the point.
        pointGauge.SetTransitionChoice(arrTransitionChoice[i])

        # 알고리즘 수행 // Execute the Algoritm
        if (res := pointGauge.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Point gauge.")
            break

        # 실행 결과를 가져옵니다. // Get the execution result.
        fllResult = CFLPoint[Double]()

        # 실행 결과를 가져옵니다. // Get the execution result. // Get the execution result.
        res = pointGauge.GetMeasuredObject(fllResult, i % 4)[0]

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
        
        if res.IsOK():
            i64Count = pointGauge.GetMeasuredObjectCount();
            fllLine = pointGauge.GetMeasurementRegion();
            
            # 측정 중심 위치를 디스플레이한다. // Display the measurement center position.
            if (res := layer.DrawFigureImage(measureCenter.MakeCrossHair(10), EColor.RED)).IsFail():
                ErrorPrint(res, "Failed to draw figure\n");
                break;
            
            # 추출된 점이 어디인지 알기 위해 디스플레이 한다 // Display to know where the extracted point is
            for i32Index in range(i64Count):
                flp = CFLPoint[Double]();

                if(res := pointGauge.GetMeasuredObject(flp, i32Index)[0]).IsFail():
                    break;

                if (res := layer.DrawFigureImage(flp.MakeCrossHair(10, True), EColor.BLACK, 3)).IsFail():
                    ErrorPrint(res, "Failed to draw figure");
                    break;

                col = EColor.YELLOW if ((arrTransitionChoice[i] == CPointGauge.ETransitionChoice.Begin or arrTransitionChoice[i] == CPointGauge.ETransitionChoice.End) and i32Index != i % 4) else EColor.CYAN;

                if (res := layer.DrawFigureImage(flp.MakeCrossHair(10, True), col, 3)).IsFail():
                    ErrorPrint(res, "Failed to draw figure");
                    break;

                print("Index {} : ({}, {})".format(i32Index, flp.x, flp.y))

            if (res := layer.DrawFigureImage(fllLine, EColor.BLUE)).IsFail():
                break;


        # 이미지 뷰를 갱신 합니다. // Update the image view.
        arrViewImage[i].Invalidate()

    bAvailable = True

    while bAvailable:
        for i in range(i32ExampleCount):
            bAvailable &= arrViewImage[i].IsAvailable()

        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()