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

        # SourceView, DstView 의 0번 레이어 가져오기 // Get Layer 0 of SourceView, DstView
        Src1Layer0 = viewImage[0].GetLayer(0)
        Dst1Layer0 = viewImage[1].GetLayer(0)
        Src2Layer0 = viewImage[2].GetLayer(0)
        Dst2Layer0 = viewImage[3].GetLayer(0)

        Src1Layer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Figure 1", EColor.YELLOW, EColor.BLACK, 15)
        Src2Layer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Figure 2", EColor.YELLOW, EColor.BLACK, 15)
        Dst1Layer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Result Figure 1", EColor.YELLOW, EColor.BLACK, 15)
        Dst2Layer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Result Figure 2", EColor.YELLOW, EColor.BLACK, 15)

        Dst1Layer0.DrawTextCanvas(CFLPoint[Double](0, 20), "Minimum Distance", EColor.CYAN, EColor.BLACK)
        Dst2Layer0.DrawTextCanvas(CFLPoint[Double](0, 20), "Minimum Distance", EColor.CYAN, EColor.BLACK)

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        if (res := viewImage[2].SynchronizePointOfView(viewImage[3])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
        for i in range(1, 4):
            if (res := viewImage[0].SynchronizeWindow(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize window.")
                break

        if res.IsFail(): # 이전 루프에서 break가 발생했는지 다시 확인 // Check again if a break occurred in the previous loop
            break

        # Figure 생성 // Create figure
        flcSource1 = CFLCircle[Double]()
        flqOperand1 = CFLQuad[Double]()
        flfaSource2 = CFLFigureArray()
        flfaOperand2 = CFLFigureArray()

        # Source Figure 불러오기 // Load source figure
        if (res := flcSource1.Load("../../ExampleImages/Figure/Circle1.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        if (res := flfaSource2.Load("../../ExampleImages/Figure/various shapes_Top.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Operand Figure 불러오기 // Load Operand Figure
        if (res := flqOperand1.Load("../../ExampleImages/Figure/Quad1.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        if (res := flfaOperand2.Load("../../ExampleImages/Figure/various shapes_Bottom.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Figure 사이의 최소 거리를 나타내는 점을 추출 // Get the point representing the minimum distance between figures
        flpaResult1 = CFLPointArray()

        res, flpaResult1 = flcSource1.GetPointsOfMinimumDistance(flqOperand1, flpaResult1)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        flpaResult2 = CFLPointArray()


        res, flpaResult2 = flfaSource2.GetPointsOfMinimumDistance(flfaOperand2, flpaResult2)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # Figure 사이의 최소 거리를 계산 // Calculate the minimum distance between figures
        f64MinimumDistance1 = 0.0

        res, f64MinimumDistance1 = flcSource1.GetMinimumDistance(flqOperand1, f64MinimumDistance1)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break


        f64MinimumDistance2 = 0.0
        
        res, f64MinimumDistance2 = flfaSource2.GetMinimumDistance(flfaOperand2, f64MinimumDistance2)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 두 Point를 잇는 Line을 생성 // Create a line connecting two points
        fllMin1 = CFLLine[Double](flpaResult1.GetAt(0), flpaResult1.GetAt(1))
        fllMin2 = CFLLine[Double](flpaResult2.GetAt(0), flpaResult2.GetAt(1))

        # SourceView1의 0번 레이어에 Source, Operand Figure 그리기 // Draw Source and Operand Figure on Layer 0 of SourceView1
        Src1Layer0.DrawFigureImage(flcSource1, EColor.BLACK, 3)
        Src1Layer0.DrawFigureImage(flcSource1, EColor.KHAKI)
        Src1Layer0.DrawFigureImage(flqOperand1, EColor.BLACK, 3)
        Src1Layer0.DrawFigureImage(flqOperand1, EColor.LIME)

        # DstView1의 0번 레이어에 결과 그리기 // Draw the result on layer 0 of DstView1
        Dst1Layer0.DrawFigureImage(flcSource1, EColor.BLACK, 3)
        Dst1Layer0.DrawFigureImage(flcSource1, EColor.KHAKI)
        Dst1Layer0.DrawFigureImage(flqOperand1, EColor.BLACK, 3)
        Dst1Layer0.DrawFigureImage(flqOperand1, EColor.LIME)
        Dst1Layer0.DrawFigureImage(flpaResult1, EColor.CYAN, 3)
        Dst1Layer0.DrawFigureImage(fllMin1, EColor.CYAN)
        Dst1Layer0.DrawTextImage(fllMin1.GetCenter(), f"{f64MinimumDistance1:.3f}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.RIGHT_TOP)

        # SourceView2의 0번 레이어에 Source, Operand Figure 그리기 // Draw Source and Operand Figure on Layer 0 of SourceView2
        Src2Layer0.DrawFigureImage(flfaSource2, EColor.BLACK, 3)
        Src2Layer0.DrawFigureImage(flfaSource2, EColor.KHAKI)
        Src2Layer0.DrawFigureImage(flfaOperand2, EColor.BLACK, 3)
        Src2Layer0.DrawFigureImage(flfaOperand2, EColor.LIME)

        # DstView2의 0번 레이어에 결과 그리기 // Draw the result on layer 0 of DstView2
        Dst2Layer0.DrawFigureImage(flfaSource2, EColor.BLACK, 3)
        Dst2Layer0.DrawFigureImage(flfaSource2, EColor.KHAKI)
        Dst2Layer0.DrawFigureImage(flfaOperand2, EColor.BLACK, 3)
        Dst2Layer0.DrawFigureImage(flfaOperand2, EColor.LIME)
        Dst2Layer0.DrawFigureImage(flpaResult2, EColor.CYAN, 3)
        Dst2Layer0.DrawFigureImage(fllMin2, EColor.CYAN)
        Dst2Layer0.DrawTextImage(fllMin2.GetCenter(), f"{f64MinimumDistance2:.3f}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.LEFT_BOTTOM)

        # Console 출력 // Console output
        print("Source1 CFLCircle<double>\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flcSource1)}\n\n")

        print("Operand1 CFLQuad<double>\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flqOperand1)}\n\n")

        print("Result1 Points of Minimum distance\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaResult1)}\n\n")

        print("Result1 Minimum distance\n")
        print(f"{f64MinimumDistance1:.3f}\n\n")

        print("\n\n")

        print("Source2 CFLFigureArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaSource2)}\n\n")

        print("Operand2 CFLFigureArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaOperand2)}\n\n")

        print("Result2 Points of Minimum distance\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaResult2)}\n\n")

        print("Result2 Minimum distance\n")
        print(f"{f64MinimumDistance2:.3f}\n\n")

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