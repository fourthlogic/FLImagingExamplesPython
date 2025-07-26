# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 // Main function
def main():
    arrViewText = [
        "Dark To Bright To Dark\nClosest",
        "Bright To Dark To Bright\nClosest",
        "Dark To Bright To Dark Or Bright To Dark To Bright\nClosest",
    ]

    arrTransitionType = [
        CCrossGauge.ETransitionType.DarkToBrightToDark,
        CCrossGauge.ETransitionType.BrightToDarkToBright,
        CCrossGauge.ETransitionType.DarkToBrightToDarkOrBrightToDarkToBright,
    ]

    i32ExampleCount = len(arrViewText)

    # 이미지 객체 선언 // Declare the image object
    fliImage = [CFLImage() for v in range(i32ExampleCount)]

    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for v in range(i32ExampleCount)]
    res = CResult()
    
    # 이미지 로드 // Load image
    if (res := fliImage[0].Load("../../ExampleImages/Gauge/Cross_Bright.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    if (res := fliImage[1].Load("../../ExampleImages/Gauge/Cross_Dark.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    if (res := fliImage[2].Load("../../ExampleImages/Gauge/Cross_Dark_Bright.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 // Create image view
    for i in range(i32ExampleCount):
        i32X = 400 * (i % 4)
        i32Y = 400 * int(i / 4)
        
        if (res := arrViewImage[i].Create(i32X, i32Y, i32X + 400, i32Y + 400)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰에 이미지를 디스플레이 // display the image in the imageview
        if (res := arrViewImage[i].SetImagePtr(fliImage[i])[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            break

        # 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the all image views.
        if i > 0:
            if (
                res := arrViewImage[i].SynchronizePointOfView(arrViewImage[0])[0]
            ).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                break

    # Cross Gauge 객체 생성 // Create Cross Gauge Object
    crossGauge = CCrossGauge()

    # 측정할 영역을 설정합니다. // Set the area to measure.
    measureRegion = CFLRect[Double](126, 126, 400, 400)
    tolerance = 70.0
    crossGauge.SetMeasurementRegion(measureRegion, tolerance)

    # 추출하기위한 파라미터를 설정합니다. // Set parameters for extraction.
    # 십자형을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. // Select the boundary point type to use among the boundary points extracted to estimate the crosshair.
    crossGauge.SetTransitionChoice(CCrossGauge.ETransitionChoice.Closest)
    # 십자형을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. // Set the threshold change of the boundary point to be extracted to estimate the cross.
    crossGauge.SetThreshold(20)
    # 십자형을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. // Set the correction value to the threshold change of the boundary point to be extracted to estimate the cross.
    crossGauge.SetMinimumAmplitude(10)
    # 십자형을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. // Set the number of representative sample values ??of the boundary points to be extracted to estimate the cross.
    crossGauge.SetThickness(1)
    # 십자형을 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. // Set the extraction interval of boundary points to be extracted to estimate the cross.
    crossGauge.SetSamplingStep(1)
    # 십자형을 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. // Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the cross.
    crossGauge.SetOutliersThreshold(3)
    # 십자형을 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. // Set the number of outlier adjustments for boundary points to be extracted to estimate the cross.
    crossGauge.SetOutliersThresholdCount(3)
    # 코너를 추정하기위해 점 클러스터링 처리 유무에 대한 설정을 합니다. // Set whether or not to process point clustering to estimate the cross.
    crossGauge.EnableClusterMode(True)
    # 코너를 추정하기위해 마진을 설정합니다. 필요에 따라 각 구역별로 설정가능합니다. // Set the margin to estimate the cross. It can be set for each zone as needed.
    crossGauge.SetMeasurementMarginRatio(0.3, 0.1)

    for i in range(i32ExampleCount):
        # 처리할 이미지 설정 // Set the image to process
        crossGauge.SetSourceImage(fliImage[i])

        # 십자형을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. // Set the boundary point change direction to extract to estimate the cross.
        crossGauge.SetTransitionType(arrTransitionType[i])

        # 알고리즘 수행 // Execute the Algoritm
        if (res := crossGauge.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Cross gauge.")
            break

        layer = arrViewImage[i].GetLayer(0)
        layer.Clear()

        if (res := layer.DrawTextImage(CFLPoint[Double](0, 0), arrViewText[i], EColor.YELLOW, EColor.BLUE, 20, True)).IsFail():
            ErrorPrint(res, "Failed to draw figure\n")
            break
        
        # 실행 결과를 가져옵니다. // Get the execution result.
        resultRegion = CFLPoint[Double]()
        flfaResultsValid = CFLFigureArray()
        flfaResultsInvalid = CFLFigureArray()
        flfaResultLine = CFLFigureArray()
        # 추정을 위한 라인을 가져옵니다. // Get the line for inference.
        crossGauge.GetMeasuredLines(flfaResultLine)
        # 추정된 십자형을 가져옵니다. // Get the estimated crosshairs.
        crossGauge.GetMeasuredObject(resultRegion)
        # 추정된 십자형을 추출에 사용된 유효 경계점을 가져옵니다. // Get the valid boundary points used to extract the estimated crosshairs.
        crossGauge.GetMeasuredValidPoints(flfaResultsValid)
        # 추정된 십자형을 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. // Get invalid boundary points that were not used to extract the estimated crosshairs.
        crossGauge.GetMeasuredInvalidPoints(flfaResultsInvalid)
        
        flfaResult = resultRegion.MakeCrossHair(25, True)
        layer.DrawFigureImage(flfaResult, EColor.BLACK, 3)
        layer.DrawFigureImage(flfaResult, EColor.CYAN, 1)

        layer.DrawFigureImage(flfaResultLine, EColor.BLACK, 5)
        layer.DrawFigureImage(flfaResultLine, EColor.CYAN, 3)
        
        if(res.IsOK()):
            res, f64ResultAngle = crossGauge.GetMeasuredAngle(0)

            print("Cross Center : ({}, {})\nAngle : {}˚".format(resultRegion.x, resultRegion.y, f64ResultAngle))

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

        # 측정 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the measurement area is
        if (res := layer.DrawFigureImage(measureRegion, EColor.BLUE)).IsFail():
            ErrorPrint(res, "Failed to draw figures objects on the image view.")
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