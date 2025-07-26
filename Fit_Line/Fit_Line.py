# FLImagingClrPy 선언 // Declare FLImagingClrPy
from pickle import LONG
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():
	
    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage() for _ in range(3)]

    while True:

        # View 1 생성 // Create View 1
        if (res := viewImage[0].Create(200, 0, 700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # View 2 생성 // Create View 2
        if (res := viewImage[1].Create(700, 0, 1200, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # View 3 생성 // Create View 3
        if (res := viewImage[2].Create(1200, 0, 1700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 각 이미지 뷰의 시점을 동기화 한다. // Synchronize the viewpoint of each image view.
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break
        if (res := viewImage[1].SynchronizePointOfView(viewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 각 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the position of each image view window
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break
        if (res := viewImage[1].SynchronizeWindow(viewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 화면에 출력하기 위해 Image View 에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
        layer = [viewImage[0].GetLayer(0), viewImage[1].GetLayer(0), viewImage[2].GetLayer(0)]

        # 화면상 좌표(고정 좌표)에 View 의 이름을 표시
        # Indicates view name on screen coordinates (fixed coordinates)
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 0), "Default", EColor.YELLOW, EColor.BLACK, 30)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 0), "Parameter 1", EColor.YELLOW, EColor.BLACK, 30)
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 0), "Parameter 2", EColor.YELLOW, EColor.BLACK, 30)

        # (x1, y1) = (100, 400), (x2, y2) = (400, 100) 선 생성
        # (x1, y1) = (100, 400), (x2, y2) = (400, 100) Create Line
        fll = CFLLine[Double](100, 400, 400, 100)

        # 선 위의 점들을 추출 // Sample points on a line
        flfaSrc = CFLFigureArray()

        res, flfaSrc = fll.GetSamplingPointsOnSegment(10, flfaSrc)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # Noise 가 추가된 PointArray 생성 // Create a PointArray with noise added
        flpaNoise = CFLPointArray()
        f64Epsilon = 10.0

        for i in range(flfaSrc.GetCount()):
            f64RandomVal = CRandomGenerator.Double(-f64Epsilon, f64Epsilon)
            flpaNoise.PushBack(CFLPoint[Double](flfaSrc.GetAt(i).GetCenter().x + f64RandomVal, flfaSrc.GetAt(i).GetCenter().y + f64RandomVal))


        fllResult1 = CFLLine[Double]()
        i64OutlierThresholdCount1 = 0

        # Fit 함수 실행 (Default parameter) // Fit function execution (Default parameter)
        if (res := fllResult1.Fit(flpaNoise)).IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # 0번 Layer 에 Figure 와 Text 를 출력 // Draw Figure and Text to Layer 0
        layer[0].DrawFigureImage(fllResult1, EColor.BLACK, 5)
        layer[0].DrawFigureImage(fllResult1, EColor.CYAN, 3)
        layer[0].DrawFigureImage(flpaNoise, EColor.BLACK, 3)
        layer[0].DrawFigureImage(flpaNoise, EColor.LIME, 1)
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 40), f"Outlier Threshold Count : {i64OutlierThresholdCount1}", EColor.YELLOW, EColor.BLACK, 15)
        layer[0].DrawTextImage(CFLPoint[Int32](350, 350), f"(x1, y1) = ({fllResult1.flpPoints[0].x:.3f},{fllResult1.flpPoints[0].y:.3f})\r\n(x2, y2) = ({fllResult1.flpPoints[1].x:.3f},{fllResult1.flpPoints[1].y:.3f})\r\nAngle = {fllResult1.GetAngle():.3f}", EColor.YELLOW, EColor.BLACK, 13, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)


        fllResult2 = CFLLine[Double]()
        i64OutlierThresholdCount2 = 1
        f64OutlierThreshold2 = 1.7
        listOutlierIndices2 = List[Int64]()
        flpaOutlier2 = CFLPointArray()

        # Fit 함수 실행 (Parameter1) // Fit function execution (Parameter1)
        res, listOutlierIndices2 = fllResult2.Fit(flpaNoise, i64OutlierThresholdCount2, f64OutlierThreshold2, listOutlierIndices2)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # Outlier 인덱스로 Outlier PointArray 추가 // Add Outlier PointArray as Outlier Index
        for i in range(len(listOutlierIndices2)):
            flpaOutlier2.PushBack(flpaNoise.GetAt(listOutlierIndices2[i]))

        # 1번 Layer 에 Figure 와 Text 를 출력 // Draw Figure and Text to Layer 1
        layer[1].DrawFigureImage(fllResult2, EColor.BLACK, 5)
        layer[1].DrawFigureImage(fllResult2, EColor.CYAN, 3)
        layer[1].DrawFigureImage(flpaNoise, EColor.BLACK, 3)
        layer[1].DrawFigureImage(flpaNoise, EColor.LIME, 1)
        layer[1].DrawFigureImage(flpaOutlier2, EColor.RED, 1)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 40), f"Outlier Threshold Count : {i64OutlierThresholdCount2}\r\nOutlier Threshold : {f64OutlierThreshold2:.3f}", EColor.YELLOW, EColor.BLACK, 15)
        layer[1].DrawTextImage(CFLPoint[Int32](350, 350), f"(x1, y1) = ({fllResult2.flpPoints[0].x:.3f},{fllResult2.flpPoints[0].y:.3f})\r\n(x2, y2) = ({fllResult2.flpPoints[1].x:.3f},{fllResult2.flpPoints[1].y:.3f})\r\nAngle = {fllResult2.GetAngle():.3f}", EColor.YELLOW, EColor.BLACK, 13, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        fllResult3 = CFLLine[Double]()
        i64OutlierThresholdCount3 = 3
        f64OutlierThreshold3 = 1.0
        listOutlierIndices3 = List[Int64]()
        flpaOutlier3 = CFLPointArray()

        # Fit 함수 실행 (Parameter2) // Fit function execution (Parameter2)
        res, listOutlierIndices3 = fllResult3.Fit(flpaNoise, i64OutlierThresholdCount3, f64OutlierThreshold3, listOutlierIndices3)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # Outlier 인덱스로 Outlier PointArray 추가 // Add Outlier PointArray as Outlier Index
        for i in range(len(listOutlierIndices3)):
            flpaOutlier3.PushBack(flpaNoise.GetAt(listOutlierIndices3[i]))

        # 2번 Layer 에 Figure 와 Text 를 출력 // Draw Figure and Text to Layer 2
        layer[2].DrawFigureImage(fllResult3, EColor.BLACK, 5)
        layer[2].DrawFigureImage(fllResult3, EColor.CYAN, 3)
        layer[2].DrawFigureImage(flpaNoise, EColor.BLACK, 3)
        layer[2].DrawFigureImage(flpaNoise, EColor.LIME, 1)
        layer[2].DrawFigureImage(flpaOutlier3, EColor.RED, 1)
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 40), f"Outlier Threshold Count : {i64OutlierThresholdCount3}\r\nOutlier Threshold : {f64OutlierThreshold3:.3f}", EColor.YELLOW, EColor.BLACK, 15)
        layer[2].DrawTextImage(CFLPoint[Int32](350, 350), f"(x1, y1) = ({fllResult3.flpPoints[0].x:.3f},{fllResult3.flpPoints[0].y:.3f})\r\n(x2, y2) = ({fllResult3.flpPoints[1].x:.3f},{fllResult3.flpPoints[1].y:.3f})\r\nAngle = {fllResult3.GetAngle():.3f}", EColor.YELLOW, EColor.BLACK, 13, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)


        # Console 출력 // Console output
        print("Source Points (With noise)\n") # C# 코드에서 "Withref noise"를 "With noise"로 수정 // Modified "Withref noise" to "With noise" in C# code
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaSrc)}\n\n")

        print("Source Points (With noise)\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaNoise)}\n\n")

        print("[Default parameter]\n")
        print(f"Outlier Threshold Count : {i64OutlierThresholdCount1}\n")
        print("Result Line : \n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(fllResult1)}\n\n")

        print("[Parameter 1]\n")
        print(f"Outlier Threshold Count : {i64OutlierThresholdCount2}\n")
        print(f"Outlier Threshold : {f64OutlierThreshold2:.3f}\n")
        print("Result Line : \n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(fllResult2)}\n\n")

        print("[Parameter 2]\n")
        print(f"Outlier Threshold Count : {i64OutlierThresholdCount3}\n")
        print(f"Outlier Threshold : {f64OutlierThreshold3:.3f}\n")
        print("Result Line : \n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(fllResult3)}\n\n")


        # 이미지 뷰들을 갱신 합니다. // Update the image views.
        for i in range(3):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 셋중에 하나라도 꺼지면 종료로 간주 // Consider closed when any of the three image views are turned off
        while all(view.IsAvailable() for view in viewImage):
            CThreadUtilities.Sleep(1)

        break
    
    # End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()