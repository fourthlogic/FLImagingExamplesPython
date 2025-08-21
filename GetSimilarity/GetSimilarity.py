# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

    # 이미지 뷰 선언 # Declare the image view
    viewImage = [CGUIViewImage() for _ in range(2)]

    while True:

        # Source Coordinate View 생성 # Create Source Coordinate View
        if (res := viewImage[0].Create(200, 0, 700, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Destination Coordinate View 생성 # Create Destination Coordinate View
        if (res := viewImage[1].Create(700, 0, 1200, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 각 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoint of each image view.
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 각 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the position of each image view window
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 화면에 출력하기 위해 Image View 에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        layer = [viewImage[0].GetLayer(0), viewImage[1].GetLayer(0)]

        # 화면상 좌표(고정 좌표)에 Get Similarity Matrix View 임을 표시
        # Indicates Get Similarity Matrix View on screen coordinates (fixed coordinates)
        layer[0].DrawTextCanvas(CFLPoint[Int32](0, 0), "Get Similarity Matrix", EColor.YELLOW, EColor.BLACK, 30)
        # 화면상 좌표(고정 좌표)에 Transformed View 임을 표시
        # Indicates Transformed View on screen coordinates (fixed coordinates)
        layer[1].DrawTextCanvas(CFLPoint[Int32](0, 0), "Transformed", EColor.YELLOW, EColor.BLACK, 30)

        fleSourceFig = CFLEllipse[Double]()

        # Source Figure 불러오기 # Load source figure
        if (res := fleSourceFig.Load("../../ExampleImages/Figure/Ellipse1.fig")).IsFail():
            ErrorPrint(res, "Failed to load the figure file.")
            break

        # Source Figure 를 Transformed Figure 에 복사한 후 Affine 변환
        # Affine transformation after copying the Source Figure to the Transformed Figure
        fleTransformedFig = CFLEllipse[Double]()
        fleTransformedFig.Set(fleSourceFig)
        fleTransformedFig.Scale(fleSourceFig.GetCenter(), 1.8, 1.8)
        fleTransformedFig.Rotate(30, fleSourceFig.GetCenter())
        fleTransformedFig.Offset(-200, 180)

        # Source Figure 와 Transformed Figure 로부터 점을 샘플링
        # Sample points from the Source Figure and Transformed Figure
        flfaSource = CFLFigureArray()
        flfaTransformed = CFLFigureArray()
        
        # GetSamplingPointsOnSegment returns a CResult and the modified CFLFigureArray
        if (res := fleSourceFig.GetSamplingPointsOnSegment(5, flfaSource)[0]).IsFail():
            ErrorPrint(res, "Failed to get sampling points for source figure.")
            break

        if (res := fleTransformedFig.GetSamplingPointsOnSegment(5, flfaTransformed)[0]).IsFail():
            ErrorPrint(res, "Failed to get sampling points for transformed figure.")
            break

        flpaSource = CFLPointArray()

        for i in range(flfaSource.GetCount()):
            flpaSource.PushBack(CFLPoint[Double](flfaSource.GetAt(i)))

        # Sampling 한 Source Points 들을 Transformed Points 로 복사한 후 Figure 와 동일하게 Affine 변환
        # After copying the sampled Source Points to Transformed Points, convert the Affine in the same way as the Figure
        flpaTransformed = CFLPointArray(flpaSource)
        flpaTransformed.Scale(fleSourceFig.GetCenter(), 1.8, 1.8)
        flpaTransformed.Rotate(30, fleSourceFig.GetCenter())
        flpaTransformed.Offset(-200, 180)

        # Transformed Points 에 Random Noise 를 추가 # Add Random Noise to Transformed Points
        flpaTransformedWithNoise = CFLPointArray()
        for i in range(flpaTransformed.GetCount()):
            flp = CFLPoint[Double](flpaTransformed.GetAt(i))
            flpaTransformedWithNoise.PushBack(CFLPoint[Double](flp.x + CRandomGenerator.Double(-5, 5), flp.y + CRandomGenerator.Double(-5, 5)))

        # 0번 Layer 에 Figure 들과 Text 를 출력 # Draw Figures and Text to Layer 0
        layer[0].DrawTextImage(fleSourceFig.GetCenter(), "Source", EColor.LIME, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER)
        layer[0].DrawTextImage(fleTransformedFig.GetCenter(), "Destination", EColor.CYAN, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER)

        layer[0].DrawFigureImage(fleSourceFig, EColor.RED)
        layer[0].DrawFigureImage(flpaSource, EColor.LIME, 1)

        layer[0].DrawFigureImage(fleTransformedFig, EColor.BLUE)
        layer[0].DrawFigureImage(flpaTransformedWithNoise, EColor.CYAN, 1)

        # Similarity 행렬 계산 # Calculate the similarity matrix
        matResult = CMatrix[Double]()
        
        if (res := CMatrix[Double].GetSimilarity(flpaSource, flpaTransformedWithNoise, matResult)[0]).IsFail():
            ErrorPrint(res, "Failed to calculate.")
            break

        # Console 출력 # Console output
        print("\n[index] Source Ellipse Points -> Target Points with noise")

        for i in range(flpaSource.GetCount()):
            print(f"[{i}] ({flpaSource.GetAt(i).x:.3f},{flpaSource.GetAt(i).y:.3f}) -> ({flpaTransformedWithNoise.GetAt(i).x:.3f},{flpaTransformedWithNoise.GetAt(i).y:.3f})")

        print("\n\nSimilarity Matrix")
        print(f"[{matResult.GetValue(0, 0):.3f}, {matResult.GetValue(0, 1):.3f}, {matResult.GetValue(0, 2):.3f}]")
        print(f"[{matResult.GetValue(1, 0):.3f}, {matResult.GetValue(1, 1):.3f}, {matResult.GetValue(1, 2):.3f}]")
        print(f"[{matResult.GetValue(2, 0):.3f}, {matResult.GetValue(2, 1):.3f}, {matResult.GetValue(2, 2):.3f}]\n\n")

        # 계산된 Similarity 행렬을 사용하여 Affine 변환할 Source Grid Point 생성
        # Create a Source Grid Point to be Affine Transformed using the calculated Similarity Matrix
        flpaSourceGrid = CFLPointArray()
        flpGridSize = CFLPoint[Int32](5, 5)
        i32GridPitch = 20
        i32GridOffsetX = 325
        i32GridOffsetY = 90

        for y in range(flpGridSize.y):
            i32PosY = y * i32GridPitch + i32GridOffsetY

            for x in range(flpGridSize.x):
                i32PosX = x * i32GridPitch + i32GridOffsetX

                flpaSourceGrid.PushBack(CFLPoint[Double](i32PosX, i32PosY))

        # View 에 Text 출력 # Output text to View
        flpDrawTextPosition = CFLPoint[Int32](flpaSourceGrid.GetBoundaryRect().left - 3, flpaSourceGrid.GetBoundaryRect().top - 5)

        layer[1].DrawFigureImage(flpaSourceGrid, EColor.LIME, 3)
        layer[1].DrawTextImage(flpDrawTextPosition, "Source", EColor.LIME, EColor.BLACK, 15, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)

        # Affine 변환할 Result PointArray 선언 # Declaration of Result PointArray to be converted to Affine
        flpaResult = CFLPointArray()
        # Affine 변환에 사용할 Matrix 선언 # Declaration of Matrix to be used for Affine transformation
        matA = CMatrix[Double](3, 1)
        matB = CMatrix[Double]()

        print("Affine Transform using Similarity Matrix\n")
        print("[index] Source Grid -> Transformed Grid")

        # Source Grid Point 를 Affine 변환 # Convert Source Grid Point to Affine
        for i in range(flpaSourceGrid.GetCount()):
            matA.SetValue(0, 0, flpaSourceGrid.GetAt(i).x)
            matA.SetValue(1, 0, flpaSourceGrid.GetAt(i).y)
            matA.SetValue(2, 0, 1)

            if (res := matResult.Multiply(matA, matB)[0]).IsFail():
                ErrorPrint(res, "Failed to calculate Matrix Operation\n")
                break

            flpaResult.PushBack(CFLPoint[Double](matB.GetValue(0, 0), matB.GetValue(1, 0)))

            # Console 출력 # Console output
            print(f"[{i}] ({flpaSourceGrid.GetAt(i).x:.3f},{flpaSourceGrid.GetAt(i).y:.3f}) -> ({flpaResult.GetAt(i).x:.3f},{flpaResult.GetAt(i).y:.3f})")
        
        if (res := matResult.Multiply(matA, matB)[0]).IsFail():
            break

        # View 에 Text 출력 # Output text to View
        flpDrawTextPosition.Scale(flpaSourceGrid.GetCenter(), 1.8, 1.8)
        flpDrawTextPosition.Rotate(30, flpaSourceGrid.GetCenter())
        flpDrawTextPosition.Offset(-200, 180)

        layer[1].DrawFigureImage(flpaResult, EColor.CYAN, 3)
        layer[1].DrawTextImage(flpDrawTextPosition, "Transformed", EColor.CYAN, EColor.BLACK, 15, False, 30, EGUIViewImageTextAlignment.LEFT_BOTTOM)

        layer[0].DrawTextCanvas(CFLPoint[Int32](5, 40), f"[{matResult.GetValue(0, 0):.3f}, {matResult.GetValue(0, 1):.3f}, {matResult.GetValue(0, 2):.3f}]", EColor.YELLOW, EColor.BLACK, 15)
        layer[0].DrawTextCanvas(CFLPoint[Int32](5, 60), f"[{matResult.GetValue(1, 0):.3f}, {matResult.GetValue(1, 1):.3f}, {matResult.GetValue(1, 2):.3f}]", EColor.YELLOW, EColor.BLACK, 15)
        layer[0].DrawTextCanvas(CFLPoint[Int32](5, 80), f"[{matResult.GetValue(2, 0):.3f}, {matResult.GetValue(2, 1):.3f}, {matResult.GetValue(2, 2):.3f}]", EColor.YELLOW, EColor.BLACK, 15)

        # 이미지 뷰들을 갱신 합니다. # Update the image views.
        for i in range(2):
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