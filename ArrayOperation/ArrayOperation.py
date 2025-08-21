# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    i32ViewCount = 4

    # 이미지 뷰 선언 # Declare the image view
    viewImage = [CGUIViewImage() for _ in range(i32ViewCount)]

    while True:
        # 이미지 뷰 생성 # Create image view
        if (res := viewImage[0].Create(400, 0, 912, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(912, 0, 1424, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[2].Create(400, 384, 912, 768)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[3].Create(912, 384, 1424, 768)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        for i in range(1, i32ViewCount):
            # 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoint of the image view
            if (res := viewImage[0].SynchronizePointOfView(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize view")
                break

            # 이미지 뷰 윈도우의 위치를 맞춤 # Align the position of the image view window
            if (res := viewImage[0].SynchronizeWindow(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize window.")
                break
        
        if (res := viewImage[0].SynchronizeWindow(viewImage[i32ViewCount - 1])[0]).IsFail():
            break

        # SourceView, DstView 의 0번 레이어 가져오기 # Get Layer 0 of SourceView, DstView
        layerView = [viewImage[i].GetLayer(0) for i in range(i32ViewCount)]

        # Figure 생성 # Create figure
        flr = CFLRect[Double](50, 50, 100, 100, 15)
        flq = CFLQuad[Double](200, 50, 360, 50, 400, 160, 150, 110)
        flc = CFLCircle[Double](100.0, 150.0, 30.0, 0, 30, 90, EArcClosingMethod.Center)
        fle = CFLEllipse[Double](300, 250, 100, 50, 0, 30, 200, EArcClosingMethod.Center)

        flfa = CFLFigureArray()

        flfa.PushBack(flr)
        flfa.PushBack(flq)
        flfa.PushBack(flc)
        flfa.PushBack(fle)

        print("Figure Array\n")

        for i in range(flfa.GetCount()):
            strFigure = f"[{i}]\n {CFigureUtilities.ConvertFigureObjectToString(flfa.GetAt(i))}\n"
            print(f"{strFigure}")

        print("\n")

        # Figure 그리기 # Draw Figure
        for i in range(flfa.GetCount()):
            layerView[i].DrawFigureImage(flfa, EColor.LIME)

        ################################ GetCenterElementwise()
        # 중심점 좌표를 담을 FigureArray 생성 # Create a FigureArray to hold the coordinates of the center point
        flfaCenter = CFLFigureArray()

        # Figure Array 각 요소의 중심점 계산 # Calculate the center point of each element of Figure Array
        res, flfaCenter = flfa.GetCenterElementwise(flfaCenter)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate center elementwise.")
            break

        # 중심들을 View0의 0번 레이어에 그리기 # Draw the centers on layer 0 of View0
        layerView[0].DrawFigureImage(flfaCenter, EColor.RED)
        layerView[0].DrawTextCanvas(CFLPoint[Double](0, 0), "GetCenterElementwise() Result", EColor.YELLOW, EColor.BLACK, 15)

        # 콘솔에 중심 좌표 표시 # Print center coordinates in console
        print("Center Point\n")

        for i in range(flfa.GetCount()):
            strFigure = f"[{i}]\n {CFigureUtilities.ConvertFigureObjectToString(flfaCenter.GetAt(i))}\n"
            print(f"{strFigure}")

        print("\n")


        ################################ GetPerimeterElementwise()
        # 각 둘레의 길이를 저장할 CFLFigureArray 생성 # Create CFLFigureArray to store the length of each perimeter
        flfaPerimeter = CFLFigureArray()

        # Figure Array 각 요소의 둘레 계산 # Calculate the perimeter of each element of the Figure Array
        res, flfaPerimeter = flfa.GetPerimeterElementwise(flfaPerimeter)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate perimeter elementwise.")
            break

        # Figure Array 각 요소의 둘레 표시 # Display perimeter of each element of Figure Array
        for i in range(flfaPerimeter.GetCount()):
            strPerimeter = f"{CFLScalar[Double](flfaPerimeter.GetAt(i)).v}"
            layerView[1].DrawTextImage(flfaCenter.GetAt(i), strPerimeter, EColor.BLACK)

        layerView[1].DrawTextCanvas(CFLPoint[Double](0, 0), "GetPerimeterElementwise() Result", EColor.YELLOW, EColor.BLACK, 15)

        # 콘솔에 길이 표시 # Display the length in the console
        print("Perimeter\n")

        for i in range(flfaPerimeter.GetCount()):
            strFigure = f"[{i}]\n {CFLScalar[Double](flfaPerimeter.GetAt(i)).v}\n"
            print(f"{strFigure}")

        print("\n")


        ################################ GetCenterOfGravityElementwise()
        # 무게중심점 좌표를 담을 FigureArray 생성 # Create a FigureArray to contain the coordinates of the center of gravity
        flfaCenterOfGravity = CFLFigureArray()

        # Figure Array 각 요소의 무게중심점 계산 # Calculate the center of gravity of each element of the Figure Array
        res, flfaCenterOfGravity = flfa.GetCenterOfGravityElementwise(flfaCenterOfGravity)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate center of gravity elementwise.")
            break

        # 무게중심들을 View0의 0번 레이어에 그리기 # Draw the centers of gravity on Layer 0 of View0
        layerView[2].DrawFigureImage(flfaCenterOfGravity, EColor.CYAN)
        layerView[2].DrawTextCanvas(CFLPoint[Double](0, 0), "GetCenterOfGravityElementwise() Result", EColor.YELLOW, EColor.BLACK, 15)

        # 콘솔에 무게중심 좌표 표시 # Display barycentric coordinates in console
        print("Center Of Gravity Point\n")

        for i in range(flfa.GetCount()):
            strFigure = f"[{i}]\n {CFigureUtilities.ConvertFigureObjectToString(flfaCenterOfGravity.GetAt(i))}\n"
            print(f"{strFigure}")

        print("\n")


        ################################ GetMinimumEnclosingRectangleElementwise()
        # 최소둘레 직사각형을 담을 FigureArray 생성 # Create a FigureArray to contain the minimum enclosing rectangle
        flfaMER = CFLFigureArray()

        # Figure Array 각 요소의 최소둘레 직사각형을 계산 # Calculate the minimum enclosing rectangle of each element of the Figure Array
        res, flfaMER = flfa.GetMinimumEnclosingRectangleElementwise(flfaMER)

        if res.IsFail():
            ErrorPrint(res, "Failed to calculate minimum enclosing rectangle elementwise.")
            break

        # 최소둘레 직사각형들을 View0의 0번 레이어에 그리기 # Draw the minimum enclosing rectangle on Layer 0 of View0
        layerView[3].DrawFigureImage(flfaMER, EColor.BLUE)
        layerView[3].DrawTextCanvas(CFLPoint[Double](0, 0), "GetMinimumEnclosingRectangleElementwise() Result", EColor.YELLOW, EColor.BLACK, 15)

        # 콘솔에 최소둘레 직사각형을 표시 # Display the minimum enclosing rectangle in console
        print("Minimum Enclosing Rectangle\n")

        for i in range(flfa.GetCount()):
            strFigure = f"[{i}]\n {CFigureUtilities.ConvertFigureObjectToString(flfaMER.GetAt(i))}\n"
            print(f"{strFigure}")

        print("\n")

        # 이미지 뷰를 갱신 합니다. # Update image view
        for i in range(i32ViewCount):
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