from FLImagingClrPy import *

def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

def main():
    # 이미지 객체 선언 // Declare the image object
    arrFliImage = [CFLImage() for _ in range(3)]

    # 이미지 뷰 선언 // Declare the image view
    arrViewImage = [CGUIViewImage() for _ in range(3)]

    while True:
        # 이미지 로드 // Load image
        res = arrFliImage[0].Load("../../ExampleImages/OperationMaximum/Flower.flif")
        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 복사 // Assign images
        res = arrFliImage[1].Assign(arrFliImage[0])
        if res.IsFail():
            ErrorPrint(res, "Failed to assign the image file.")
            break

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

        # 이미지 뷰에 이미지 설정 // Set images to views
        bError = False
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

        # Scalar 값 생성 // Create scalar values
        mvScalar = CMultiVar[float](100, 100, 100)
        mvScalar2 = CMultiVar[float](200, 200, 200)

        # Operation Maximum 객체 생성 // Create Operation Maximum object
        maximum = COperationMaximum()
        maximum.SetSourceImage(arrFliImage[0])
        maximum.SetDestinationImage(arrFliImage[1])
        maximum.SetOperationSource(EOperationSource.Scalar)
        maximum.SetScalarValue(mvScalar)

        # 알고리즘 수행 // Execute algorithm
        if (res := maximum.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute operation maximum (first).")
            break

        maximum.SetDestinationImage(arrFliImage[2])
        maximum.SetOperationSource(EOperationSource.Scalar)
        maximum.SetScalarValue(mvScalar2)

        if (res := maximum.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute operation maximum (second).")
            break

        # 레이어 획득 및 초기화 // Get and clear layers
        arrLayer = [arrViewImage[i].GetLayer(0) for i in range(3)]
        for layer in arrLayer:
            layer.Clear()

        # 텍스트 위치 // Text position
        tpPosition = TPoint[float](0, 0)

        # 텍스트 출력 // Draw text on layers
        if (res := arrLayer[0].DrawTextCanvas(tpPosition, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break
        if (res := arrLayer[1].DrawTextCanvas(tpPosition, "Destination1 Image(Maximum 100)", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break
        if (res := arrLayer[2].DrawTextCanvas(tpPosition, "Destination2 Image(Maximum 200)", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        # 뷰 갱신 // Invalidate views
        for view in arrViewImage:
            view.Invalidate(True)

        # 뷰 종료 대기 // Wait until all views are closed
        while all(view.IsAvailable() for view in arrViewImage):
            CThreadUtilities.Sleep(1)

        break

if __name__ == "__main__":
    main()