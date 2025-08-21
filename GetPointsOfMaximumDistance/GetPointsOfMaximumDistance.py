# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    # 이미지 뷰 선언 # Declare the image view
    viewImage = [CGUIViewImage() for _ in range(4)]

    while True:

        # 이미지 뷰 생성 # Create image view
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

        # SourceView, DstView 의 0번 레이어 가져오기 # Get Layer 0 of SourceView, DstView
        layerSrc1 = viewImage[0].GetLayer(0)
        layerDst1 = viewImage[1].GetLayer(0)
        layerSrc2 = viewImage[2].GetLayer(0)
        layerDst2 = viewImage[3].GetLayer(0)

        layerSrc1.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Figure 1", EColor.YELLOW, EColor.BLACK, 15)
        layerSrc2.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Figure 2", EColor.YELLOW, EColor.BLACK, 15)
        layerDst1.DrawTextCanvas(CFLPoint[Double](0, 0), "Result Figure 1", EColor.YELLOW, EColor.BLACK, 15)
        layerDst2.DrawTextCanvas(CFLPoint[Double](0, 0), "Result Figure 2", EColor.YELLOW, EColor.BLACK, 15)

        layerDst1.DrawTextCanvas(CFLPoint[Double](0, 20), "Maximum Distance", EColor.CYAN, EColor.BLACK)
        layerDst2.DrawTextCanvas(CFLPoint[Double](0, 20), "Maximum Distance", EColor.CYAN, EColor.BLACK)

        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        if (res := viewImage[2].SynchronizePointOfView(viewImage[3])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
        for i in range(1, 4):
            if (res := viewImage[0].SynchronizeWindow(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize window.")
                break

        if res.IsFail():
            break

        # Figure 생성 # Create figure
        flcSource1 = CFLCircle[Double]()
        flqOperand1 = CFLQuad[Double]()
        flfaSource2 = CFLFigureArray()
        flfaOperand2 = CFLFigureArray()

        # Source Figure 불러오기 # Load source figure
        if (res := flcSource1.Load("../../ExampleImages/Figure/Circle1.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        if (res := flfaSource2.Load("../../ExampleImages/Figure/various shapes_Top.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Operand Figure 불러오기 # Load Operand Figure
        if (res := flqOperand1.Load("../../ExampleImages/Figure/Quad1.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        if (res := flfaOperand2.Load("../../ExampleImages/Figure/various shapes_Bottom.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Figure 사이의 최대 거리를 나타내는 점을 추출 # Get the point representing the maximum distance between figures
        flpaResult1 = CFLPointArray()

        res, flpaResult1 = flcSource1.GetPointsOfMaximumDistance(flqOperand1, flpaResult1)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break


        flpaResult2 = CFLPointArray()
        
        res, flpaResult2 = flfaSource2.GetPointsOfMaximumDistance(flfaOperand2, flpaResult2)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # Figure 사이의 최대 거리를 계산 # Calculate the maximum distance between figures
        f64MaximumDistance1 = 0.0

        res, f64MaximumDistance1 = flcSource1.GetMaximumDistance(flqOperand1, f64MaximumDistance1)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break


        f64MaximumDistance2 = 0.0
        
        res, f64MaximumDistance2 = flfaSource2.GetMaximumDistance(flfaOperand2, f64MaximumDistance2)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 두 Point를 잇는 Line을 생성 # Create a line connecting two points
        fllMax1 = CFLLine[Double](flpaResult1.GetAt(0), flpaResult1.GetAt(1))
        fllMax2 = CFLLine[Double](flpaResult2.GetAt(0), flpaResult2.GetAt(1))

        # SourceView1의 0번 레이어에 Source, Operand Figure 그리기 # Draw Source and Operand Figure on Layer 0 of SourceView1
        layerSrc1.DrawFigureImage(flcSource1, EColor.BLACK, 3)
        layerSrc1.DrawFigureImage(flcSource1, EColor.KHAKI)
        layerSrc1.DrawFigureImage(flqOperand1, EColor.BLACK, 3)
        layerSrc1.DrawFigureImage(flqOperand1, EColor.LIME)

        # DstView1의 0번 레이어에 결과 그리기 # Draw the result on layer 0 of DstView1
        layerDst1.DrawFigureImage(flcSource1, EColor.BLACK, 3)
        layerDst1.DrawFigureImage(flcSource1, EColor.KHAKI)
        layerDst1.DrawFigureImage(flqOperand1, EColor.BLACK, 3)
        layerDst1.DrawFigureImage(flqOperand1, EColor.LIME)
        layerDst1.DrawFigureImage(flpaResult1, EColor.CYAN, 3)
        layerDst1.DrawFigureImage(fllMax1, EColor.CYAN)
        layerDst1.DrawTextImage(fllMax1.GetCenter(), f"{f64MaximumDistance1:.3f}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.RIGHT_TOP)

        # SourceView2의 0번 레이어에 Source, Operand Figure 그리기 # Draw Source and Operand Figure on Layer 0 of SourceView2
        layerSrc2.DrawFigureImage(flfaSource2, EColor.BLACK, 3)
        layerSrc2.DrawFigureImage(flfaSource2, EColor.KHAKI)
        layerSrc2.DrawFigureImage(flfaOperand2, EColor.BLACK, 3)
        layerSrc2.DrawFigureImage(flfaOperand2, EColor.LIME)

        # DstView2의 0번 레이어에 결과 그리기 # Draw the result on layer 0 of DstView2
        layerDst2.DrawFigureImage(flfaSource2, EColor.BLACK, 3)
        layerDst2.DrawFigureImage(flfaSource2, EColor.KHAKI)
        layerDst2.DrawFigureImage(flfaOperand2, EColor.BLACK, 3)
        layerDst2.DrawFigureImage(flfaOperand2, EColor.LIME)
        layerDst2.DrawFigureImage(flpaResult2, EColor.CYAN, 3)
        layerDst2.DrawFigureImage(fllMax2, EColor.CYAN)
        layerDst2.DrawTextImage(fllMax2.GetCenter(), f"{f64MaximumDistance2:.3f}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.LEFT_BOTTOM)

        # Console 출력 # Console output
        print("Source1 CFLCircle<double>\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flcSource1)}\n\n")

        print("Operand1 CFLQuad<double>\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flqOperand1)}\n\n")

        print("Result1 Points of Maximum distance\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaResult1)}\n\n")

        print("Result1 Maximum distance\n")
        print(f"{f64MaximumDistance1:.3f}\n\n")

        print("\n\n")

        print("Source2 CFLFigureArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaSource2)}\n\n")

        print("Operand2 CFLFigureArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaOperand2)}\n\n")

        print("Result2 Points of Maximum distance\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaResult2)}\n\n")

        print("Result2 Maximum distance\n")
        print(f"{f64MaximumDistance2:.3f}\n\n")

        # 이미지 뷰를 갱신 합니다. # Update image view
        for i in range(4):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
        while all(view.IsAvailable() for view in viewImage):
            CThreadUtilities.Sleep(1)

        break
    
    # End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()