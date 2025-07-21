# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():
	
    # 이미지 뷰 선언 // Declare the image object
    viewImage = [CGUIViewImage() for _ in range(4)]

    while True:

        # 이미지 뷰 생성 // Create image view
        res = viewImage[0].Create(400, 0, 912, 384)

        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        res = viewImage[1].Create(912, 0, 1424, 384)

        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        res = viewImage[2].Create(400, 400, 912, 794)

        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        res = viewImage[3].Create(912, 400, 1424, 794)

        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # SourceView, DstView 의 0번 레이어 가져오기 // Get Layer 0 of SourceView, DstView
        SrcLayer0 = viewImage[0].GetLayer(0)
        DstLayer0 = viewImage[1].GetLayer(0)
        SrcLayer1 = viewImage[2].GetLayer(0)
        DstLayer1 = viewImage[3].GetLayer(0)

        # 텍스트 그리기 // Draw text
        SrcLayer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Figure And Region1", EColor.YELLOW, EColor.BLACK, 15)
        DstLayer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Remove Figure Within Region1", EColor.YELLOW, EColor.BLACK, 15)
        SrcLayer1.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Figure And Region2", EColor.YELLOW, EColor.BLACK, 15)
        DstLayer1.DrawTextCanvas(CFLPoint[Double](0, 0), "Remove Figure Within Region2", EColor.YELLOW, EColor.BLACK, 15)

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        for i in range(1, 4):
            resTuple = viewImage[0].SynchronizePointOfView(viewImage[i])

            if resTuple[0].IsFail():
                ErrorPrint(resTuple[0], "Failed to synchronize view")
                break

        if resTuple[0].IsFail():
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
        for i in range(1, 4):
            resTuple = viewImage[0].SynchronizeWindow(viewImage[i])

            if resTuple[0].IsFail():
                ErrorPrint(resTuple[0], "Failed to synchronize window.")
                break

        if resTuple[0].IsFail():
            break

        # Figure 생성 // Create figure
        fll = CFLLine[Double](76, 300, 130, 210)
        flr = CFLRect[Double](50, 50, 100, 100)
        flc = CFLCircle[Double](150.0, 100.0, 30.0, 0.0, 0.0, 80.0, EArcClosingMethod.Center)
        fle = CFLEllipse[Double](300, 150, 100, 50, 0, 180, 60, EArcClosingMethod.EachOther)

        flcr = CFLComplexRegion()
        flcr.PushBack(CFLPoint[Double](270, 100))
        flcr.PushBack(CFLPoint[Double](420, 160))
        flcr.PushBack(CFLPoint[Double](300, 200))

        flfaSource = CFLFigureArray()
        flfaSource.PushBack(fll)
        flfaSource.PushBack(flr)
        flfaSource.PushBack(flc)
        flfaSource.PushBack(fle)
        flfaSource.PushBack(flcr)

        # Region 생성 // Create region
        flcrRegion1 = CFLComplexRegion()
        flcrRegion1.PushBack(CFLPoint[Double](0, 0))
        flcrRegion1.PushBack(CFLPoint[Double](220, 50))
        flcrRegion1.PushBack(CFLPoint[Double](240, 100))
        flcrRegion1.PushBack(CFLPoint[Double](200, 150))
        flcrRegion1.PushBack(CFLPoint[Double](110, 170))
        flcrRegion1.PushBack(CFLPoint[Double](70, 200))

        flcrRegion2 = CFLComplexRegion()
        flcrRegion2.PushBack(CFLPoint[Double](150, 100))
        flcrRegion2.PushBack(CFLPoint[Double](240, 160))
        flcrRegion2.PushBack(CFLPoint[Double](430, 250))
        flcrRegion2.PushBack(CFLPoint[Double](300, 400))
        flcrRegion2.PushBack(CFLPoint[Double](200, 300))
        flcrRegion2.PushBack(CFLPoint[Double](140, 200))
        flcrRegion2.PushBack(CFLPoint[Double](110, 80))

        # Figure 정보 출력 // Print Figure information
        print("Source Figure Array\n")
        strFigure = f"{CFigureUtilities.ConvertFigureObjectToString(flfaSource)}\n\n"
        print(strFigure)

        print("Region1\n")
        strFigure = f"{CFigureUtilities.ConvertFigureObjectToString(flcrRegion1)}\n\n"
        print(strFigure)

        # SourceView1의 0번 레이어에 Source Figure, Region1 그리기 // Draw Source Figure, Region1 on Layer 0 of SourceView1
        SrcLayer0.DrawFigureImage(flfaSource, EColor.CYAN)
        SrcLayer0.DrawFigureImage(flcrRegion1, EColor.BLUE, 1, EColor.BLUE, EGUIViewImagePenStyle.Solid, 1, 0.2)

        print("Region2\n")
        strFigure = f"{CFigureUtilities.ConvertFigureObjectToString(flcrRegion2)}\n\n"
        print(strFigure)

        # SourceView2의 0번 레이어에 Source Figure, Region2 그리기 // Draw Source Figure, Region2 on Layer 0 of SourceView2
        SrcLayer1.DrawFigureImage(flfaSource, EColor.CYAN)
        SrcLayer1.DrawFigureImage(flcrRegion2, EColor.BLUE, 1, EColor.BLUE, EGUIViewImagePenStyle.Solid, 1, 0.2)

        # Region1과 겹쳐지는 Figure 제거 // Remove the overlapping figure with Region1
        flfaResult1 = CFLFigureArray(flfaSource)
        flfaResult1.RemoveFigureWithinRegion(flcrRegion1)

        print("Result Figure Within Region1\n")
        strFigure = f"{CFigureUtilities.ConvertFigureObjectToString(flfaResult1)}\n\n"
        print(strFigure)

        # DstView1의 0번 레이어에 결과 그리기 // Draw the result on layer 0 of DstView1
        DstLayer0.DrawFigureImage(flfaSource, EColor.CYAN)
        DstLayer0.DrawFigureImage(flcrRegion1, EColor.BLUE, 1, EColor.BLUE, EGUIViewImagePenStyle.Solid, 1, 0.2)
        DstLayer0.DrawFigureImage(flfaResult1, EColor.LIME, 3, EColor.LIME, EGUIViewImagePenStyle.Solid, 1, 0.2)

        # Region2과 겹쳐지는 Figure 제거 // Remove figure overlapping with Region2
        flfaResult2 = CFLFigureArray(flfaSource)
        flfaResult2.RemoveFigureWithinRegion(flcrRegion2)

        print("Result Figure Within Region2\n")
        strFigure = f"{CFigureUtilities.ConvertFigureObjectToString(flfaResult2)}\n\n"
        print(strFigure)

        # DstView1의 0번 레이어에 결과 그리기 // Draw the result on layer 0 of DstView1
        DstLayer1.DrawFigureImage(flfaSource, EColor.CYAN)
        DstLayer1.DrawFigureImage(flcrRegion2, EColor.BLUE, 1, EColor.BLUE, EGUIViewImagePenStyle.Solid, 1, 0.2)
        DstLayer1.DrawFigureImage(flfaResult2, EColor.LIME, 3, EColor.LIME, EGUIViewImagePenStyle.Solid, 1, 0.2)

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