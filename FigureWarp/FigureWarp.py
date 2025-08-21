# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    # 이미지 뷰 선언 # Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage()]

    while True:
        # Source Figures View 생성 # Create the Source Figures View
        if (res := viewImage[0].Create(200, 0, 700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Warp Result View 생성 # Create the Warp Result View^
        if (res := viewImage[1].Create(700, 0, 1200, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 각 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoint of each image view.
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 각 이미지 뷰 윈도우의 위치를 동기화 한다. # Synchronize the position of each image view window.
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 화면상에 잘 보이도록 좌표 0.5배율을 적용 # Apply 0.5 magnification to the coordinates so that they can be seen clearly on the screen
        f64Scale = 0.5
        # 화면상에 잘 보이도록 시점 Offset 조정 # Adjust the viewpoint offset so that it can be seen clearly on the screen
        f64CenterCoordX = 737.5
        f64CenterCoordY = 524.5
        viewImage[0].SetViewCenterAndScale(CFLPoint[Double](f64CenterCoordX, f64CenterCoordY), f64Scale)

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        layer = [viewImage[0].GetLayer(0), viewImage[1].GetLayer(0)]

        # 화면상 좌표(고정 좌표)에 Source Figure View 임을 표시 # Displays Source Figure View in on-screen coordinates (fixed coordinates)
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 0), "Source Figures", EColor.YELLOW, EColor.BLACK, 30)
        # 화면상 좌표(고정 좌표)에 Warp Result View 임을 표시 # Display of Warp Result View in on-screen coordinates (fixed coordinates)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 0), "Warp Result", EColor.YELLOW, EColor.BLACK, 30)

        # Warp을 동작하기 위한 Source Figure들이 담긴 FigureArray를 로드합니다. (다른 Figure들도 동작 가능합니다.)
        # Loads a FigureArray containing the source figures for running the warp. (Other figures are also available.)
        flfaSource = CFLFigureArray()

        # Source Figure 불러오기 # Load Source Figure
        if (res := flfaSource.Load("../../ExampleImages/Figure/DistortedCoordinates.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break


        # Source Figure의 각 꼭지점을 SourceRegion Quad로 생성
        # Each vertex of the source figure is created as a SourceRegion Quad
        flqSourceRegion = CFLQuad[Double](CFLPoint[Double](397.5, 227.0), CFLPoint[Double](1065.0, 292.0), CFLPoint[Double](1063.5, 739.5), CFLPoint[Double](395.0, 822.5))
        # SourceRegion Quad를 직사각형의 형태로 펼친 Quad로 TargetRegion Quad를 생성
        # Create a TargetRegion Quad with a Quad that spreads the SourceRegion Quad in the form of a rectangle
        flqTargetRegion = CFLQuad[Double](CFLPoint[Double](397.5, 227.0), CFLPoint[Double](1065.0, 227.0), CFLPoint[Double](1065.5, 822.5), CFLPoint[Double](397.5, 822.5))

        print(f"Source Quad Region : {CFigureUtilities.ConvertFigureObjectToString(flqSourceRegion)}")
        print(f"Target Quad Region : {CFigureUtilities.ConvertFigureObjectToString(flqTargetRegion)}\n")

        # Warp 결과를 받아올 FigureArray # FigureArray to receive the warp result
        flfaResult = CFLFigureArray()

        # Perspective Type으로 Warp 함수 동작 (Perspective, Bilinear 두 타입으로 함수 동작 가능)
        # Warp function works with perspective type (function can be operated with two types, perspective and bilinear)
        res, flfaResult = flfaSource.Warp(flqSourceRegion, flqTargetRegion, flfaResult, EWarpingType.Perspective)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # Source Figure 그리기 # Draw the Source Figure
        if (res := layer[0].DrawFigureImage(flfaSource, EColor.YELLOW, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        # Warp Result Figure 그리기 # Draw Warp Result Figure
        if (res := layer[1].DrawFigureImage(flfaResult, EColor.LIME, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        # SourceRegion Quad 그리기 # Draw SourceRegion Quad
        if (res := layer[0].DrawFigureImage(flqSourceRegion, EColor.RED, 1)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        # TargetRegion Quad 그리기 # Draw TargetRegion Quad
        if (res := layer[1].DrawFigureImage(flqTargetRegion, EColor.BLUE, 1)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.")
            break

        # Source와 Warp Result Point를 Console 창에 출력 # Output the Source and Warp Result Point to the console window
        for i in range(flfaSource.GetCount()):
            flpSource = CFLPoint[Double](flfaSource.GetAt(i))
            flpTarget = CFLPoint[Double](flfaResult.GetAt(i))

            print(f"Source ({flpSource.x:.1f}, {flpSource.y:.1f}) -> Warp Result ({flpTarget.x:.1f}, {flpTarget.y:.1f})")

        # 이미지 뷰들을 갱신 합니다. # Update the image views.
        for i in range(2):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 둘중에 하나라도 꺼지면 종료로 간주 # If either one of the imageviews is turned off, it is considered to be closed.
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