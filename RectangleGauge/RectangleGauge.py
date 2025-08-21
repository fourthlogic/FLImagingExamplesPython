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
    viewImage = CGUIViewImage()
    res = CResult()

    # 이미지 로드 # Load image
    if (res := fliImage.Load("../../ExampleImages/Gauge/Rect.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 # Create image view
    if (res := viewImage.Create(200, 0, 968, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.\n")
        return

    # 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
    if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return

    # Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
    if (res := viewImage.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit\n")
        return
    
    # Rectangle Gauge 객체 생성 # Create Rectangle Gauge Object
    rectangleGauge = CRectangleGauge()
    
    # 처리할 이미지 설정 # Set the image to process
    rectangleGauge.SetSourceImage(fliImage)

    # 측정할 영역을 설정합니다. # Set the area to measure.
    measureRegion = CFLRect[Double](213.577428, 262.324155, 295.020437, 348.179290)
    tolerance = 25.0
    rectangleGauge.SetMeasurementRegion(measureRegion, tolerance)
    
    # 사각형을 추정하기위해 추출할 경계점 변화 방향에 대해 설정합니다. # Set the boundary point change direction to extract to estimate the rectangle.
    rectangleGauge.SetTransitionType(CRectangleGauge.ETransitionType.DarkToBrightOrBrightToDark)
    # 사각형을 추정하기위해 추출한 경계점 중 사용할 경계점 유형을 선택합니다. # Select the boundary point type to use among the boundary points extracted to estimate the rectangle.
    rectangleGauge.SetTransitionChoice(CRectangleGauge.ETransitionChoice.Closest)
    # 추출하기위한 파라미터를 설정합니다. # Set parameters for extraction.                
    # 사각형을 추정하기위해 추출할 경계점의 변화 임계값에 대해 설정합니다. # Set the threshold change of the boundary point to be extracted to estimate the rectangle.
    rectangleGauge.SetThreshold(20)
    # 사각형을 추정하기위해 추출할 경계점의 변화 임계값에 보정값을 설정합니다. # Set the correction value to the threshold change of the boundary point to be extracted to estimate the rectangle.
    rectangleGauge.SetMinimumAmplitude(10)
    # 사각형을 추정하기위해 추출할 경계점들의 대표값 표본 개수를 설정합니다. # Set the number of representative sample values ??of the boundary points to be extracted to estimate the rectangle.
    rectangleGauge.SetThickness(1)
    # 사각형을 추정하기위해 추출할 경계점들의 추출 간격을 설정합니다. # Set the extraction interval of boundary points to be extracted to estimate the rectangle.
    rectangleGauge.SetSamplingStep(1)
    # 사각형을 추정하기위해 추출할 경계점들의 이상치 조정을 위한 임계값을 설정합니다. # Set the threshold value for outlier adjustment of the boundary points to be extracted to estimate the rectangle.
    rectangleGauge.SetOutliersThreshold(3)
    # 사각형을 추정하기위해 추출할 경계점들의 이상치 조정 횟수을 설정합니다. # Set the number of outlier adjustments for boundary points to be extracted to estimate the rectangle.
    rectangleGauge.SetOutliersThresholdCount(3)
    # 사각형을 추정하기위해 점 클러스터링 처리 유무에 대한 설정을 합니다. # Set whether or not to process point clustering to estimate the rectangle.
    rectangleGauge.EnableClusterMode(True)
    # 사각형을 추정하기위해 마진을 설정합니다. 필요에 따라 각 구역별로 설정가능합니다. # Set the margin to estimate the rectangle. It can be set for each zone as needed.
    rectangleGauge.SetMeasurementMarginRatio(0, CRectangleGauge.EMargin.All)
    # 사각형을 추정하기위한 Tolerance를 설정합니다. 필요에 따라 각 구역별로 설정가능합니다. # Set the Tolerance for estimating the rectangle. It can be set for each zone as needed.
    rectangleGauge.SetTolerance(tolerance, CRectangleGauge.ETolerance.All)
    
    # 알고리즘 수행 # Execute the Algoritm
    if (res := rectangleGauge.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute Rectangle gauge.")
        return

    
    layer = viewImage.GetLayer(0)
    layer.Clear()

    # 실행 결과를 가져옵니다. # Get the execution result.
    flrResult = CFLRect[Double]()
        
    # 추정된 사각형을 가져옵니다. # Get the estimated rectangle.
    res = rectangleGauge.GetMeasuredObject(flrResult)[0]
    
    flrRegion = rectangleGauge.GetMeasurementRegion()
    arrTolerance = rectangleGauge.GetTolerance()
    f64Tolerance = arrTolerance[0]

    arrF64Tolerance = [0.0, 0.0, 0.0, 0.0]
    f64WidthTolerance = 0
    f64HeightTolerance = 0
    f64Ratio = 0

    f64Height = flrRegion.GetHeight()
    f64Width = flrRegion.GetWidth()

    # 설정된 ROI에 대해 내부 및 외부 측정영역을 디스플레이 합니다. # Display the inner and outer measurement areas for the set ROI.
    if f64Height >= f64Width:
        f64Ratio = f64Width / f64Height

        f64MinTolerance = f64Height / 2.0

        if f64Tolerance >= f64MinTolerance:
            f64Tolerance = f64MinTolerance

        f64HeightTolerance = f64Tolerance
        f64WidthTolerance = f64HeightTolerance * f64Ratio

    if f64Height < f64Width:
        f64Ratio = f64Height / f64Width

        f64MinTolerance = f64Width / 2.0

        if f64Tolerance >= f64MinTolerance:
            f64Tolerance = f64MinTolerance

        f64WidthTolerance = f64Tolerance
        f64HeightTolerance = f64WidthTolerance * f64Ratio

    for i in range(2):
        arrF64Tolerance[2 * i] = f64WidthTolerance
        arrF64Tolerance[2 * i + 1] = f64HeightTolerance

    flpCent = flrRegion.GetCenter()
    flrInner = CFLRect[Double](flrRegion)
    flrOuter = CFLRect[Double](flrRegion)

    if flrInner.GetWidth() / 2.0 <= arrF64Tolerance[0] or flrInner.GetHeight() / 2.0 <= arrF64Tolerance[1]:
        flpPosition = flrInner.GetCenter()

        if (res := layer.DrawFigureImage(flpPosition, EColor.RED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return
    else:
        flrInner.Offset(-flpCent.x, -flpCent.y)
        flrInner.Multiply((flrRegion.GetWidth() - arrF64Tolerance[0] * 2.0) / flrRegion.GetWidth(), (flrRegion.GetHeight() - arrF64Tolerance[1] * 2.0) / flrRegion.GetHeight())
        flrInner.Offset(flpCent)

        if (res := layer.DrawFigureImage(flrInner, EColor.RED)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

    flrOuter.Offset(-flpCent.x, -flpCent.y)
    flrOuter.Multiply((flrRegion.GetWidth() + arrF64Tolerance[0] * 2.0) / flrRegion.GetWidth(), (flrRegion.GetHeight() + arrF64Tolerance[1] * 2.0) / flrRegion.GetHeight())
    flrOuter.Offset(flpCent)

    if (res := layer.DrawFigureImage(flrOuter, EColor.RED)).IsFail():
        ErrorPrint(res, "Failed to draw figure")
        return

    if res.IsOK():
        # 추정된 사각형을 디스플레이 합니다. # Display the estimated rectangle.
        if (res := layer.DrawFigureImage(flrResult, EColor.BLACK, 5)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

        if (res := layer.DrawFigureImage(flrResult, EColor.CYAN, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            return

        # 사각형의 정보를 Console창에 출력합니다. # Output the square information to the console window.
        f64ResultWidth = 0
        f64ResultHeight = 0
        f64ResultAngle = 0
        f64ResultWidth = flrResult.GetWidth()
        f64ResultHeight = flrResult.GetHeight()
        f64ResultAngle = flrResult.GetAngle()
        flpLineCenter = flrResult.GetCenter()
        print("Rectangle Center : ({0}, {1})\nWidth : {2} pixels\nHeight : {3} pixels\nAngle : {4}˚".format(flpLineCenter.x, flpLineCenter.y, f64ResultWidth, f64ResultHeight, f64ResultAngle))
            
    flfaResultsValid = CFLFigureArray()
    flfaResultsInvalid = CFLFigureArray()

    # 추정된 사각형을 추출에 사용된 유효 경계점을 가져옵니다. # Get the effective boundary point used to extract the estimated rectangle.
    rectangleGauge.GetMeasuredValidPoints(flfaResultsValid)
    # 추정된 사각형을 추출에 사용되지 못한 유효하지 않은 경계점을 가져옵니다. # Get an invalid boundary point that is not used to extract the estimated rectangle.
    rectangleGauge.GetMeasuredInvalidPoints(flfaResultsInvalid)

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
        return

    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()