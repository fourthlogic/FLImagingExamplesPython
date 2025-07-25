# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():
	
    # 3D 뷰 선언
    # Declaration of the 3D view
    view3D = [CGUIView3D() for _ in range(2)]

    # 3D 뷰 layer 선언
    # Declaration of the 3D view layer
    layer3D = [CGUIView3DLayer() for _ in range(2)]

    while True:
        # 3D 뷰 생성 // Create the 3D view
        if (res := view3D[0].Create(400, 0, 812, 384)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.")
            break

        if (res := view3D[1].Create(812, 0, 1224, 384)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.")
            break

        # 각 3D 뷰의 시점을 동기화 한다. // Synchronize the viewpoint of each 3D view.
        if (res := view3D[0].SynchronizePointOfView(view3D[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 각 3D 뷰 윈도우의 위치를 동기화 한다 // Synchronize the position of each 3D view window
        if (res := view3D[0].SynchronizeWindow(view3D[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 각각의 3D View 에서 0번 레이어 가져오기 // Get Layer 0 from each 3D view
        for i in range(2):
            layer3D[i] = view3D[i].GetLayer(0)

        # 각 레이어 캔버스에 텍스트 그리기 // Draw text to each Layer Canvas
        layer3D[0].DrawTextCanvas(CFLPoint[Double](3, 0), "Figure A", EColor.YELLOW, EColor.BLACK, 20)
        layer3D[1].DrawTextCanvas(CFLPoint[Double](3, 0), "Figure A", EColor.YELLOW, EColor.BLACK, 20)

        layer3D[0].DrawTextCanvas(CFLPoint[Double](3, 30), "Base Plane", EColor.YELLOW, EColor.BLACK, 15)
        layer3D[1].DrawTextCanvas(CFLPoint[Double](3, 30), "Length : +20", EColor.YELLOW, EColor.BLACK, 15)

        # Figure A 의 한쪽 면 생성 // Create one side of Figure A
        flpFigA0 = CFLPoint3[Double](0, 0, 5)
        flpFigA1 = CFLPoint3[Double](0, 10, 5)
        flpFigA2 = CFLPoint3[Double](10, 0, 0)
        fltBasePlaneFigA = CFLTriangle3[Double](flpFigA0, flpFigA1, flpFigA2)

        # 두 번째 평면은 첫 번째 평면의 법선 방향으로 `Length`만큼 떨어진 위치에 계산됩니다.
        # The second plane is calculated at a distance of `Length` in the normal direction of the first plane.
        f64LengthA = 20.0
        fltsSolidFigA = CFLTriangularSolid3[Double](fltBasePlaneFigA, f64LengthA)


        # 3D 뷰에 3D figure 추가 // Add 3D figures to the 3D view
        view3DObj = CGUIView3DObject()
        view3DObj.SetTopologyType(ETopologyType3D.Wireframe)

        arr3DObj = [CFL3DObject(fltBasePlaneFigA), CFL3DObject(fltsSolidFigA)]

        for i in range(2):
            view3DObj.Set3DObject(arr3DObj[i])
            view3D[i].PushObject(view3DObj)

        # 추가한 3D 객체가 화면 안에 들어오도록 Zoom Fit // Perform Zoom Fit to ensure added 3D objects are within the view
        view3D[1].ZoomFit()

        # 3D 뷰어의 시점(카메라) 변경 // Change the viewpoint (camera) of the 3D viewer
        cam1 = view3D[1].GetCamera()
        cam1.SetPosition(CFLPoint3[Single](22.43, -30.54, 7.29))
        cam1.SetDirection(CFLPoint3[Single](-0.41, 0.90, 0.12))
        cam1.SetDirectionUp(CFLPoint3[Single](0.06, -0.10, 0.99))
        view3D[1].SetCamera(cam1)


        # Console 출력 // Console output
        print("<Figure A>\n")
        print(f"Base Plane : \n{CFigureUtilities.ConvertFigureObjectToString(fltBasePlaneFigA)}\n\n")
        print(f"Solid Figure : \n{CFigureUtilities.ConvertFigureObjectToString(fltsSolidFigA)}\n\n")

        # 3D 뷰들을 갱신 합니다. // Update the 3D views.
        for i in range(2):
            view3D[i].UpdateScreen()
            view3D[i].Invalidate(True)

        # 3D 뷰가 둘중에 하나라도 꺼지면 종료로 간주 // Consider closed when any of the two 3D views are turned off
        while view3D[0].IsAvailable() and view3D[1].IsAvailable():
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