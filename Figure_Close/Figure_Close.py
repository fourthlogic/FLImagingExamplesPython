# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():
	
    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]

    while True:
        # Source View 생성 // Create Source View
        if (res := viewImage[0].Create(200, 0, 700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Close result1 View 생성 // Create Close result1 view
        if (res := viewImage[1].Create(700, 0, 1200, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Close result2 View 생성 // Create Close result2 view
        if (res := viewImage[2].Create(200, 500, 700, 1000)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Close result3 View 생성 // Create Close result3 view
        if (res := viewImage[3].Create(700, 500, 1200, 1000)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 각 이미지 뷰의 시점을 동기화 한다. // Synchronize the viewpoint of each image view.
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break
        if (res := viewImage[0].SynchronizePointOfView(viewImage[2]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break
        if (res := viewImage[0].SynchronizePointOfView(viewImage[3]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break

        # 각 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the position of each image view window
        if (res := viewImage[0].SynchronizeWindow(viewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window.")
            break
        if (res := viewImage[0].SynchronizeWindow(viewImage[2]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window.")
            break
        if (res := viewImage[0].SynchronizeWindow(viewImage[3]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window.")
            break

        # 화면에 출력하기 위해 Image View 에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
        layer = [viewImage[0].GetLayer(0), viewImage[1].GetLayer(0), viewImage[2].GetLayer(0), viewImage[3].GetLayer(0)]

        # 화면상 좌표(고정 좌표)에 Source Figure View 임을 표시
        # Indicates Source Figure View on screen coordinates (fixed coordinates)
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 0), "Source Figure", EColor.YELLOW, EColor.BLACK, 30)
        # 화면상 좌표(고정 좌표)에 Result View 임을 표시
        # Indicates Result View on screen coordinates (fixed coordinates)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 0), "Close Result1", EColor.YELLOW, EColor.BLACK, 30)
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 0), "Close Result2", EColor.YELLOW, EColor.BLACK, 30)
        layer[3].DrawTextCanvas(CFLPoint[Int32](0, 0), "Close Result2", EColor.YELLOW, EColor.BLACK, 30)

        flrgSourceFig = CFLRegion()

        # Source Figure 불러오기 // Load source figure
        if (res := flrgSourceFig.Load("../../ExampleImages/Figure/RegionForReduce.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # 각 Layer 에 Figure 를 출력 // Draw Figure to each Layers
        for i in range(4):
            layer[i].DrawFigureImage(flrgSourceFig, EColor.BLACK, 5)
            layer[i].DrawFigureImage(flrgSourceFig, EColor.LIME, 3)

        # Close 함수 실행 (KernelSize : 21, default kernel : Rectangle)
        # Close function execution (KernelSize : 21, default kernel : Rectangle)
        flfaResult1 = CFLFigureArray()
        i64KernelSize = 21

        # res는 (CResult, 변경된 flfaResult1) 튜플을 반환 // res returns a (CResult, modified flfaResult1) tuple
        if (res := flrgSourceFig.Close(i64KernelSize, i64KernelSize, flfaResult1))[0].IsFail():
            ErrorPrint(res[0], "Failed to calculate.")
            break
        flfaResult1 = res[1] # ref 파라미터 결과 할당 // Assign ref parameter result

        # Close 함수 실행 (KernelSize : 21, kernel shape : Circle)
        # Close function execution (KernelSize : 21, kernel shape : Circle)
        flfaResult2 = CFLFigureArray()

        # res는 (CResult, 변경된 flfaResult2) 튜플을 반환 // res returns a (CResult, modified flfaResult2) tuple
        if (res := flrgSourceFig.Close(i64KernelSize, i64KernelSize, flfaResult2, EKernelShape.Circle))[0].IsFail():
            ErrorPrint(res[0], "Failed to calculate.")
            break
        flfaResult2 = res[1] # ref 파라미터 결과 할당 // Assign ref parameter result

        # Close 함수 실행 (Figure Kernel : 반지름이 10인 원)
        # Close function execution (Figure Kernel : Circle with radius 10)
        flfaResult3 = CFLFigureArray()

        fleKernel = CFLEllipse[Double](0, 0, 5, 20, 90)
        fleForDrawing = CFLEllipse[Double]()
        fleForDrawing.Set(fleKernel)

        flpOffset = CFLPoint[Double](245, 53)
        flpOffset.x -= fleForDrawing.GetCenter().x
        flpOffset.y -= fleForDrawing.GetCenter().y

        fleForDrawing.Offset(flpOffset)

        # res는 (CResult, 변경된 flfaResult3) 튜플을 반환 // res returns a (CResult, modified flfaResult3) tuple
        if (res := flrgSourceFig.Close(fleKernel, flfaResult3))[0].IsFail():
            ErrorPrint(res[0], "Failed to calculate.")
            break
        flfaResult3 = res[1] # ref 파라미터 결과 할당 // Assign ref parameter result

        # View 에 결과 FigureArray 그리기 // Draw the resulting FigureArray in the View
        layer[1].DrawFigureImage(flfaResult1, EColor.BLACK, 5)
        layer[1].DrawFigureImage(flfaResult1, EColor.CYAN, 3)
        layer[2].DrawFigureImage(flfaResult2, EColor.BLACK, 5)
        layer[2].DrawFigureImage(flfaResult2, EColor.YELLOW, 3)
        layer[3].DrawFigureImage(flfaResult3, EColor.BLACK, 5)
        layer[3].DrawFigureImage(flfaResult3, EColor.LIGHTRED, 3)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 40), "Rectangle (KernelSize : 21)", EColor.YELLOW, EColor.BLACK, 20)
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 40), "Circle (KernelSize : 21)", EColor.YELLOW, EColor.BLACK, 20)
        layer[3].DrawTextCanvas(CFLPoint[Int32](0, 40), "User Defined Kernel", EColor.YELLOW, EColor.BLACK, 20)
        layer[3].DrawFigureCanvas(fleForDrawing, EColor.LIGHTRED, 1, EColor.LIGHTRED, EGUIViewImagePenStyle.Solid, 1.0, 0.5)

        # Console 출력 // Console output
        print("\n<Source Figure>\n\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flrgSourceFig)}")

        print(f"\n\n<Close Result1>\nKernelSize = {i64KernelSize}\nKernel Shape = Default(Rectangle)\n\n")
        print(f"Result1 Figure : {CFigureUtilities.ConvertFigureObjectToString(flfaResult1)}")

        print(f"\n\n<Close Result2>\nKernelSize = {i64KernelSize}\nKernel Shape = Circle\n\n")
        print(f"Result2 Figure : {CFigureUtilities.ConvertFigureObjectToString(flfaResult2)}")

        print("\n\n<Close Result3>\nKernel Shape = User Defined Kernel\n")
        print(f"Kernel Figure : {CFigureUtilities.ConvertFigureObjectToString(fleKernel)}\n\n")
        print(f"Result3 Figure : {CFigureUtilities.ConvertFigureObjectToString(flfaResult3)}")


        # 이미지 뷰들을 갱신 합니다. // Update the image views.
        for i in range(4):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 하나라도 꺼지면 종료로 간주 // Consider closed when any of image views are turned off
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