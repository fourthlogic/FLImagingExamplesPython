from FLImagingClrPy import *

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")

def main():
    # 이미지 객체 선언 // Declare the image object
    arrFliImage = [CFLImage() for _ in range(3)]

    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for _ in range(3)]

    while True:
        # 이미지 로드 // Load images
        res = arrFliImage[0].Load("../../ExampleImages/OperationSubtract/House.flif")
        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        res = arrFliImage[1].Load("../../ExampleImages/OperationSubtract/Sunset.flif")
        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 복사 // Assign image
        res = arrFliImage[2].Assign(arrFliImage[0])
        if res.IsFail():
            ErrorPrint(res, "Failed to assign the image file.")
            break

        # 이미지 뷰 생성 // Create image views
        res = arrViewImage[0].Create(100, 0, 612, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break
        res = arrViewImage[1].Create(612, 0, 1124, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break
        res = arrViewImage[2].Create(1124, 0, 1636, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        bError = False
        # 이미지 뷰에 이미지 설정 // Set images to views
        for i in range(3):
            if (res := arrViewImage[i].SetImagePtr(arrFliImage[i]))[0].IsFail():
                ErrorPrint(res[0], "Failed to set image object on the image view.")
                bError = True
                break
        if bError:
            break

        # 이미지 뷰 동기화 // Synchronize viewpoints and windows
        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break
        if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[2]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize view")
            break
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[1]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window")
            break
        if (res := arrViewImage[0].SynchronizeWindow(arrViewImage[2]))[0].IsFail():
            ErrorPrint(res[0], "Failed to synchronize window")
            break

        # COperationSubtract 객체 생성 // Create COperationSubtract object
        subtract = COperationSubtract()
        # Source 이미지 설정 // Set source image
        subtract.SetSourceImage(arrFliImage[0])
        # Operand 이미지 설정 // Set operand image
        subtract.SetOperandImage(arrFliImage[1])
        # Destination 이미지 설정 // Set destination image
        subtract.SetDestinationImage(arrFliImage[2])
        # 연산 방식 설정 // Set operation source
        subtract.SetOperationSource(EOperationSource.Image)

        # 알고리즘 수행 // Execute the algorithm
        if (res := subtract.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute operation subtract.")
            break

        # 레이어 획득 및 초기화 // Get and clear layers
        arrLayer = [arrViewImage[i].GetLayer(0) for i in range(3)]
        for layer in arrLayer:
            layer.Clear()

        # 텍스트 위치 // Text position
        tpPosition = TPoint[Double](0, 0)

        # 텍스트 출력 // Draw text on layers
        if (res := arrLayer[0].DrawTextCanvas(tpPosition, "Source Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break
        if (res := arrLayer[1].DrawTextCanvas(tpPosition, "Operand Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break
        if (res := arrLayer[2].DrawTextCanvas(tpPosition, "Destination Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        # 이미지 뷰 갱신 // Invalidate views
        for view in arrViewImage:
            view.Invalidate(True)

        # 이미지 뷰 종료 대기 // Wait until all views are closed
        while all(view.IsAvailable() for view in arrViewImage):
            CThreadUtilities.Sleep(1)

        break

if __name__ == "__main__":
    main()