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
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCornerGauge.ETransitionType.DarkToBright,
        CCornerGauge.ETransitionType.BrightToDark,
        CCornerGauge.ETransitionType.DarkToBrightToDark
    ]

    arrTransitionChoice = [
        CCornerGauge.ETransitionChoice.Begin,
        CCornerGauge.ETransitionChoice.Begin,
        CCornerGauge.ETransitionChoice.Begin,
        CCornerGauge.ETransitionChoice.LargestArea,
        CCornerGauge.ETransitionChoice.End,
        CCornerGauge.ETransitionChoice.End,
        CCornerGauge.ETransitionChoice.End,
        CCornerGauge.ETransitionChoice.LargestAmplitude,
        CCornerGauge.ETransitionChoice.Closest,
        CCornerGauge.ETransitionChoice.Closest,
        CCornerGauge.ETransitionChoice.Closest,
        CCornerGauge.ETransitionChoice.Closest
    ]

    i32ExampleCount = len(arrViewText)

    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for v in range(i32ExampleCount)]
    res = CResult()

    # 이미지 로드 // Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/Rect.flif")).IsFail():
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
            if (res := arrViewImage[i].SynchronizePointOfView(arrViewImage[0])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                break

    # Corner Gauge 객체 생성 // Create Corner Gauge Object
    cornerGauge = CCornerGauge()
    
    # 처리할 이미지 설정 // Set the image to process
    cornerGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. // Set the area to measure.
    measureRegion = CFLRect[Double](213.577428, 262.324155, 295.020437, 348.179290)
    tolerance = 100.0
    cornerGauge.SetMeasurementRegion(measureRegion, tolerance)

    # 추출하기위한 파라미터를 설정합니다. // Set parameters for extraction.                
    # 코너를 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. // Set the threshold change of the boundary point to be extracted to estimate the corner.
    cornerGauge.SetThreshold(20)
    # 코너를 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. // Set the correction value to the threshold change of the boundary point to be extracted to estimate the corner.
    cornerGauge.SetMinimumAmplitude(10)
    # 코너를 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. // Set the number of representative sample values ??of the boundary points to be extracted to estimate the corner.
    cornerGauge.SetThickness(1)
    # 코너를 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. // Set the extraction interval of boundary points to be extracted to estimate the corner.
    cornerGauge.SetSamplingStep(1)
    # 코너를 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. // Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the corner.
    cornerGauge.SetOutliersThreshold(3)
    # 코너를 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. // Set the number of outlier adjustments for boundary points to be extracted to estimate the corner.
    cornerGauge.SetOutliersThresholdCount(3)
    # 코너를 추정하기위해 점 클러스터링 처리 유무에 대한 설정을 합니다. // Set whether or not to process point clustering to estimate the corner.
    cornerGauge.EnableClusterMode(True)
    # 코너를 추정하기위해 마진을 설정합니다. 필요에 따라 각 구역별로 설정가능합니다. // Set the margin to estimate the corner. It can be set for each zone as needed.
    cornerGauge.SetMeasurementMarginRatio(0, CCornerGauge.EMargin.All)
    # 코너를 추정하기위한 Tolerance를 설정합니다. 필요에 따라 각 구역별로 설정가능합니다. // Set the Tolerance for estimating the corner. It can be set for each zone as needed.
    cornerGauge.SetTolerance(tolerance, CCornerGauge.ETolerance.All)
    # 코너를 측정하기위한 영역을 설정합니다. // Set the area for measuring corners.
    cornerGauge.SetCorner(CCornerGauge.ECorner.All)

    for i in range(i32ExampleCount):
        # 코너를 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. // Set the boundary point change direction to extract to estimate the corner.
        cornerGauge.SetTransitionType(arrTransitionType[i])
        # 코너를 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 코너택합니다. // Select the boundary point type to use among the boundary points extracted to estimate the corner.
        cornerGauge.SetTransitionChoice(arrTransitionChoice[i])

        # 알고리즘 수행 // Execute the Algoritm
        if (res := cornerGauge.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Corner gauge.")
            break

        layer = arrViewImage[i].GetLayer(0)
        layer.Clear()
        
        if (res := layer.DrawTextImage(CFLPoint[Double](0, 0), arrViewText[i], EColor.YELLOW, EColor.BLUE, 20, True)).IsFail():
            ErrorPrint(res, "Failed to draw figure\n")
            break

        # 실행 결과를 가져옵니다. // Get the execution result.
        flfaResultLine = CFLFigureArray()
        
        # 추정된 코너를 가져옵니다. // Get the estimated corner.
        res = cornerGauge.GetMeasuredLines(flfaResultLine, i % 4)[0]
        
        layer.DrawFigureImage(flfaResultLine, EColor.BLACK, 5)
        layer.DrawFigureImage(flfaResultLine, EColor.CYAN, 3)

        
        arrLines = [CFLLine[Double]() for v in range(2)];
        arrLines[0].Set(flfaResultLine.GetAt(0));
        arrLines[1].Set(flfaResultLine.GetAt(1));

        # 실행 결과를 가져옵니다. // Get the execution result.
        flfaResultCorners = CFLFigureArray();
        # 추정된 코너를 가져옵니다. // Get the estimated corner.
        cornerGauge.GetMeasuredObject(flfaResultCorners, i % 4);

        layer.DrawFigureImage(flfaResultCorners, EColor.BLACK, 3);
        layer.DrawFigureImage(flfaResultCorners, EColor.CYAN, 1);

        for j in range(flfaResultCorners.GetCount()):
            print("#{} : Corner X : {}, Corner Y : {}".format(j, flfaResultCorners.GetAt(j).GetCenter().x, flfaResultCorners.GetAt(j).GetCenter().y))

        for j in range(2):
            f64ResultAngle = arrLines[j].GetAngle();
            print("Line Angle : {}˚".format(f64ResultAngle))
            
        flfaResultsValid = CFLFigureArray()
        flfaResultsInvalid = CFLFigureArray()

        # 추정된 코너를 추출에 사용된 유효 경계점을 가져옵니다. // Get the effective boundary point used to extract the estimated corner.
        cornerGauge.GetMeasuredValidPoints(flfaResultsValid, i % 4)
        # 추정된 코너를 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. // Get an invalid boundary point that is not used to extract the estimated corner.
        cornerGauge.GetMeasuredInvalidPoints(flfaResultsInvalid, i % 4)

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
            if flfaResultsInvalid.GetAt(i64Index).GetDeclType() != EFigureDeclType.Point:
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