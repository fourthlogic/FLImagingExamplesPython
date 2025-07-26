# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():
	
    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage()]

    while True:
        # 이미지 뷰 생성 // Create image view
        if (res := viewImage[0].Create(400, 0, 912, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(912, 0, 1424, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # SourceView, DstView 의 0번 레이어 가져오기 // Get Layer 0 of SourceView, DstView
        SrcLayer0 = viewImage[0].GetLayer(0)
        DstLayer0 = viewImage[1].GetLayer(0)

        SrcLayer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Figure To Save", EColor.YELLOW, EColor.BLACK, 15)
        DstLayer0.DrawTextCanvas(CFLPoint[Double](0, 0), "Loaded Figure", EColor.YELLOW, EColor.BLACK, 15)

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        ######## Save
        # Figure 생성 // Create figure
        flr = CFLRect[Double](50, 50, 100, 100)

        flc = CFLCircle[Double](150.0, 100.0, 30.0, 0.0, 0.0, 80.0, EArcClosingMethod.Center)

        fle = CFLEllipse[Double](300, 150, 100, 50, 0, 180, 60, EArcClosingMethod.EachOther)

        flfa = CFLFigureArray()

        flfa.PushBack(flc)
        flfa.PushBack(fle)

        print("Figure To Save\n")

        strFigure = f"Rect : {CFigureUtilities.ConvertFigureObjectToString(flr)}\n"
        print(f"{strFigure}")

        strFigure = f"Figure Array : {CFigureUtilities.ConvertFigureObjectToString(flfa)}\n\n"
        print(f"{strFigure}")

        # SourceView의 0번 레이어에 그리기 // Draw on Layer 0 of SourceView
        SrcLayer0.DrawFigureImage(flr, EColor.RED)
        SrcLayer0.DrawFigureImage(flfa, EColor.BLUE)

        # 경로 없이 파일명만 넣고 저장하는 것도 가능 // It is also possible to put only the file name without path and save it
        if (res := flr.Save("FLRect.fig")).IsFail():
            ErrorPrint(res, "Failed to save FLRect.fig.")
            break

        # 확장자명 없이 저장하는 것도 가능 // It is also possible to save without an extension name
        if (res := flfa.Save("FigureArray")).IsFail():
            ErrorPrint(res, "Failed to save FigureArray.")
            break

        ######## Load
        # 다른 DeclType 인 파일을 Load할 경우 반환값이 EResult_OK 가 아닌 다른 반환값을 반환
        # When loading a file with a different DeclType, return value other than EResult_OK is returned
        flrLoad = CFLRect[Double]()

        # Rect 에 FigureArray 로드했으므로 실패 // Failed because we loaded FigureArray into Rect
        res = flrLoad.Load("FigureArray")
        # print(f"Attempting to load FigureArray into CFLRect. Result: {res.GetString()}") # 디버깅용 // For debugging

        # Rect 에 Rect 파일을 로드했으므로 파일을 로드했으므로 성공 EResult_OK 반환
        # Loaded the Rect file into Rect, so we loaded the file, so return EResult_OK
        res = flrLoad.Load("FLRect")
        # print(f"Attempting to load FLRect into CFLRect. Result: {res.GetString()}") # 디버깅용 // For debugging

        # 다른 DeclType 인 파일을 Load할 경우 반환값이 EResult_OK 가 아닌 다른 반환값을 반환
        # When loading a file with a different DeclType, return value other than EResult_OK is returned
        flfaLoad = CFLFigureArray()

        # FigureArray 에 Rect 파일을 로드했으므로 실패 // Failed because Rect file was loaded into FigureArray
        res = flfaLoad.Load("FLRect")
        # print(f"Attempting to load FLRect into CFLFigureArray. Result: {res.GetString()}") # 디버깅용 // For debugging

        # FigureArray 에 FigureArray 파일을 로드했으므로 성공 EResult_OK 반환
        # Success returned EResult_OK because FigureArray file was loaded into FigureArray
        res = flfaLoad.Load("FigureArray")
        # print(f"Attempting to load FigureArray into CFLFigureArray. Result: {res.GetString()}") # 디버깅용 // For debugging

        print("Loaded Figure\n")

        strFigure = f"Rect : {CFigureUtilities.ConvertFigureObjectToString(flrLoad)}\n"
        print(f"{strFigure}")

        strFigure = f"Figure Array : {CFigureUtilities.ConvertFigureObjectToString(flfaLoad)}\n\n"
        print(f"{strFigure}")

        # DestinationView의 0번 레이어에 그리기 // Draw on Layer 0 of DestinationView
        DstLayer0.DrawFigureImage(flrLoad, EColor.MAGENTA)
        DstLayer0.DrawFigureImage(flfaLoad, EColor.LIME)

        # 이미지 뷰를 갱신 합니다. // Update image view
        viewImage[0].Invalidate(True)
        viewImage[1].Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
        while viewImage[0].IsAvailable() or viewImage[1].IsAvailable():
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