# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():
	
    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage() for _ in range(4)]

    while True:

        # 이미지 뷰 생성 // Create image view
        if (res := viewImage[0].Create(400, 0, 812, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(812, 0, 1224, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[2].Create(400, 384, 812, 768)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[3].Create(812, 384, 1224, 768)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Minimum Thickness View, Maximum Thickness View 의 0번 레이어 가져오기 // Get Layer 0 of Minimum Thickness View, Maximum Thickness View
        layerMin0 = viewImage[0].GetLayer(0)
        layerMax0 = viewImage[1].GetLayer(0)
        layerMin1 = viewImage[2].GetLayer(0)
        layerMax1 = viewImage[3].GetLayer(0)

        layerMin0.DrawTextCanvas(CFLPoint[Double](0, 0), "Minimum Thickness", EColor.YELLOW, EColor.BLACK, 15)
        layerMax0.DrawTextCanvas(CFLPoint[Double](0, 0), "Maximum Thickness", EColor.YELLOW, EColor.BLACK, 15)
        layerMin1.DrawTextCanvas(CFLPoint[Double](0, 0), "Minimum Thickness", EColor.YELLOW, EColor.BLACK, 15)
        layerMax1.DrawTextCanvas(CFLPoint[Double](0, 0), "Maximum Thickness", EColor.YELLOW, EColor.BLACK, 15)
        layerMin0.DrawTextCanvas(CFLPoint[Double](0, 20), "Trim Ratio : Default", EColor.YELLOW, EColor.BLACK)
        layerMax0.DrawTextCanvas(CFLPoint[Double](0, 20), "Trim Ratio : Default", EColor.YELLOW, EColor.BLACK)
        layerMin1.DrawTextCanvas(CFLPoint[Double](0, 20), "Trim Ratio : 0.01", EColor.YELLOW, EColor.BLACK)
        layerMax1.DrawTextCanvas(CFLPoint[Double](0, 20), "Trim Ratio : 0.05", EColor.YELLOW, EColor.BLACK)

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        for i in range(1, 4):
            if (res := viewImage[0].SynchronizePointOfView(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize view")
                break

        if (res := viewImage[0].SynchronizePointOfView(viewImage[3])[0]).IsFail(): # 이전 루프에서 break가 발생했는지 다시 확인 // Check again if a break occurred in the previous loop
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
        for i in range(1, 4):
            if (res := viewImage[0].SynchronizeWindow(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize window.")
                break

        if (res := viewImage[0].SynchronizeWindow(viewImage[3])[0]).IsFail(): # 이전 루프에서 break가 발생했는지 다시 확인 // Check again if a break occurred in the previous loop
            break

        # 화면상에 잘 보이도록 좌표 0.5배율을 적용 // Apply 0.5 magnification to the coordinates so that they can be seen clearly on the screen
        f64Scale = 0.5
        # 화면상에 잘 보이도록 시점 Offset 조정 // Adjust the viewpoint offset so that it can be seen clearly on the screen
        f64CenterCoordX = 500.0
        f64CenterCoordY = 500.0
        viewImage[0].SetViewCenterAndScale(CFLPoint[Double](f64CenterCoordX, f64CenterCoordY), f64Scale)

        # Source Figure 불러오기 // Load source figure
        flfSource = CFigureUtilities.LoadFigure("../../ExampleImages/Figure/Thickness1.fig")

        # 도형의 최소 두께를 나타내는 점을 얻어옴 // Get a point representing the minimum thickness of the figure
        flpaResultMinPoints1 = CFLPointArray()

        res, flpaResultMinPoints1 = flfSource.GetPointsOfMinimumThickness(flpaResultMinPoints1)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 두께를 측정한 값들에 대해 Trimming 파라미터 적용하여 계산 // Calculated by applying trimming parameters to the measured thickness values
        flpaResultMinPoints2 = CFLPointArray()

        res, flpaResultMinPoints2  = flfSource.GetPointsOfMinimumThickness(flpaResultMinPoints2, 0.01)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 도형의 최대 두께를 나타내는 점을 얻어옴 // Get a point representing the maximum thickness of the figure
        flpaResultMaxPoints1 = CFLPointArray()

        res, flpaResultMaxPoints1 = flfSource.GetPointsOfMaximumThickness(flpaResultMaxPoints1)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 두께를 측정한 값들에 대해 Trimming 파라미터 적용하여 계산 // Calculated by applying trimming parameters to the measured thickness values
        flpaResultMaxPoints2 = CFLPointArray()

        res, flpaResultMaxPoints2 = flfSource.GetPointsOfMaximumThickness(flpaResultMaxPoints2, 0.05)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 도형의 최소 두께를 얻어옴 // Get the minimum thickness of the figure
        f64MinimumThickness1 = flfSource.GetMinimumThickness()

        # 두께를 측정한 값들에 대해 Trimming 파라미터 적용하여 계산 // Calculated by applying trimming parameters to the measured thickness values
        f64MinimumThickness2 = flfSource.GetMinimumThickness(0.01)

        # 도형의 최대 두께를 얻어옴 // Get the minimum thickness of the figure
        f64MaximumThickness1 = flfSource.GetMaximumThickness()

        # 두께를 측정한 값들에 대해 Trimming 파라미터 적용하여 계산 // Calculated by applying trimming parameters to the measured thickness values
        f64MaximumThickness2 = flfSource.GetMaximumThickness(0.05)

        # 각각의 레이어에 Source Figure 그리기 // Draw source figure on each layer
        layerMin0.DrawFigureImage(flfSource, EColor.BLACK, 3)
        layerMin0.DrawFigureImage(flfSource, EColor.LIME)
        layerMin1.DrawFigureImage(flfSource, EColor.BLACK, 3)
        layerMin1.DrawFigureImage(flfSource, EColor.LIME)
        layerMax0.DrawFigureImage(flfSource, EColor.BLACK, 3)
        layerMax0.DrawFigureImage(flfSource, EColor.LIME)
        layerMax1.DrawFigureImage(flfSource, EColor.BLACK, 3)
        layerMax1.DrawFigureImage(flfSource, EColor.LIME)


        # 각각의 레이어에 결과 Point Figure 와 거리값 그리기 // Draw the resulting point figure and distance value on each layer.

        # CFLPoint<double>(flpaResultMinPoints1.GetCenter())와 같이 생성 // Create like CFLPoint<double>(flpaResultMinPoints1.GetCenter())
        flpForDrawMinPoints1 = CFLPoint[Double](flpaResultMinPoints1.GetCenter())
        flpForDrawMinPoints2 = CFLPoint[Double](flpaResultMinPoints2.GetCenter())
        flpForDrawMaxPoints1 = CFLPoint[Double](flpaResultMaxPoints1.GetCenter())
        flpForDrawMaxPoints2 = CFLPoint[Double](flpaResultMaxPoints2.GetCenter())
        flpForDrawMinPoints1.Offset(0, 20)
        flpForDrawMinPoints2.Offset(0, 20)
        flpForDrawMaxPoints1.Offset(0, 20)
        flpForDrawMaxPoints2.Offset(0, 20)

        layerMin0.DrawFigureImage(flpaResultMinPoints1, EColor.BLACK, 3)
        layerMin0.DrawFigureImage(flpaResultMinPoints1, EColor.MAGENTA)
        layerMin0.DrawTextImage(flpForDrawMinPoints1, f"{f64MinimumThickness1:.3f}", EColor.YELLOW, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_TOP)

        layerMin1.DrawFigureImage(flpaResultMinPoints2, EColor.BLACK, 3)
        layerMin1.DrawFigureImage(flpaResultMinPoints2, EColor.MAGENTA)
        layerMin1.DrawTextImage(flpForDrawMinPoints2, f"{f64MinimumThickness2:.3f}", EColor.YELLOW, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_TOP)

        layerMax0.DrawFigureImage(flpaResultMaxPoints1, EColor.BLACK, 3)
        layerMax0.DrawFigureImage(flpaResultMaxPoints1, EColor.CYAN)
        layerMax0.DrawTextImage(flpForDrawMaxPoints1, f"{f64MaximumThickness1:.3f}", EColor.YELLOW, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_TOP)

        layerMax1.DrawFigureImage(flpaResultMaxPoints2, EColor.BLACK, 3)
        layerMax1.DrawFigureImage(flpaResultMaxPoints2, EColor.CYAN)
        layerMax1.DrawTextImage(flpForDrawMaxPoints2, f"{f64MaximumThickness2:.3f}", EColor.YELLOW, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_TOP)

        # Console 출력 // Console output
        print("<Minimum Thickness>\nTrim Ratio : Default\n")
        print(f"Result Thickness : {f64MinimumThickness1}\n")
        print(f"Result Points : {CFigureUtilities.ConvertFigureObjectToString(flpaResultMinPoints1)}\n\n")

        print("<Maximum Thickness>\nTrim Ratio : Default\n")
        print(f"Result Thickness : {f64MaximumThickness1}\n")
        print(f"Result Points : {CFigureUtilities.ConvertFigureObjectToString(flpaResultMaxPoints1)}\n\n")

        print("<Minimum Thickness>\nTrim Ratio : 0.01\n")
        print(f"Result Thickness : {f64MinimumThickness2}\n")
        print(f"Result Points : {CFigureUtilities.ConvertFigureObjectToString(flpaResultMinPoints2)}\n\n")

        print("<Maximum Thickness>\nTrim Ratio : 0.05\n")
        print(f"Result Thickness : {f64MaximumThickness2}\n")
        print(f"Result Points : {CFigureUtilities.ConvertFigureObjectToString(flpaResultMaxPoints2)}\n\n")

        # 이미지 뷰를 갱신 합니다. // Update image view
        for i in range(4):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
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