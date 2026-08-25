# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

def main():

    # 이미지 객체 선언 # Declare the image object
    arrFliImage = [CFLImage() for _ in range(3)]

    # 이미지 뷰 선언 # Declare the image view
    arrViewImage = [CGUIViewImage() for _ in range(3)]

    while True:
        # 이미지 로드 # Load image
        if (res := arrFliImage[0].Load("../../ExampleImages/OperationMaximum/palmtree.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        # 이미지 로드 # Load image
        if (res := arrFliImage[1].Load("../../ExampleImages/OperationMaximum/Flower.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        # Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
        if (res := arrFliImage[2].Assign(arrFliImage[0])).IsFail():
            ErrorPrint(res, "Failed to assign the image file.\n")
            break

        # 이미지 뷰 생성 # Create image view
        if (res := arrViewImage[0].Create(100, 0, 612, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰 생성 # Create image view
        if (res := arrViewImage[1].Create(612, 0, 1124, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰 생성 # Create image view
        if (res := arrViewImage[2].Create(1124, 0, 1636, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        bError = False

        # 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
        for i in range(3):
            if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                bError = True
                break

        if bError:
            break

        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        # 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # Operation Maximum 객체 생성 # Create Operation Maximum object
        operationMaximum = COperationMaximum()
        # Source 이미지 설정 # Set source image
        operationMaximum.SetSourceImage(arrFliImage[0])
        # Operand 이미지 설정 # Set Operand image
        operationMaximum.SetOperandImage(arrFliImage[1])
        # Destination 이미지 설정 # Set destination image
        operationMaximum.SetDestinationImage(arrFliImage[2])
        # 연산 방식 설정 # Set operation source
        operationMaximum.SetOperationSource(EOperationSource.Image)

        # 알고리즘 수행 # Execute the algorithm
        if (res := operationMaximum.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute operation maximum.")
            print(res.GetString())
            break

        arrLayer = [arrViewImage[i].GetLayer(0) for i in range(3)]

        for i in range(3):
            # 출력을 위한 이미지 레이어를 얻어옵니다. # Gets the image layer for output.
            # 따로 해제할 필요 없음 # No need to release separately
            # 기존에 Layer에 그려진 도형들을 삭제 # Delete the shapes drawn on the existing layer
            arrLayer[i].Clear()

        # View 정보를 디스플레이 합니다. # Display View information.
        # 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.
        # The function DrawTextCanvas below draws a String based on the screen coordinates.
        # 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
        #                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
        # Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
        #                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
        tpPosition = TPoint[float](0, 0)

        if (res := arrLayer[0].DrawTextCanvas(tpPosition, "Source Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        if (res := arrLayer[1].DrawTextCanvas(tpPosition, "Operand Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        if (res := arrLayer[2].DrawTextCanvas(tpPosition, "Destination Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        # 이미지 뷰를 갱신 합니다. # Update the image view.
        arrViewImage[0].Invalidate(True)
        arrViewImage[1].Invalidate(True)
        arrViewImage[2].Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
        while (arrViewImage[0].IsAvailable()
               and arrViewImage[1].IsAvailable()
               and arrViewImage[2].IsAvailable()):
            CThreadUtilities.Sleep(1)

        for i in range(3):
            arrViewImage[i].Destroy()

        break


if __name__ == "__main__":
    main()
