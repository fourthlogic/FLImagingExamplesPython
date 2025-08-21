# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    # Figure 객체 선언 # Declare figure object
    flfaSource = CFLFigureArray()

    # 이미지 뷰 선언 # Declare the image view
    viewImageCenterFirst = CGUIViewImage()
    viewImageAreaFirst = CGUIViewImage()

    while True:
        # Figure 로드 # Load figure
        if (res := flfaSource.Load("../../ExampleImages/Figure/various shapes2.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # 이미지 뷰 생성 # Create image view
        if (res := viewImageCenterFirst.Create(200, 0, 968, 576)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImageAreaFirst.Create(968, 0, 1736, 576)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        if (res := viewImageCenterFirst.SynchronizePointOfView(viewImageAreaFirst)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
        if (res := viewImageCenterFirst.SynchronizeWindow(viewImageAreaFirst)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 화면상에 잘 보이도록 좌표 1.5배율을 적용 # Apply 1.5 magnification to the coordinates so that they can be seen clearly on the screen
        f64Scale = 1.5
        # 화면상에 잘 보이도록 시점 Offset 조정 # Adjust the viewpoint offset so that it can be seen clearly on the screen
        f64CenterCoordX = 200.0
        f64CenterCoordY = 180.0

        viewImageCenterFirst.SetViewCenterAndScale(CFLPoint[Double](f64CenterCoordX, f64CenterCoordY), f64Scale)

        flfaCenterFirst = CFLFigureArray(flfaSource)
        flfaAreaFirst = CFLFigureArray(flfaSource)

        # FigureArray를 1순위 CenterY 오름차순, 2순위 CenterX 오름차순, 3순위 Area 내림차순으로 정렬
        # Sort FigureArray in ascending order as 1st priority CenterY, ascending order as 2nd priority CenterX, and descending order as 3rd priority Area.
        if (res := flfaCenterFirst.Sort(ESortOrderFigure.CenterY_Asc, ESortOrderFigure.CenterX_Asc, ESortOrderFigure.Area_Desc)).IsFail():
            ErrorPrint(res, "Failed to sort.")
            break

        # FigureArray를 1순위 Area 내림차순, 2순위 CenterY 오름차순, 3순위 CenterX 오름차순으로 정렬
        # Sort FigureArray in descending order as 1st priority Area, ascending order as 2nd priority CenterY, and ascending order as 3rd priority CenterX.
        if (res := flfaAreaFirst.Sort(ESortOrderFigure.Area_Desc, ESortOrderFigure.CenterY_Asc, ESortOrderFigure.CenterX_Asc)).IsFail():
            ErrorPrint(res, "Failed to sort.")
            break

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        layerCenterFirst = viewImageCenterFirst.GetLayer(0)
        layerAreaFirst = viewImageAreaFirst.GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
        layerCenterFirst.Clear()
        layerAreaFirst.Clear()

        flp = CFLPoint[Double]()

        if (res := layerCenterFirst.DrawTextCanvas(flp, ("1st Y, 2nd X, 3rd Area"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text on the image view.")
            break

        if (res := layerAreaFirst.DrawTextCanvas(flp, ("1st Area, 2nd Y, 3rd X"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text on the image view.")
            break

        # FigureArray는 Figure들의 배열이기 때문에 Layer에 넣기만 해도 모두 드로윙이 가능하다.
        # 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며
        # 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다.
        # 여기서 0.25이므로 옅은 반투명 상태라고 볼 수 있다.
        # 파라미터 순서 : 레이어 . Figure 객체 . 선 색 . 선 두께 . 면 색 . 펜 스타일 . 선 알파값(불투명도) . 면 알파값 (불투명도)

        # FigureArray is an array of Figures, so you can draw all of them just by adding them to a Layer.
        # The function DrawFigureImage below means drawing a Figure based on Image coordinates.
        # The last two parameters are opacity values, where 1 means opaque and 0 means completely transparent.
        # Since it's 0.25 here, it can be seen as a light translucent state.
        # Parameter order: layer, Figure object, line color, line thickness, fill color, pen style, line alpha (opacity), fill alpha (opacity)
        if (res := layerCenterFirst.DrawFigureImage(flfaCenterFirst, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1, 0.25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        if (res := layerAreaFirst.DrawFigureImage(flfaAreaFirst, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1, 0.25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        # 정보값을 각각 확인하는 코드 # Code to check each information value
        for i in range(flfaCenterFirst.GetCount()):
            flf = flfaCenterFirst.GetAt(i)

            flpCenter = flf.GetCenter()

            print(f"CenterFirst No. {i} : ({flpCenter.x}, {flpCenter.y}), Area : {flf.GetArea()}")

            layerCenterFirst.DrawTextImage(flpCenter, f"{i}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        print("\n")

        for i in range(flfaAreaFirst.GetCount()):
            flf = flfaAreaFirst.GetAt(i)

            flpCenter = flf.GetCenter()

            print(f"AreaFirst No. {i} : ({flpCenter.x}, {flpCenter.y}), Area : {flf.GetArea()}")

            layerAreaFirst.DrawTextImage(flpCenter, f"{i}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        # 이미지 뷰를 갱신 합니다. # Update image view
        viewImageCenterFirst.RedrawWindow()
        viewImageAreaFirst.RedrawWindow()

        # 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
        while viewImageCenterFirst.IsAvailable() and viewImageAreaFirst.IsAvailable():
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