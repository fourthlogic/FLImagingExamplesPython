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

# 메인 함수 // Main function
def main():
    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImage = CGUIViewImage()
    res = CResult()

    # 이미지 로드 // Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/Rect.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 // Create image view
    if (res := viewImage.Create(200, 0, 968, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.\n")
        return

    # 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
    if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return

    # Image 크기에 맞게 view의 크기를 조정 // Zoom the view to fit the image size
    if (res := viewImage.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit\n")
        return
    
    # Corner Gauge 객체 생성 // Create Corner Gauge Object
    cornerGauge = CCornerGauge()
    
    # 처리할 이미지 설정 // Set the image to process
    cornerGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. // Set the area to measure.
    measureRegion = CFLRect[Double](213.577428, 262.324155, 295.020437, 348.179290)
    tolerance = 100.0
    cornerGauge.SetMeasurementRegion(measureRegion, tolerance)
    
    # 코너를 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. // Set the boundary point change direction to extract to estimate the corner.
    cornerGauge.SetTransitionType(CCornerGauge.ETransitionType.DarkToBrightOrBrightToDark)
    # 코너를 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. // Select the boundary point type to use among the boundary points extracted to estimate the corner.
    cornerGauge.SetTransitionChoice(CCornerGauge.ETransitionChoice.Closest)
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
    
    # 알고리즘 수행 // Execute the Algoritm
    if (res := cornerGauge.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute Corner gauge.")
        return

    
    layer = viewImage.GetLayer(0)
    layer.Clear()

    # 실행 결과를 가져옵니다. // Get the execution result.
    flfaResultLine = CFLFigureArray()
        
    # 추정된 코너를 가져옵니다. // Get the estimated corner.
    res = cornerGauge.GetMeasuredLines(flfaResultLine)[0]
        
    layer.DrawFigureImage(flfaResultLine, EColor.BLACK, 5)
    layer.DrawFigureImage(flfaResultLine, EColor.CYAN, 3)

        
    arrLines = [CFLLine[Double]() for v in range(2)];
    arrLines[0].Set(flfaResultLine.GetAt(0));
    arrLines[1].Set(flfaResultLine.GetAt(1));

    # 실행 결과를 가져옵니다. // Get the execution result.
    flfaResultCorners = CFLFigureArray();
    # 추정된 코너를 가져옵니다. // Get the estimated corner.
    cornerGauge.GetMeasuredObject(flfaResultCorners);

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
    cornerGauge.GetMeasuredValidPoints(flfaResultsValid)
    # 추정된 코너를 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. // Get an invalid boundary point that is not used to extract the estimated corner.
    cornerGauge.GetMeasuredInvalidPoints(flfaResultsInvalid)

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
        return

    # 이미지 뷰를 갱신 합니다. // Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()