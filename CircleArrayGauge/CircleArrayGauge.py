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
    
    # 이미지 객체 선언 # Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 # Declare the image view
    arrViewImage = CGUIViewImage()
    res = CResult()

    # 이미지 로드 # Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/Circle Array.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 # Create image view
    if (res := arrViewImage.Create(100, 100, 600, 600)).IsFail():
        ErrorPrint(res, "Failed to create the image view.\n")
        return

    # 이미지 뷰에 이미지를 디스플레이 # display the image in the imageview
    if (res := arrViewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return

    # Circle Gauge 객체 생성 # Create Circle Gauge Object
    circleArrayGauge = CCircleArrayGauge()
    
    # 처리할 이미지 설정 # Set the image to process
    circleArrayGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. # Set the area to measure.
    flfaMeasurementRegion = CFLFigureArray()
    flfaMeasurementRegion.Load("../../ExampleImages/Gauge/Circle Array Measurement Region")
    tolerance = 15
    circleArrayGauge.SetMeasurementRegion(flfaMeasurementRegion, tolerance)

    # 추출하기위한 파라미터를 설정합니다. # Set parameters for extraction.                
    # 원을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. # Set the threshold change of the boundary point to be extracted to estimate the circle.
    circleArrayGauge.SetThreshold(20)
    # 원을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. # Set the correction value to the threshold change of the boundary point to be extracted to estimate the circle.
    circleArrayGauge.SetMinimumAmplitude(10)
    # 원을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. # Set the number of representative sample values ??of the boundary points to be extracted to estimate the circle.
    circleArrayGauge.SetThickness(3)
    # 원을 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. # Set the extraction interval of boundary points to be extracted to estimate the circle.
    circleArrayGauge.SetSamplingStep(1)
    # 원을 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. # Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the circle.
    circleArrayGauge.SetOutliersThreshold(3)
    # 원을 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. # Set the number of outlier adjustments for boundary points to be extracted to estimate the circle.
    circleArrayGauge.SetOutliersThresholdCount(3)

    # 원을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. # Set the boundary point change direction to extract to estimate the circle.
    circleArrayGauge.SetTransitionType(CCircleGauge.ETransitionType.BrightToDark)
    # 원을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. # Select the boundary point type to use among the boundary points extracted to estimate the circle.
    circleArrayGauge.SetTransitionChoice(CCircleGauge.ETransitionChoice.LargestAmplitude)

    # 알고리즘 수행 # Execute the Algoritm
    if (res := circleArrayGauge.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute Circle gauge.")
        return

    # 실행 결과를 가져옵니다. # Get the execution result.
    flfaResult = CFLFigureArray()
    flfaResultsValid = CFLFigureArray()
    flfaResultsInvalid = CFLFigureArray()

    # 실행 결과를 가져옵니다. # Get the execution result. # Get the execution result.
    res = circleArrayGauge.GetMeasuredObject(flfaResult)[0]
    # 추정된 원을 추출에 사용된 유효 경계점을 가져옵니다. # Get the effective boundary point used to extract the estimated circle.
    circleArrayGauge.GetMeasuredValidPoints(flfaResultsValid)
    # 추정된 원을 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. # Get an invalid boundary point that is not used to extract the estimated circle.
    circleArrayGauge.GetMeasuredInvalidPoints(flfaResultsInvalid)

    layer = arrViewImage.GetLayer(0)

    layer.Clear()

    # 측정 영역이 어디인지 알기 위해 디스플레이 한다 # Display to know where the measurement area is
    flfaMeasurementToleranceRegion = circleArrayGauge.GetActualMeasurementRegion();

    if (res := layer.DrawFigureImage(flfaMeasurementToleranceRegion, EColor.BLUE)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    if (res := layer.DrawFigureImage(flfaMeasurementToleranceRegion, EColor.BLUE)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return
    
    # 추정된 원을 디스플레이 합니다. # Display the estimated circle.
    if (res := layer.DrawFigureImage(flfaResult, EColor.BLACK, 5)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    if (res := layer.DrawFigureImage(flfaResult, EColor.CYAN, 3)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    # 원의 정보를 Console창에 출력합니다. # Output the original information to the console window.
    for i in range(flfaResult.GetCount()):
        flcRes = CFLCircle[Double](flfaResult.GetAt(i))
        f64Radius = flcRes.GetRadius()
        flpCenter = CFLPoint[Double]()
        flcRes.GetCenter(flpCenter)
        Console.WriteLine("[{}]Circle Center : ({}, {})\nRadius : {} pixels".format(i, flpCenter.x, flpCenter.y, f64Radius))

    # 추출된 유효점이 어디인지 알기 위해 디스플레이 한다 # Display to know where the extracted valid point is
    flfaValidCrossHair = CFLFigureArray()
    flfaValidCrossHair = flfaResultsValid.MakeCrossHairElementwise(flfaValidCrossHair, 1.0, True)[1]

    if (res := layer.DrawFigureImage(flfaValidCrossHair, EColor.LIME)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return


    # 추출된 유효하지 않은 점이 어디인지 알기 위해 디스플레이 한다 # Display to see where the extracted invalid points are
    flfaInvalidCrossHair = CFLFigureArray()
    flfaInvalidCrossHair = flfaResultsInvalid.MakeCrossHairElementwise(flfaInvalidCrossHair, 1.0, True)[1]

    if (res := layer.DrawFigureImage(flfaInvalidCrossHair, EColor.RED)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    # 이미지 뷰를 갱신 합니다. # Update the image view.
    arrViewImage.Invalidate()
        
    while arrViewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()