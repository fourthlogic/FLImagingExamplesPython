# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")

# 메인 함수 # Main function
def main():
    # 이미지 객체 배열 선언 # Declare image object array
    arrFliImage = [CFLImage() for _ in range(3)]

    # 이미지 뷰 배열 선언 # Declare image view array
    arrViewImage = [CGUIViewImage() for _ in range(3)]

    while True:
        # 이미지 로드 # Load images
        if (res := arrFliImage[0].Load("../../ExampleImages/OperationAdd/Sky.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        if (res := arrFliImage[1].Load("../../ExampleImages/OperationAdd/Flower.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # Destination 이미지를 Source 이미지와 동일하게 생성 # Assign destination image same as source image
        if (res := arrFliImage[2].Assign(arrFliImage[0])).IsFail():
            ErrorPrint(res, "Failed to assign the image file.")
            break

        # 이미지 뷰 생성 # Create image views
        if (res := arrViewImage[0].Create(100, 0, 612, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := arrViewImage[1].Create(612, 0, 1124, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := arrViewImage[2].Create(1124, 0, 1636, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지 디스플레이 # Display images in the image views
        bError = False
        for i in range(3):
            if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.")
                bError = True
                break
        if bError:
            break

        # 뷰 시점 동기화 # Synchronize viewpoints
        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 윈도우 위치 동기화 # Synchronize window positions
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # Operation Add 객체 생성 # Create Add object
        operationAdd = COperationAdd()

        # Source 이미지 설정 # Set source image
        operationAdd.SetSourceImage(arrFliImage[0])

        # Operand 이미지 설정 # Set operand image
        operationAdd.SetOperandImage(arrFliImage[1])

        # Destination 이미지 설정 # Set destination image
        operationAdd.SetDestinationImage(arrFliImage[2])

        # 연산 방식 설정 # Set operation source
        operationAdd.SetOperationSource(EOperationSource.Image)

        # 알고리즘 수행 # Execute algorithm
        if (res := operationAdd.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute operation add.")
            print(res.GetString())
            break

        # 이미지 레이어 배열 생성 # Create image layer array
        arrLayer = [None] * 3

        # 레이어 가져오고 초기화 # Get layers and clear existing shapes
        for i in range(3):
            arrLayer[i] = arrViewImage[i].GetLayer(0)
            arrLayer[i].Clear()

        # 텍스트 출력 좌표 설정 # Text output coordinate
        tpPosition = TPoint[Double](0, 0)

        # 텍스트 출력 # Draw text on each view
        if (res := arrLayer[0].DrawTextCanvas(tpPosition, "Source Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            return

        if (res := arrLayer[1].DrawTextCanvas(tpPosition, "Operand Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            return

        if (res := arrLayer[2].DrawTextCanvas(tpPosition, "Destination Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            return

        # 이미지 뷰 갱신 # Invalidate image views
        for i in range(3):
            arrViewImage[i].Invalidate(True)

        # 이미지 뷰 종료 대기 # Wait until all views are closed
        while (arrViewImage[0].IsAvailable() and
               arrViewImage[1].IsAvailable() and
               arrViewImage[2].IsAvailable()):
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()