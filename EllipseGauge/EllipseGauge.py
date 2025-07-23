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
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CEllipseGauge.ETransitionType.DarkToBright,
        CEllipseGauge.ETransitionType.BrightToDark,
        CEllipseGauge.ETransitionType.DarkToBrightToDark,
    ]

    arrTransitionChoice = [
        CEllipseGauge.ETransitionChoice.Begin,
        CEllipseGauge.ETransitionChoice.Begin,
        CEllipseGauge.ETransitionChoice.Begin,
        CEllipseGauge.ETransitionChoice.LargestArea,
        CEllipseGauge.ETransitionChoice.End,
        CEllipseGauge.ETransitionChoice.End,
        CEllipseGauge.ETransitionChoice.End,
        CEllipseGauge.ETransitionChoice.LargestAmplitude,
        CEllipseGauge.ETransitionChoice.Closest,
        CEllipseGauge.ETransitionChoice.Closest,
        CEllipseGauge.ETransitionChoice.Closest,
        CEllipseGauge.ETransitionChoice.Closest,
    ]

    i32ExampleCount = len(arrViewText)

    arrTolerance = [
        85.0,
        85.0,
        85.0,
        20.0,
        85.0,
        85.0,
        85.0,
        30.0,
        30.0,
        30.0,
        30.0,
        30.0,
    ]
    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for v in range(i32ExampleCount)]
    res = CResult()

    # 이미지 로드 // Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/Ellipse.flif")).IsFail():
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

    # Ellipse Gauge 객체 생성 // Create Ellipse Gauge Object
    ellipseGauge = CEllipseGauge()

    # 처리할 이미지 설정 // Set the image to process
    ellipseGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. // Set the area to measure.
    measureRegion = CFLEllipse[Double](240, 280, 96, 150, 22)

    # 추출하기위한 파라미터를 설정합니다. // Set parameters for extraction.
    # 타원을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. // Set the threshold change of the boundary point to be extracted to estimate the ellipse.
    ellipseGauge.SetThreshold(20)
    # 타원을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. // Set the correction value to the threshold change of the boundary point to be extracted to estimate the ellipse.
    ellipseGauge.SetMinimumAmplitude(10)
    # 타원을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. // Set the number of representative sample values ??of the boundary points to be extracted to estimate the ellipse.
    ellipseGauge.SetThickness(3)
    # 타원을 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. // Set the extraction interval of boundary points to be extracted to estimate the ellipse.
    ellipseGauge.SetSamplingStep(1)
    # 타원을 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. // Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the ellipse.
    ellipseGauge.SetOutliersThreshold(3)
    # 타원을 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. // Set the number of outlier adjustments for boundary points to be extracted to estimate the ellipse.
    ellipseGauge.SetOutliersThresholdCount(3)

    for i in range(i32ExampleCount):
        # 타원을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. // Set the boundary point change direction to extract to estimate the ellipse.
        ellipseGauge.SetTransitionType(arrTransitionType[i])
        # 타원을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. // Select the boundary point type to use among the boundary points extracted to estimate the ellipse.
        ellipseGauge.SetTransitionChoice(arrTransitionChoice[i])

        ellipseGauge.SetMeasurementRegion(measureRegion, arrTolerance[i])

        # 알고리즘 수행 // Execute the Algoritm
        if (res := ellipseGauge.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Ellipse gauge.")
            break

        # 실행 결과를 가져옵니다. // Get the execution result.
        fleResult = CFLEllipse[Double]()
        flfaResultsValid = CFLFigureArray()
        flfaResultsInvalid = CFLFigureArray()

        # 실행 결과를 가져옵니다. // Get the execution result. // Get the execution result.
        res = ellipseGauge.GetMeasuredObject(fleResult, i % 4)[0]
        # 추정된 타원을 추출에 사용된 유효 경계점을 가져옵니다. // Get the effective boundary point used to extract the estimated ellipse.
        ellipseGauge.GetMeasuredValidPoints(flfaResultsValid, i % 4)
        # 추정된 타원을 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. // Get an invalid boundary point that is not used to extract the estimated ellipse.
        ellipseGauge.GetMeasuredInvalidPoints(flfaResultsInvalid, i % 4)

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

        # 측정 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the measurement area is
        fleRegion = ellipseGauge.GetMeasurementRegion()

        fleInner = CFLEllipse[Double](fleRegion)
        fleOuter = CFLEllipse[Double](fleRegion)
        
        res, f64Radius1 = fleInner.GetRadius1(0)
        res, f64Radius2 = fleInner.GetRadius2(0)
        f64Tolerance = ellipseGauge.GetTolerance()
        
        f64Radius1Tolerance = f64Tolerance if fleRegion.radius1 >= fleRegion.radius2 else f64Tolerance * (fleRegion.radius1 / fleRegion.radius2)
        f64Radius2Tolerance = f64Tolerance * (fleRegion.radius2 / fleRegion.radius1) if fleRegion.radius1 >= fleRegion.radius2 else f64Tolerance

        # 설정된 ROI에 대해 내부 및 외부 측정영역을 디스플레이 합니다. // Display the inner and outer measurement areas for the set ROI.
        if f64Radius1 < f64Radius1Tolerance or f64Radius2 < f64Radius2Tolerance:
            fleInner.Set(fleInner.GetCenter().x, fleInner.GetCenter().y, 0.1, 0.1)
        else:
            fleInner.radius1 -= f64Radius1Tolerance
            fleInner.radius2 -= f64Radius2Tolerance

        fleOuter.radius1 += f64Radius1Tolerance
        fleOuter.radius2 += f64Radius2Tolerance

        if (res := layer.DrawFigureImage(fleInner, EColor.RED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if (res := layer.DrawFigureImage(fleOuter, EColor.RED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if res.IsOK():
            # 추정된 타원을 디스플레이 합니다. // Display the estimated ellipse.
            if (res := layer.DrawFigureImage(fleResult, EColor.BLACK, 5)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            if (res := layer.DrawFigureImage(fleResult, EColor.CYAN, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            # 타원의 정보를 Console창에 출력합니다. // Output the original information to the console window.
            
            res, f64Radius1 = fleResult.GetRadius1(0)
            res, f64Radius2 = fleResult.GetRadius2(0)
            f64Angle = fleResult.GetAngle();
            flpLineCenter = CFLPoint[Double]()
            fleResult.GetCenter(flpLineCenter)
            print("Ellipse Center : ({}, {})\nRadius X : {} pixels\nRadius Y : {} pixels\nAngle : {}˚".format(flpLineCenter.x, flpLineCenter.y, f64Radius1, f64Radius2, f64Angle))

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