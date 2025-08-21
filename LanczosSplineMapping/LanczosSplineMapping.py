# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    # 이미지 뷰 선언 # Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]

    while True:
        # Source Coordinate View 생성 # Create Source Coordinate View
        if (res := viewImage[0].Create(200, 0, 700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # Destination Coordinate View 생성 # Create Destination Coordinate View
        if (res := viewImage[1].Create(700, 0, 1200, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # Restore Coordinate View 생성 # Create Restore Coordinate View
        if (res := viewImage[2].Create(1200, 0, 1700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 각 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoint of each image view.
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break
        if (res := viewImage[1].SynchronizePointOfView(viewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        # 각 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the position of each image view window
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break
        if (res := viewImage[1].SynchronizeWindow(viewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # 화면상에 잘 보이도록 좌표 90배율을 적용 # Apply 90 magnification to the coordinates so that they can be seen clearly on the screen
        f64Scale = 90.0
        # 화면상에 잘 보이도록 시점 Offset 조정 # Adjust the viewpoint offset so that it can be seen clearly on the screen
        f64CenterCoordX = 2.007
        f64CenterCoordY = 1.865
        viewImage[0].SetViewCenterAndScale(CFLPoint[Double](f64CenterCoordX, f64CenterCoordY), f64Scale)

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        layer = [viewImage[0].GetLayer(0), viewImage[1].GetLayer(0), viewImage[2].GetLayer(0)]

        # 화면상 좌표(고정 좌표)에 Source 좌표 View 임을 표시
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 0), "Source Coordinate", EColor.YELLOW, EColor.BLACK, 30)
        # 화면상 좌표(고정 좌표)에 Destination 좌표 View 임을 표시
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 0), "Destination Coordinate", EColor.YELLOW, EColor.BLACK, 30)
        # 화면상 좌표(고정 좌표)에 Restore 좌표 View 임을 표시
        layer[2].DrawTextCanvas(CFLPoint[Int32](0, 0), "Restore Coordinate (from Destination)", EColor.YELLOW, EColor.BLACK, 30)


        # 좌표 매핑용 클래스 선언 # Class declaration for coordinate mapping
        lanczosSplineMapping = CLanczosSplineMapping()

        # 만약 기존 저장된 매핑 데이터가 있다면 해당 데이터를 로드합니다. # If there is previously saved mapping data, load the data.
        # 두번째 실행부터는 파일이 생성될 것이기 때문에 아래 세팅과정을 수행하지 않고 지나가게 됩니다. # Since the file will be created from the second execution, the setting process below will be skipped.
        # 계속 새로 데이터를 생성하는것을 테스트 하려 한다면 아래 Load함수와 관련된 if문 1줄을 삭제하면 됩니다. # If you want to test continuously creating new data, you can delete one line of the if statement related to the Load function below.
        if (res := lanczosSplineMapping.Load("MappingData.fllcz")).IsFail():
            # 그리드를 (5,5)로 초기화하면서, 가상 확장 영역을 3으로 지정
            # 확장영역 밖으로 값을 변환하려고 하면 값이 나오지 않기때문에 적절한 크기로 확장을 해야 하며,
            # 가능하면 정확한 매핑을 위해 큰 범위의 매핑을 하는것을 추천합니다.
            # Initialize grid to (5,5), set virtual extent to 3
            # If you try to convert the value outside the extended range, the value does not come out,
            # so you need to expand it to an appropriate size, and if possible, it is recommended to map a large range for accurate mapping.
            iExtension = 3
            flpGridSize = CFLPoint[Int32](5, 5)
            lanczosSplineMapping.Initialize(flpGridSize, iExtension)

            flpGridIndex = CFLPoint[Int32]()
            for y in range(flpGridSize.y):
                flpGridIndex.y = y

                for x in range(flpGridSize.x):
                    flpGridIndex.x = x

                    # Grid Index와 같은 좌표로 Source 좌표를 설정 # Set the source coordinates to the same coordinates as the Grid Index
                    flpSource = CFLPoint[Double](flpGridIndex.x, flpGridIndex.y)
                    # Grid Index와 같은 좌표에서 미세한 랜덤 값을 부여해서 좌표를 왜곡 # Distort the coordinates by giving fine random values at the same coordinates as the Grid Index
                    flpDistortion = CFLPoint[Double](flpGridIndex.x + CRandomGenerator.Double(-0.1, 0.1), flpGridIndex.y + CRandomGenerator.Double(-0.1, 0.1))

                    # 위에서 설정한 좌표들을 바탕으로 LanczosSplineMapping 클래스에 하나의 Vertex를 설정
                    # Set one vertex in the LanczosSplineMapping class based on the coordinates set above
                    lanczosSplineMapping.SetControlPoint(flpGridIndex, flpSource, flpDistortion)
            
            # 설정한 데이터를 매핑 가능하도록 마무리 작업을 진행합니다.
            # 반드시 이 함수를 호출해서 결과가 OK가 나와야 매핑 사용이 가능합니다.
            # We proceed with the finishing work so that the set data can be mapped.
            # You must call this function and the result must be OK to use the mapping.
            if (res := lanczosSplineMapping.Finish()).IsFail():
                ErrorPrint(res, "Failed to finalize\n")
                break

            # Finalize 까지 완료된 상태라면 Save를 통해 파일에 저장이 가능하며,
            # 추후 Load함수를 통해 로드 시 위의 Initialize -> Set -> Finalize 과정을 생략할 수 있습니다.
            # If Finalize is completed, it can be saved to a file through Save.
            # When loading through the Load function later, the above Initialize -> Set -> Finalize process can be omitted.
            if (res := lanczosSplineMapping.Save("MappingData.fllcz")).IsFail():
                ErrorPrint(res, "Failed to save mapping data\n")
                break
        
        # 이전 if문에서 break가 발생했는지 다시 확인
        if 'res' in locals() and res.IsFail():
            break

        # 세팅이 완료된 LanczosSplineMapping 클래스를 이용해 변환을 하는 단계입니다.
        # This step is to convert using the LanczosSplineMapping class that has been set.

        # LanczosSplineMapping 클래스에 설정된 Vertex 정보를 화면에 Display
        # Display the vertex information set in the LanczosSplineMapping class on the screen
        for y in range(lanczosSplineMapping.GetRow()):
            for x in range(lanczosSplineMapping.GetColumn()):
                vertex = lanczosSplineMapping.GetControlPoint(CFLPoint[Int32](x, y))

                flpSource = CFLPoint[Double](vertex.tpSource.x, vertex.tpSource.y)
                flpDestination = CFLPoint[Double](vertex.tpDestination.x, vertex.tpDestination.y)

                for i in range(3):
                    # Destination Vertex를 각 View Layer에 Drawing # Drawing the destination vertex to each view layer
                    if (res := layer[i].DrawFigureImage(flpDestination, EColor.BLUE, 3)).IsFail():
                        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
                        break

                    # Source Vertex를 각 View Layer에 Drawing # Drawing source vertex to each view layer
                    if (res := layer[i].DrawFigureImage(flpSource, EColor.RED, 3)).IsFail():
                        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
                        break
                
                # 내부 루프에서 break가 발생했는지 다시 확인
                if 'res' in locals() and res.IsFail():
                    break

                print(f"Source Vertex ({x},{y}) : ({vertex.tpSource.x:.3f},{vertex.tpSource.y:.3f})")
                print(f"Destination Vertex ({x},{y}) : ({vertex.tpDestination.x:.3f},{vertex.tpDestination.y:.3f})")
            
            # 외부 루프에서 break가 발생했는지 다시 확인
            if 'res' in locals() and res.IsFail():
                break

        # 이전 루프에서 break가 발생했는지 다시 확인
        if 'res' in locals() and res.IsFail():
            break

        # 정점 사이를 대략 10등분, 즉 하나의 영역에 100개의 보간영역을 테스트
        # Divide the vertices into approximately 10 equal parts, that is, test 100 interpolation areas in one area
        f64Slice = 10.0
        
        flpdSource = CFLPoint[Double]() # Source 좌표 # Source coordinates
        flpaSource = CFLPointArray() # Source 좌표 (PointArray) # Source coordinates (PointArray)
        flpaDestination = CFLPointArray() # Destination 좌표 # Destination coordinates
        flpaConvertedSource = CFLPointArray() # Destination 좌표를 다시 Source로 변환, 검증 용도의 좌표 # Convert destination coordinates back to source, coordinates for verification purposes

        for y in range(int((lanczosSplineMapping.GetRow() - 1) * f64Slice) + 1):
            flpdSource.y = y / f64Slice

            for x in range(int((lanczosSplineMapping.GetColumn() - 1) * f64Slice) + 1):
                flpdSource.x = x / f64Slice
                flpaSource.PushBack(flpdSource)

        # 연산을 수행할 Source 좌표를 View에 Display # Display the source coordinates to perform the operation on the View
        if (res := layer[0].DrawFigureImage(flpaSource, EColor.YELLOW)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
            break

        # Source 좌표의 공간을 Destination 좌표 공간으로 변환 # Convert the space of source coordinates to destination coordinate space
        if (resConvertSrcToDst := lanczosSplineMapping.ConvertSourceToDestination(flpaSource, flpaDestination))[0].IsOK():
            flpaDestination = resConvertSrcToDst[1]

        # Source 좌표에서 Destination 좌표로 변환된 좌표를 View에 Display # Display coordinates converted from source coordinates to destination coordinates on the View
        if (res := layer[1].DrawFigureImage(flpaDestination, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
            break

        # 변환된 Destination 좌표를 그대로 Source 좌표로 변환해서 자신의 위치로 제대로 돌아오는지 검증
        # Verify that the converted destination coordinates are converted to source coordinates as they are and return to their own position properly
        if (resConvertDstToSrc := lanczosSplineMapping.ConvertDestinationToSource(flpaDestination, flpaConvertedSource))[0].IsOK():
            flpaConvertedSource = resConvertDstToSrc[1] # ref 파라미터 결과 할당 # Assign ref parameter result

        # 변환된 좌표를 View에 Display # Display the converted coordinates in the View
        if (res := layer[2].DrawFigureImage(flpaConvertedSource, EColor.CYAN)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
            break

        pointCount = flpaSource.GetCount()

        for i in range(pointCount):
            flpdSource = flpaSource.GetAt(i)
            flpdDestination = flpaDestination.GetAt(i)
            flpdConvertedSource = flpaConvertedSource.GetAt(i)
            print(f"Source ({flpdSource.x:.3f},{flpdSource.y:.3f}) -> Destination ({flpdDestination.x:.3f},{flpdDestination.y:.3f}) -> Source ({flpdConvertedSource.x:.3f},{flpdConvertedSource.y:.3f})")
        

        # 이미지 뷰들을 갱신 합니다. # Update the image views.
        for i in range(3):
            viewImage[i].Invalidate(True)

        # 이미지 뷰가 셋중에 하나라도 꺼지면 종료로 간주 # Consider closed when any of the three image views are turned off
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