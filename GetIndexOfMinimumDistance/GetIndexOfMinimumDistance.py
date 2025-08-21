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

        layerDst1.DrawTextCanvas(CFLPoint[Double](0, 20), "Index of Minimum Distance", EColor.CYAN, EColor.BLACK)
        layerDst2.DrawTextCanvas(CFLPoint[Double](0, 20), "Index of Minimum Distance", EColor.CYAN, EColor.BLACK)

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

        if (res := viewImage[0].SynchronizeWindow(viewImage[3])[0]).IsFail():
            break

        # Figure 생성 # Create figure
        flpaSource1 = CFLPointArray()
        flcDestination1 = CFLCircle[Double]()
        flfaSource2 = CFLFigureArray()
        flfaDestination2 = CFLFigureArray()

        # Source Figure 불러오기 # Load Source figure
        if (res := flpaSource1.Load("../../ExampleImages/Figure/PointArray1.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        if (res := flfaSource2.Load("../../ExampleImages/Figure/various_arrays.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Destination Figure 불러오기 # Load Destination Figure
        if (res := flcDestination1.Load("../../ExampleImages/Figure/Circle2.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        if (res := flfaDestination2.Load("../../ExampleImages/Figure/Circles2.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Figure 사이의 최소 거리를 나타내는 인덱스를 추출 # Get the index of representing the minimum distance between figures
        flfaResultSrc1 = CFLFigureArray()

        res, flfaResultSrc1 = flpaSource1.GetIndexOfMinimumDistance(flcDestination1, flfaResultSrc1)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        flfaResultSrc2 = CFLFigureArray()
        flfaResultDst2 = CFLFigureArray()

        # refVal는 (변경된 flfaResultSrc2, 변경된 flfaResultDst2) 튜플을 반환 # refVal returns a (modified flfaResultSrc2, modified flfaResultDst2) tuple
        res, *refVal = flfaSource2.GetIndexOfMinimumDistance(flfaDestination2, flfaResultSrc2, True, True, flfaResultDst2)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        flfaResultSrc2 = refVal[0] # ref 파라미터 결과 할당 # Assign ref parameter result
        flfaResultDst2 = refVal[1] # 두 번째 ref 파라미터 결과 할당 # Assign second ref parameter result


        # SourceView1의 0번 레이어에 Source, Destination Figure 그리기 # Draw Source and Destination Figure on Layer 0 of SourceView1
        layerSrc1.DrawFigureImage(flpaSource1, EColor.BLACK, 3)
        layerSrc1.DrawFigureImage(flpaSource1, EColor.LIME)
        layerSrc1.DrawFigureImage(flcDestination1, EColor.BLACK, 3)
        layerSrc1.DrawFigureImage(flcDestination1, EColor.KHAKI)

        for i in range(flpaSource1.GetCount()):
            layerSrc1.DrawTextImage(flpaSource1.GetAt(i).GetCenter(), f"{i}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_BOTTOM)

        # DstView1의 0번 레이어에 결과 그리기 # Draw the result on layer 0 of DstView1
        # C#의 (CFLScalar<long>)flfaResultSrc1.Front()와 유사 # Similar to C#'s (CFLScalar<long>)flfaResultSrc1.Front()
        flvSrc = CFLScalar[Int64](flfaResultSrc1.Front()) 
        layerDst1.DrawFigureImage(flpaSource1, EColor.BLACK, 3)
        layerDst1.DrawFigureImage(flpaSource1, EColor.LIME)
        layerDst1.DrawFigureImage(flcDestination1, EColor.BLACK, 3)
        layerDst1.DrawFigureImage(flcDestination1, EColor.KHAKI)
        layerDst1.DrawFigureImage(flpaSource1.GetAt(flvSrc.v), EColor.CYAN, 3)
        layerDst1.DrawTextImage(flpaSource1.GetAt(flvSrc.v).GetCenter(), f"{flvSrc.v}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_BOTTOM)
        layerDst1.DrawTextImage(flcDestination1.GetCenter(), f"{flvSrc.v}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        # SourceView2의 0번 레이어에 Source, Destination Figure 그리기 # Draw Source and Destination Figure on Layer 0 of SourceView2
        layerSrc2.DrawFigureImage(flfaSource2, EColor.BLACK, 3)
        layerSrc2.DrawFigureImage(flfaSource2, EColor.LIME)
        layerSrc2.DrawFigureImage(flfaDestination2, EColor.BLACK, 3)
        layerSrc2.DrawFigureImage(flfaDestination2, EColor.KHAKI)

        for i in range(flfaSource2.GetCount()):
            flfaArrayDepth1 = CFLFigureArray(flfaSource2.GetAt(i))
            flrBoundary = CFLRect[Double]()
            
            res, flrBoundary = flfaArrayDepth1.GetBoundaryRect(flrBoundary)
            
            if res.IsFail():
                ErrorPrint(res, "Failed to get boundary rect.")
                break

            layerSrc2.DrawFigureImage(flrBoundary, EColor.LIGHTBLUE, 1)
            layerSrc2.DrawTextImage(flfaArrayDepth1.GetCenter(), f"{i}", EColor.LIGHTBLUE, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

            for j in range(flfaArrayDepth1.GetCount()):
                layerSrc2.DrawTextImage(flfaArrayDepth1.GetAt(j).GetCenter(), f"{j}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)
        
        # 이전 루프에서 break가 발생했는지 다시 확인 # Check again if a break occurred in the previous loop
        if 'res' in locals() and res.IsFail():
            break

        for i in range(flfaDestination2.GetCount()):
            layerSrc2.DrawTextImage(flfaDestination2.GetAt(i).GetCenter(), f"{i}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        # DstView2의 0번 레이어에 결과 그리기 # Draw the result on layer 0 of DstView2
        layerDst2.DrawFigureImage(flfaSource2, EColor.BLACK, 3)
        layerDst2.DrawFigureImage(flfaSource2, EColor.LIME)
        layerDst2.DrawFigureImage(flfaDestination2, EColor.BLACK, 3)
        layerDst2.DrawFigureImage(flfaDestination2, EColor.KHAKI)

        # C#의 (CFLScalar<long>)flfaResultSrc2.GetAt(0)와 유사 # Similar to C#'s (CFLScalar<long>)flfaResultSrc2.GetAt(0)
        flvSrcDepth1 = CFLScalar[Int64](flfaResultSrc2.GetAt(0))
        flvSrcDepth2 = CFLScalar[Int64](flfaResultSrc2.GetAt(1))

        # C#의 (CFLFigureArray)flfaSource2.GetAt(flvSrcDepth1.v)와 유사 # Similar to C#'s (CFLFigureArray)flfaSource2.GetAt(flvSrcDepth1.v)
        flfaSrcDepth1 = CFLFigureArray(flfaSource2.GetAt(flvSrcDepth1.v))
        flfSrcDepth1 = flfaSource2.GetAt(flvSrcDepth1.v)
        # C#의 ((CFLFigureArray)flfSrcDepth1).GetAt(flvSrcDepth2.v)와 유사 # Similar to C#'s ((CFLFigureArray)flfSrcDepth1).GetAt(flvSrcDepth2.v)
        flfSrcDepth2 = CFLFigureArray(flfSrcDepth1).GetAt(flvSrcDepth2.v)

        flfaArraySrcDepth1 = CFLFigureArray(flfaSource2.GetAt(flvSrcDepth1.v))
        flrBoundary2 = CFLRect[Double]()
        
        res, flrBoundary2 = flfaArraySrcDepth1.GetBoundaryRect(flrBoundary2)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to get boundary rect for flrBoundary2.")
            break


        layerDst2.DrawFigureImage(flrBoundary2, EColor.LIGHTORANGE, 1)
        layerDst2.DrawTextImage(flfaArraySrcDepth1.GetCenter(), f"{flvSrcDepth1.v}", EColor.LIGHTORANGE, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        layerDst2.DrawTextImage(flfaArraySrcDepth1.GetAt(flvSrcDepth2.v).GetCenter(), f"{flvSrcDepth2.v}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)
        layerDst2.DrawFigureImage(flfSrcDepth2, EColor.CYAN, 1)

        flvDstDepth1 = CFLScalar[Int64](flfaResultDst2.GetAt(0))

        flfDstDepth1 = flfaDestination2.GetAt(flvDstDepth1.v)

        layerDst2.DrawTextImage(flfDstDepth1.GetCenter(), f"{flvDstDepth1.v}", EColor.MAGENTA, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)
        layerDst2.DrawFigureImage(flfDstDepth1, EColor.MAGENTA, 1)


        # Console 출력 # Console output
        print("Source1 CFLPointArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flpaSource1)}\n\n")

        print("Destination1 CFLCircle<double>\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flcDestination1)}\n\n")

        print("Result1 Index of Minimum distance\n")
        print(f"{flvSrc.v}\n\n")

        print("\n\n")

        print("Source2 CFLFigureArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaSource2)}\n\n")

        print("Destination2 CFLFigureArray\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaDestination2)}\n\n")

        print("Src Result2 Index of Minimum distance\n")
        print(f"Depth1 : {flvSrcDepth1.v}\nDepth2 : {flvSrcDepth2.v}\n\n")

        print("Dst Result2 Index of Minimum distance\n")
        print(f"Depth1 : {flvDstDepth1.v}\n\n")

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