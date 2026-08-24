# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
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
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightOrBrightToDark,
        CCircleGauge.ETransitionType.DarkToBright,
        CCircleGauge.ETransitionType.BrightToDark,
        CCircleGauge.ETransitionType.DarkToBrightToDark
    ]

    arrTransitionChoice = [
        CCircleGauge.ETransitionChoice.Begin,
        CCircleGauge.ETransitionChoice.Begin,
        CCircleGauge.ETransitionChoice.Begin,
        CCircleGauge.ETransitionChoice.LargestArea,
        CCircleGauge.ETransitionChoice.End,
        CCircleGauge.ETransitionChoice.End,
        CCircleGauge.ETransitionChoice.End,
        CCircleGauge.ETransitionChoice.LargestAmplitude,
        CCircleGauge.ETransitionChoice.Closest,
        CCircleGauge.ETransitionChoice.Closest,
        CCircleGauge.ETransitionChoice.Closest,
        CCircleGauge.ETransitionChoice.Closest
    ]

    i32ExampleCount = len(arrViewText)

    # 이미지 객체 선언 # Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 # Declare the image view
    arrViewImage = [CGUIViewImage() for v in range(i32ExampleCount)]
    res = CResult()

    # 이미지 로드 # Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/Circle.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 # Create image view
    for i in range(i32ExampleCount):        
        i32X = 300 * (i % 4)
        i32Y = 300 * int(i / 4)

        if (res := arrViewImage[i].Create(i32X, i32Y, i32X + 300, i32Y + 300)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰에 이미지를 디스플레이 # display the image in the imageview
        if (res := arrViewImage[i].SetImagePtr(fliImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            break

        # 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the all image views. 
        if i > 0:
            if (res := arrViewImage[i].SynchronizePointOfView(arrViewImage[0])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                break

    # Circle Gauge 객체 생성 # Create Circle Gauge Object
    circleGauge = CCircleGauge()
    
    # 처리할 이미지 설정 # Set the image to process
    circleGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. # Set the area to measure.
    measureRegion = CFLCircle[Double](260.0, 265.0, 120.0)
    tolerance = 100
    circleGauge.SetMeasurementRegion(measureRegion, tolerance)

    # 추출하기위한 파라미터를 설정합니다. # Set parameters for extraction.                
    # 원을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. # Set the threshold change of the boundary point to be extracted to estimate the circle.
    circleGauge.SetThreshold(20)
    # 원을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. # Set the correction value to the threshold change of the boundary point to be extracted to estimate the circle.
    circleGauge.SetMinimumAmplitude(10)
    # 원을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. # Set the number of representative sample values ??of the boundary points to be extracted to estimate the circle.
    circleGauge.SetThickness(3)
    # 원을 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. # Set the extraction interval of boundary points to be extracted to estimate the circle.
    circleGauge.SetSamplingStep(1)
    # 원을 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. # Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the circle.
    circleGauge.SetOutliersThreshold(3)
    # 원을 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. # Set the number of outlier adjustments for boundary points to be extracted to estimate the circle.
    circleGauge.SetOutliersThresholdCount(3)

    for i in range(i32ExampleCount):
        # 원을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. # Set the boundary point change direction to extract to estimate the circle.
        circleGauge.SetTransitionType(arrTransitionType[i])
        # 원을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. # Select the boundary point type to use among the boundary points extracted to estimate the circle.
        circleGauge.SetTransitionChoice(arrTransitionChoice[i])

        # 알고리즘 수행 # Execute the Algoritm
        if (res := circleGauge.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Circle gauge.")
            break

        # 실행 결과를 가져옵니다. # Get the execution result.
        flcResult = CFLCircle[Double]()
        flfaResultsValid = CFLFigureArray()
        flfaResultsInvalid = CFLFigureArray()

        # 실행 결과를 가져옵니다. # Get the execution result. # Get the execution result.
        res = circleGauge.GetMeasuredObject(flcResult, i % 4)[0]
        # 추정된 원을 추출에 사용된 유효 경계점을 가져옵니다. # Get the effective boundary point used to extract the estimated circle.
        circleGauge.GetMeasuredValidPoints(flfaResultsValid, i % 4)
        # 추정된 원을 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. # Get an invalid boundary point that is not used to extract the estimated circle.
        circleGauge.GetMeasuredInvalidPoints(flfaResultsInvalid, i % 4)

        layer = arrViewImage[i].GetLayer(0)

        layer.Clear()

        if (res := layer.DrawTextImage(CFLPoint[Double](0, 0), arrViewText[i], EColor.YELLOW, EColor.BLUE, 20, True)).IsFail():
            ErrorPrint(res, "Failed to draw figure\n")
            break

        # 측정 영역이 어디인지 알기 위해 디스플레이 한다 # Display to know where the measurement area is
        flcRegion = circleGauge.GetMeasurementRegion()

        flcInner = CFLCircle[Double]()
        flcOuter = CFLCircle[Double]()
        f64Tolerance = circleGauge.GetTolerance()

        # 설정된 ROI에 대해 내부 및 외부 측정영역을 디스플레이 합니다. # Display the inner and outer measurement areas for the set ROI.

        flpRegionCenter = flcRegion.GetCenter()

        if flcRegion.radius < f64Tolerance:
            flcInner.Set(flpRegionCenter.x, flpRegionCenter.y, 0.1)
        else:
            flcInner.Set(flpRegionCenter.x, flpRegionCenter.y, flcRegion.radius - f64Tolerance)

        flcOuter.Set(flpRegionCenter.x, flpRegionCenter.y, flcRegion.radius + f64Tolerance)

        if (res := layer.DrawFigureImage(flcInner, EColor.RED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if (res := layer.DrawFigureImage(flcOuter, EColor.RED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if res.IsOK():
            # 추정된 원을 디스플레이 합니다. # Display the estimated circle.
            if (res := layer.DrawFigureImage(flcResult, EColor.BLACK, 5)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            if (res := layer.DrawFigureImage(flcResult, EColor.CYAN, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure")
                break

            # 원의 정보를 Console창에 출력합니다. # Output the original information to the console window.
            f64Radius = 0
            flcResult.GetRadius(f64Radius)
            flpLineCenter = CFLPoint[Double]()
            flcResult.GetCenter(flpLineCenter)
            Console.WriteLine("Circle Center : ({}, {})\nRadius : {} pixels".format(flpLineCenter.x, flpLineCenter.y, f64Radius))

        # 추출된 유효점이 어디인지 알기 위해 디스플레이 한다 # Display to know where the extracted valid point is
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

        # 추출된 유효하지 않은 점이 어디인지 알기 위해 디스플레이 한다 # Display to see where the extracted invalid points are
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

        # 측정 영역이 어디인지 알기 위해 디스플레이 한다 # Display to know where the measurement area is
        if (res := layer.DrawFigureImage(measureRegion, EColor.BLUE)).IsFail():
            ErrorPrint(res, "Failed to draw figures objects on the image view.")
            break

        # 이미지 뷰를 갱신 합니다. # Update the image view.
        arrViewImage[i].Invalidate()
        
    bAvailable = True

    while bAvailable:
        for i in range(i32ExampleCount):
            bAvailable &= arrViewImage[i].IsAvailable()

        CThreadUtilities.Sleep(1)
        
    for i in range(i32ExampleCount):
        arrViewImage[i].Destroy()


if __name__ == "__main__":
    main()