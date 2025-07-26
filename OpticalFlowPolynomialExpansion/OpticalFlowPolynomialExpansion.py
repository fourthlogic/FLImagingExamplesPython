from FLImagingClrPy import *

def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")

def main():
    # 이미지 객체 선언 // Declare the image object
    arrFliImage = [CFLImage() for _ in range(2)]
    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for _ in range(2)]

    res = CResult()

    while True:
        # Source 이미지 로드 // Load the source image
        res = arrFliImage[0].Load("../../ExampleImages/OpticalFlowPolynomialExpansion/Highway.flif")
        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
        res = arrFliImage[1].Assign(arrFliImage[0])
        if res.IsFail():
            ErrorPrint(res, "Failed to assign the image file.")
            break

        # OpticalFlowPolynomialExpansion 객체 생성 // Create OpticalFlowPolynomialExpansion object
        opticalFlow = COpticalFlowPolynomialExpansion()
        opticalFlow.SetSourceImage(arrFliImage[0])
        opticalFlow.SetDestinationImage(arrFliImage[1])
        opticalFlow.SetPyramidLevel(2)
        opticalFlow.SetIteration(3)
        opticalFlow.SetWindowSize(15)

        print("Processing....")

        # 알고리즘 수행 // Execute algorithm
        res = opticalFlow.Execute()
        if res.IsFail():
            ErrorPrint(res, "Failed to execute OpticalFlow Polynomial Expansion.")
            break

        # 이미지 뷰 생성 // Create image views
        res = arrViewImage[0].Create(400, 0, 1012, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        res = arrViewImage[1].Create(1012, 0, 1624, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지 설정 // Set images to views
        bError = False
        for i in range(2):
            if (res := arrViewImage[i].SetImagePtr(arrFliImage[i]))[0].IsFail():
                ErrorPrint(res[0], "Failed to set image object on the image view.")
                bError = True
                break
        if bError:
            break

        # 이미지 뷰 동기화 // Synchronize viewpoints, pages, and windows
        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break
        if (res := arrViewImage[0].SynchronizePageIndex(arrViewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window")
            break

        # 레이어 얻기 및 초기화 // Get layers and clear drawings
        arrLayer = [arrViewImage[i].GetLayer(0) for i in range(2)]
        for layer in arrLayer:
            layer.Clear()

        # 텍스트 위치 // Text position
        tpPosition = TPoint[Single](0, 30)

        # 텍스트 출력 // Draw text on layers
        if (res := arrLayer[0].DrawTextCanvas(tpPosition, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        if (res := arrLayer[1].DrawTextCanvas(tpPosition, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        # 이미지 뷰 갱신 // Invalidate image views
        arrViewImage[0].Invalidate(True)
        arrViewImage[1].Invalidate(True)

        # Optical Flow 벡터 출력 준비 변수 선언 // Prepare variables for optical flow vector drawing
        m_flpStart = CFLPoint[Single]()
        m_flpEnd = CFLPoint[Single]()
        m_fllDisplay = CFLLine[Single]()

        # Optical Flow Vector 크기 최소값 설정 // Minimum vector length to display
        f64MinVectorSize = 1.0

        i32FlowWidth = int(arrFliImage[0].GetWidth())
        i32FlowHeight = int(arrFliImage[0].GetHeight())

        # Optical Flow Vector 간격 설정 // Vector grid step
        i32GridStep = i32FlowWidth // 50 if i32FlowWidth > i32FlowHeight else i32FlowHeight // 50

        # Auto Clear Mode 비활성화 (페이지 변경 시) // Disable auto clear mode on page change
        arrViewImage[0].SetLayerAutoClearMode(0, ELayerAutoClearMode.PageChanged, False)
        arrViewImage[1].SetLayerAutoClearMode(0, ELayerAutoClearMode.PageChanged, False)
        arrViewImage[0].SetLayerAutoClearMode(1, ELayerAutoClearMode.PageChanged, False)

        # 첫번째 페이지 선택 // Select first page
        arrViewImage[0].MoveToPage(0)
        arrViewImage[1].MoveToPage(0)

        # Layer 1 그리기 수동 모드 설정 // Set layer 1 drawing method to Manual
        arrViewImage[0].GetLayer(1).SetLayerDrawingMethod(ELayerDrawingMethod.Manual)

        flfaArrow1 = CFLFigureArray()
        flfaArrow2 = CFLFigureArray()

        # Optical Flow Vector 출력 루프 // Loop to draw optical flow vectors
        while arrViewImage[0].IsAvailable() and arrViewImage[1].IsAvailable():
            if arrFliImage[0].GetPageCount() - 1 == arrFliImage[0].GetSelectedPageIndex():
                arrViewImage[0].MoveToPage(0)
                arrViewImage[1].MoveToPage(0)
                continue

            arrViewImage[0].GetLayer(1).Clear()
            flfaArrow1.Clear()
            flfaArrow2.Clear()

            # Destination 이미지 버퍼 얻기 // Get destination image buffer for pixel access
            dstImgBuffer = List[Single]()
            arrFliImage[1].GetBuffer(dstImgBuffer)

            for i32Width in range(0, i32FlowWidth, i32GridStep):
                for i32Height in range(0, i32FlowHeight, i32GridStep):
                    m_flpStart.x = i32Width
                    m_flpStart.y = i32Height

                    index = i32Height * i32FlowWidth * 2 + i32Width * 2
                    m_flpEnd.x = i32Width + dstImgBuffer[index]
                    m_flpEnd.y = i32Height + dstImgBuffer[index + 1]

                    #flfaArrow.PushBack(CFLLine[Double](m_flpStart, m_flpEnd))
                    # Line 객체에 시작점, 끝점 설정 // Set start and end points of line
                    #m_fllDisplay.Set(m_flpStart.x, m_flpEnd.y)
                    m_fllDisplay.flpPoints[0].x = m_flpStart.x
                    m_fllDisplay.flpPoints[0].y = m_flpStart.y
                    m_fllDisplay.flpPoints[1].x = m_flpEnd.x
                    m_fllDisplay.flpPoints[1].y = m_flpEnd.y

                    # 벡터 길이가 최소값 이상인 경우 그리기 // Draw arrow if vector length is greater than minimum
                    if m_fllDisplay.GetLength() > f64MinVectorSize:
                        flfaArrow1.PushBack(m_fllDisplay.MakeArrowWithRatio(0.4, True, 30))
                        flfaArrow2.PushBack(m_fllDisplay.MakeArrowWithRatio(0.4, True, 30))

            arrViewImage[0].GetLayer(1).DrawFigureImage(flfaArrow1, EColor.BLACK, 3)
            arrViewImage[0].GetLayer(1).DrawFigureImage(flfaArrow2, EColor.YELLOW, 1)

            if not arrViewImage[0].IsAvailable() or not arrViewImage[1].IsAvailable():
                break

            arrViewImage[0].MoveToNextPage()
            arrViewImage[1].MoveToNextPage()
            arrViewImage[0].GetLayer(1).Update()
            arrViewImage[0].RedrawWindow()

        break

if __name__ == "__main__":
    main()