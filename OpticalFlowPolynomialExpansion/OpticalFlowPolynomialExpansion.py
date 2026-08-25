from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")

def main():
    # 이미지 객체 선언 # Declare the image object
    arrFliImage = [CFLImage() for _ in range(2)]
    # 이미지 뷰 선언 # Declare the image view
    arrViewImage = [CGUIViewImage() for _ in range(2)]

    res = CResult()

    while True:
        # Source 이미지 로드 # Load the source image
        res = arrFliImage[0].Load("../../ExampleImages/OpticalFlowPolynomialExpansion/Highway.flif")
        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
        res = arrFliImage[1].Assign(arrFliImage[0])
        if res.IsFail():
            ErrorPrint(res, "Failed to assign the image file.")
            break

        # OpticalFlowPolynomialExpansion 객체 생성 # Create OpticalFlowPolynomialExpansion object
        opticalFlowPolynomialExpansion = COpticalFlowPolynomialExpansion()
        # Source 이미지 설정 # Set the source image
        opticalFlowPolynomialExpansion.SetSourceImage(arrFliImage[0])
        # Destination 이미지 설정 # Set the destination image
        opticalFlowPolynomialExpansion.SetDestinationImage(arrFliImage[1])
        # Pyramid Level 설정 # Set Pyramid Level
        opticalFlowPolynomialExpansion.SetPyramidLevel(2)
        # Iteration 설정 # Set Iteration
        opticalFlowPolynomialExpansion.SetIteration(3)
        # Window Size 설정 # Set Window Size
        opticalFlowPolynomialExpansion.SetWindowSize(15)
        # Binning Size 설정 # Set Binning Size
        opticalFlowPolynomialExpansion.SetBinningSize(8)
        # Minimum Vector Size 설정 # Set  Minimum Vector Size
        opticalFlowPolynomialExpansion.SetMinimumVectorSize(5.000000)

        print("Processing....")

        # 알고리즘 수행 # Execute algorithm
        res = opticalFlowPolynomialExpansion.Execute()
        if res.IsFail():
            ErrorPrint(res, "Failed to execute OpticalFlow Polynomial Expansion.")
            break

        # 이미지 뷰 생성 # Create image views
        res = arrViewImage[0].Create(400, 0, 1012, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        res = arrViewImage[1].Create(1012, 0, 1624, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지 설정 # Set images to views
        bError = False
        for i in range(2):
            if (res := arrViewImage[i].SetImagePtr(arrFliImage[i]))[0].IsFail():
                ErrorPrint(res[0], "Failed to set image object on the image view.")
                bError = True
                break
        if bError:
            break

        # 이미지 뷰 동기화 # Synchronize windows
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window")
            break

        # 레이어 얻기 및 초기화 # Get layers and clear drawings
        arrLayer = [arrViewImage[i].GetLayer(0) for i in range(2)]
        for layer in arrLayer:
            layer.Clear()

        # 텍스트 위치 # Text position
        tpPosition = TPoint[Single](0, 30)

        # 텍스트 출력 # Draw text on layers
        if (res := arrLayer[0].DrawTextCanvas(tpPosition, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        if (res := arrLayer[1].DrawTextCanvas(tpPosition, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        # 이미지 뷰 갱신 # Invalidate image views
        arrViewImage[0].Invalidate(True)
        arrViewImage[1].Invalidate(True)

        # Auto Clear Mode 비활성화 (페이지 변경 시) # Disable auto clear mode on page change
        arrViewImage[0].SetLayerAutoClearMode(0, ELayerAutoClearMode.PageChanged, False)
        arrViewImage[1].SetLayerAutoClearMode(0, ELayerAutoClearMode.PageChanged, False)
        arrViewImage[0].SetLayerAutoClearMode(1, ELayerAutoClearMode.PageChanged, False)

        # 첫번째 페이지 선택 # Select first page
        arrViewImage[0].MoveToPage(0)
        arrViewImage[1].MoveToPage(0)

        # Layer 1 그리기 수동 모드 설정 # Set layer 1 drawing method to Manual
        arrViewImage[0].GetLayer(1).SetLayerDrawingMethod(ELayerDrawingMethod.Manual)
        
        i32PageIndex = 0
        performanceCounter = CPerformanceCounter()
        flfaResultArrow = CFLFigureArray()
        
        opticalFlowPolynomialExpansion.GetResultMotionVectorsArrowShapeAllScenes(flfaResultArrow)
        performanceCounter.Start()

        # Optical Flow Vector 출력 루프 # Loop to draw optical flow vectors
        while arrViewImage[0].IsAvailable() and arrViewImage[1].IsAvailable():
            if arrFliImage[0].GetPageCount() - 1 == arrFliImage[0].GetSelectedPageIndex():
                arrViewImage[0].MoveToPage(0)
                arrViewImage[1].MoveToPage(0)
                i32PageIndex = 0
                continue
            
            arrViewImage[0].MoveToPage(i32PageIndex)
            arrViewImage[1].MoveToPage(i32PageIndex)
            arrViewImage[0].GetLayer(1).Clear()
            arrViewImage[1].GetLayer(1).DrawFigureImage(flfaResultArrow.GetAt(i32PageIndex), EColor.BLACK, 3)
            arrViewImage[1].GetLayer(1).DrawFigureImage(flfaResultArrow.GetAt(i32PageIndex), EColor.YELLOW, 1)
            arrViewImage[0].GetLayer(1).Update()
            arrViewImage[0].RedrawWindow()
            
            if not arrViewImage[0].IsAvailable() or not arrViewImage[1].IsAvailable():
                break
            
            while performanceCounter.GetElapsedTimeFromStartInMilliSecond() <= 40.0:
                CThreadUtilities.Sleep(1)
                
            performanceCounter.Start()
            i32PageIndex += 1

        arrViewImage[0].Destroy()
        arrViewImage[1].Destroy()

        break


if __name__ == "__main__":
    main()
