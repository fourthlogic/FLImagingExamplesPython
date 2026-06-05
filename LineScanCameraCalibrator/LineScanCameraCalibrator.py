# FLImagingClrPy 선언 # Declare FLImagingClrPy
from asyncio.windows_events import NULL
from FLImagingClrPy import *

from enum import IntEnum

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
    if len(str) > 1:
        print(str)

    print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


    
# 메인 함수 # Main function
def main():

    class EView(IntEnum):
        Calibration = 0
        Source = 1
        Destination = 2
        Count = 3

    # 이미지 객체 선언 # Declare the image object
    fliImage = [CFLImage(),CFLImage(),CFLImage()]

    # 이미지 뷰 선언 # Declare the image view
    arrViewImage =  [CGUIViewImage(),CGUIViewImage(),CGUIViewImage()]

    strViewName = ["Calibration View", "Source View", "Destination View"]

    res = CResult()

    while True:
        # Learn 이미지 로드 # Load the Learn image
        if (res := fliImage[EView.Calibration].Load("../../ExampleImages/LineScanCameraCalibrator/Calibration Image.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        fliImage[EView.Source].Assign(fliImage[EView.Calibration])

        for i in range(EView.Count):
            # Learn 이미지 뷰 생성 # Create the Learn image view
            if (res := arrViewImage[i].Create(300 + 480 * i, 0, 300 + 480 * (i + 1), 360)).IsFail():
                ErrorPrint(res, "Failed to create the image view.\n")
                break

            # Learn 이미지 뷰에 이미지를 디스플레이 # Display the image in the Learn image view
            if (res := arrViewImage[i].SetImagePtr(fliImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                break

            # 두 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoints of the two image views.

            if i != 0:
                if (res := arrViewImage[i].SynchronizePointOfView(arrViewImage[0])[0]).IsFail():
                    ErrorPrint(res, "Failed to synchronize view\n")
                    break

        if (res := arrViewImage[EView.Calibration].ZoomFit()).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        # calibration
        # 캘리브레이션 객체 생성 # Create Calibrator object
        lineScanCameraCalibrator = CLineScanCameraCalibrator()

        # 캘리브레이션 이미지 설정 # Set calibration image
        lineScanCameraCalibrator.SetCalibrationImage(fliImage[EView.Calibration])
        # 보드의 셀 간격 설정(mm) # Sets the board cell pitch (mm).
        lineScanCameraCalibrator.SetCellPitch(10)
        # 카메라의 픽셀 정밀도 설정(mm) # Sets the camera pixel accuracy (mm).
        lineScanCameraCalibrator.SetPixelAccuracy(0.19)

        # 측정 기준 위치 설정. x축 좌표는 무시되며 y축 좌표기준으로 이미지 범위의 line을 검사
        # Sets the measurement reference position. The x-coordinate is ignored, and the image is inspected along the y-coordinate.
        flp = CFLPoint[Double](0, 160)
        lineScanCameraCalibrator.SetMeasurementPosition(flp)

        # 캘리브레이션 # Calibration
        if (res := lineScanCameraCalibrator.Calibrate()).IsFail():
            ErrorPrint(res, "Undistortion failed\n")
            break

        # 캘리브레이션 결과 출력 # Display the calibration result.
        layer = arrViewImage[EView.Calibration].GetLayer(0)

        # 셀 간격의 픽셀 크기 # Cell pitch in pixels.
        f64PixelPerPitch = lineScanCameraCalibrator.GetCellPitch() / lineScanCameraCalibrator.GetPixelAccuracy()

        # 실제 측정되는 범위 # Actual measurement range.
        fllMeasurementLine = CFLLine[Double]()

        fllMeasurementLine.flpPoints[0].x = 0
        fllMeasurementLine.flpPoints[1].x = fliImage[EView.Calibration].GetWidth()

        fllMeasurementLine.flpPoints[0].y = fllMeasurementLine.flpPoints[1].y = flp.y

        # 측정된 결과 제어점 # Measured control points.
        flpaCalibratedPoints = CFLPointArray()
        flpaCalibratedPoints = lineScanCameraCalibrator.GetCalibratedControlPoints(flpaCalibratedPoints)[1]

        flfaCrosshair = CFLFigureArray()
        flfaCrosshair = flpaCalibratedPoints.MakeCrossHairElementwise(flfaCrosshair, f64PixelPerPitch / 10, True)[1]

        layer.DrawFigureImage(fllMeasurementLine, EColor.RED, 2)
        layer.DrawFigureImage(flfaCrosshair, EColor.CYAN, 2)

        # execute (undistortion)
        # 연산 이미지, 연산 결과 이미지 설정 # Set source image, destination image
        lineScanCameraCalibrator.SetSourceImage(fliImage[EView.Source])
        lineScanCameraCalibrator.SetDestinationImage(fliImage[EView.Destination])

        # 왜곡 보정 동작 # Undistortion
        if (res := lineScanCameraCalibrator.Execute()).IsFail():
            ErrorPrint(res, "Undistortion failed\n")
            break

        # 뷰 이름 출력 # display view name
        for i in range(EView.Count):
            currentLayer = arrViewImage[i].GetLayer(0)

            currentLayer.DrawTextImage(CFLPoint[Double](), strViewName[i], EColor.YELLOW, EColor.BLACK, 20)
            arrViewImage[i].Invalidate()

        # The image view is waiting until close.
        bAvailable = True

        while bAvailable == True:
            for i in range(EView.Count):
                bAvailable &= arrViewImage[i].IsAvailable()

            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()
