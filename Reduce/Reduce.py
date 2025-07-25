# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage() for _ in range(3)] # C#의 배열 초기화와 유사

    while True:

        # Source View 생성 // Create Source View
        if (res := viewImage[0].Create(200, 0, 700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Reduce result1 View 생성 // Create Reduce result1 view
        if (res := viewImage[1].Create(700, 0, 1200, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Reduce result2 View 생성 // Create Reduce result2 view
        if (res := viewImage[2].Create(1200, 0, 1700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 각 이미지 뷰의 시점을 동기화 한다. // Synchronize the viewpoint of each image view.
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        if (res := viewImage[1].SynchronizePointOfView(viewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 각 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the position of each image view window
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        if (res := viewImage[1].SynchronizeWindow(viewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 화면에 출력하기 위해 Image View 에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
        layer = [viewImage[0].GetLayer(0), viewImage[1].GetLayer(0), viewImage[2].GetLayer(0)]

        # 화면상 좌표(고정 좌표)에 Source Figure View 임을 표시
        # Indicates Source Figure View on screen coordinates (fixed coordinates)
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 0), "Source Figure", EColor.YELLOW, EColor.BLACK, 30)
        # 화면상 좌표(고정 좌표)에 Reduce Result View 임을 표시
        # Indicates Reduce Result View on screen coordinates (fixed coordinates)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 0), "Reduce Result1", EColor.YELLOW, EColor.BLACK, 30)
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 0), "Reduce Result2", EColor.YELLOW, EColor.BLACK, 30)

        flrgSourceFig = CFLRegion()

        # Source Figure 불러오기 // Load source figure
        if (res := flrgSourceFig.Load("../../ExampleImages/Figure/RegionForReduce.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # 0번 Layer 에 Figure 와 Text 를 출력 // Draw Figure and Text to Layer 0
        layer[0].DrawFigureImage(flrgSourceFig, EColor.LIME, 3)
        layer[0].DrawFigureImage(CFLPointArray(flrgSourceFig), EColor.BLACK, 1)
        layer[0].DrawTextImage(flrgSourceFig.GetCenter(), f"vertex count : {flrgSourceFig.GetCount()}", EColor.LIME, EColor.BLACK, 17, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)


        # Reduce 함수 실행 (Epsilon : 10.0) // Reduce function execution (Epsilon : 10.0)
        flrgResult1 = CFLRegion()
        f64Epsilon1 = 10.0

        res, flrgResult1 = flrgSourceFig.Reduce(f64Epsilon1, True, flrgResult1)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # Reduce 함수 실행 (Epsilon : 15.0) // Reduce function execution (Epsilon : 15.0)
        flrgResult2 = CFLRegion()
        f64Epsilon2 = 15.0

        res, flrgResult2 = flrgSourceFig.Reduce(f64Epsilon2, True, flrgResult2)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # View 에 결과 Region 과 정점 그리기 // Draw the resulting Region and vertices in the View
        layer[1].DrawFigureImage(flrgResult1, EColor.CYAN, 3)
        layer[2].DrawFigureImage(flrgResult2, EColor.YELLOW, 3)
        layer[1].DrawFigureImage(CFLPointArray(flrgResult1), EColor.BLACK, 1)
        layer[2].DrawFigureImage(CFLPointArray(flrgResult2), EColor.BLACK, 1)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 40), "epsilon : 10.0", EColor.YELLOW, EColor.BLACK, 20)
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 40), "epsilon : 15.0", EColor.YELLOW, EColor.BLACK, 20)
        layer[1].DrawTextImage(flrgResult1.GetCenter(), f"vertex count : {flrgResult1.GetCount()}", EColor.CYAN, EColor.BLACK, 17, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)
        layer[2].DrawTextImage(flrgResult2.GetCenter(), f"vertex count : {flrgResult2.GetCount()}", EColor.YELLOW, EColor.BLACK, 17, False, 0.0, EGUIViewImageTextAlignment.CENTER_CENTER)

        # Console 출력 // Console output
        print(f"\nSource Region Points : \nvertex count = {flrgSourceFig.GetCount()}\n\n")

        for i in range(flrgSourceFig.GetCount()):
            print(f"[{i}] ({flrgSourceFig.GetAt(i).x:.3f},{flrgSourceFig.GetAt(i).y:.3f})\n")

        print(f"\n\nResult1 Region Points : \nepsilon = {f64Epsilon1:.0f}\nvertex count = {flrgResult1.GetCount()}\n\n")

        for i in range(flrgResult1.GetCount()):
            print(f"[{i}] ({flrgResult1.GetAt(i).x:.3f},{flrgResult1.GetAt(i).y:.3f}\n")

        print(f"\n\nResult2 Region Points : \nepsilon = {f64Epsilon2:.0f}\nvertex count = {flrgResult2.GetCount()}\n\n")

        for i in range(flrgResult2.GetCount()):
            print(f"[{i}] ({flrgResult2.GetAt(i).x:.3f},{flrgResult2.GetAt(i).y:.3f}\n")


        # 이미지 뷰들을 갱신 합니다. // Update the image views.
        for i in range(3):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 셋중에 하나라도 꺼지면 종료로 간주 // Consider closed when any of the three image views are turned off
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