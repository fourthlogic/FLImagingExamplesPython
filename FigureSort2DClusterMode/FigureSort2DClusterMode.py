# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():
	
    # Figure 객체 선언 // Declare figure object
    flfaSource = CFLFigureArray()

    # 이미지 뷰 선언 // Declare the image view
    viewImageNormalSort2D = CGUIViewImage()
    viewImageSort2DClusterMode = CGUIViewImage()

    while True:
        # Figure 로드 // Load figure
        if (res := flfaSource.Load("../../ExampleImages/Figure/RectangleArray.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImageNormalSort2D.Create(200, 0, 968, 576)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImageSort2DClusterMode.Create(968, 0, 1736, 576)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        if (res := viewImageNormalSort2D.SynchronizePointOfView(viewImageSort2DClusterMode)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
        if (res := viewImageNormalSort2D.SynchronizeWindow(viewImageSort2DClusterMode)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        flfaNormalSort2D = CFLFigureArray(flfaSource)
        flfaSort2DClusterMode = CFLFigureArray(flfaSource)

        # FigureArray를 일반 Sort 정렬. 1순위 Y오름차순, 2순위 X오름차순
        # Normal Sort sort the FigureArray. 1st rank Y ascending, 2nd rank X ascending
        if (res := flfaNormalSort2D.Sort2D(ESortOrder2D.Y_Asc_X_Asc)).IsFail():
            ErrorPrint(res, "Failed to process normal sort.")
            break

        # FigureArray를 Sort2DClusterMode 정렬. 1순위 Y오름차순, 2순위 X오름차순
        # Sort the FigureArray with Sort2DClusterMode. 1st rank Y ascending, 2nd rank X ascending
        if (res := flfaSort2DClusterMode.Sort2DClusterMode(ESortOrder2D.Y_Asc_X_Asc)).IsFail():
            ErrorPrint(res, "Failed to process Sort2DClusterMode.")
            break

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
        layerNormalSort2D = viewImageNormalSort2D.GetLayer(0)
        layerSort2DClusterMode = viewImageSort2DClusterMode.GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
        layerNormalSort2D.Clear()
        layerSort2DClusterMode.Clear()
        flp = CFLPoint[Double]()

        if (res := layerNormalSort2D.DrawTextCanvas(flp, ("Normal Sort2D (BoundaryRectCenter Y, X)"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text on the image view.")
            break

        if (res := layerSort2DClusterMode.DrawTextCanvas(flp, ("Sort2DClusterMode (Y Asc, X Asc)"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text on the image view.")
            break

        # flfaNormalSort2D 는 Figure들의 배열이기 때문에 Layer에 넣기만 해도 모두 드로윙이 가능하다.
        # 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며
        # 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다.
        # 여기서 0.25이므로 옅은 반투명 상태라고 볼 수 있다.
        # 파라미터 순서 : 레이어 . Figure 객체 . 선 색 . 선 두께 . 면 색 . 펜 스타일 . 선 알파값(불투명도) . 면 알파값 (불투명도)
        if (res := layerNormalSort2D.DrawFigureImage(flfaNormalSort2D, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1, 0.25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        if (res := layerSort2DClusterMode.DrawFigureImage(flfaSort2DClusterMode, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1, 0.25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        # 정보값을 각각 확인하는 코드 // Code to check each information value
        for i in range(flfaNormalSort2D.GetCount()):
            flrg = CFLRegion(flfaNormalSort2D.GetAt(i))

            flpCenter = flrg.GetCenter()

            print(f"NormalSort2D No. {i} : ({flpCenter.x}, {flpCenter.y})")

            layerNormalSort2D.DrawTextImage(flpCenter, f"{i}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        print("\n")

        # 정보값을 각각 확인하는 코드 // Code to check each information value
        for i in range(flfaSort2DClusterMode.GetCount()):
            flfaCluster = CFLFigureArray(flfaSort2DClusterMode.GetAt(i))

            flrBoundary = CFLRect[Double]()

            res, flrBoundary = flfaCluster.GetBoundaryRect(flrBoundary)

            if res.IsFail():
                ErrorPrint(res, "Failed to get boundary rect.")
                break
            
            print(f"Sort2DClusterMode Cluster No. {i}")

            for j in range(flfaCluster.GetCount()):
                flrg = CFLRegion(flfaCluster.GetAt(j))

                flpCenter = flrg.GetCenter()

                print(f"Sort2DClusterMode No. {j} : ({flpCenter.x}, {flpCenter.y})")

                layerSort2DClusterMode.DrawTextImage(flpCenter, f"{i},{j}", EColor.CYAN, EColor.BLACK, 12, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)
        
        # 이전 루프에서 break가 발생했는지 다시 확인 // Check again if a break occurred in the previous loop
        if 'res' in locals() and res.IsFail():
            break

        # 이미지 뷰를 갱신 합니다. // Update image view
        viewImageNormalSort2D.RedrawWindow()
        viewImageSort2DClusterMode.RedrawWindow()

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
        while viewImageNormalSort2D.IsAvailable() and viewImageSort2DClusterMode.IsAvailable():
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