from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


def ErrorPrint(cResult: CResult, msg: str):
    # 에러 메시지 출력 // Print error message
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {cResult.GetResultCode()}\nError name : {cResult.GetString()}\n")

def main():
    # 이미지 객체 선언 // Declare the image object
    fliSourceImage = CFLImage()
    fliDestinationImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageSource = CGUIViewImage()
    viewImageDestination = CGUIViewImage()

    while True:
        # 이미지 로드 // Load image
        res = fliSourceImage.Load("../../ExampleImages/OperationLogicalNor/Cat.flif")

        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        # Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
        res = fliDestinationImage.Assign(fliSourceImage)
        if res.IsFail():
            ErrorPrint(res, "Failed to assign the image file.\n")
            break

        # 이미지 뷰 생성 // Create image view
        res = viewImageSource.Create(100, 0, 612, 512)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the source image view.\n")
            break

        # 이미지 뷰 생성 // Create image view
        res = viewImageDestination.Create(612, 0, 1124, 512)

        if res.IsFail():
            ErrorPrint(res, "Failed to create the destination image view.\n")
            break

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        if (res := viewImageSource.SynchronizePointOfView(viewImageDestination)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view.\n")
            break

        # Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
        if (res := viewImageSource.SetImagePtr(fliSourceImage))[0].IsFail():
            ErrorPrint(res, "Failed to set source image object on the image view.\n")
            break

        # Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
        if (res := viewImageDestination.SetImagePtr(fliDestinationImage))[0].IsFail():
            ErrorPrint(res, "Failed to set destination image object on the image view.\n")
            break

        # 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
        if (res := viewImageSource.SynchronizeWindow(viewImageDestination))[0].IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # Operation Logical Nor 객체 생성 // Create Logical Nor object
        logicalNor = COperationLogicalNor()

        # Source 이미지 설정 // Set source image
        logicalNor.SetSourceImage(fliSourceImage)

        # ROI 범위 설정 // Set the ROI value
        flcSourceROI = CFLCircle[Double](128, 128, 80, 0, 0, 360, EArcClosingMethod.EachOther)

        # Source 이미지의 ROI 지정 // Set the Source ROI
        logicalNor.SetSourceROI(flcSourceROI)

        # Scalar Operation 소스로 설정 // Set Operation Source to scalar
        logicalNor.SetOperationSource(EOperationSource.Scalar)

        # 스칼라 값 지정 // Set the Scalar value
        logicalNor.SetScalarValue(0)

        # Destination 이미지 설정 // Set destination image
        logicalNor.SetDestinationImage(fliDestinationImage)

        # Operation Logical Nor 수행 // Execute Logical Nor operation
        res = logicalNor.Execute()

        if res.IsFail():
            ErrorPrint(res, "Failed to execute OperationLogicalNor.\n")
            break
        
        # 출력을 위한 이미지 레이어를 얻어옵니다. // Gets the image layer for output
        # 따로 해제할 필요 없음 // No need to release separately
        layerSource = viewImageSource.GetLayer(0)
        layerDestination = viewImageDestination.GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 // Clear existing shapes in the layers
        layerSource.Clear()
        layerDestination.Clear()

        if(res := layerSource.DrawFigureImage(flcSourceROI, EColor.LIME)).IsFail() :
            ErrorPrint(res, "Failed to draw figure. \n")
            break		

        if(res := layerDestination.DrawFigureImage(flcSourceROI, EColor.LIME)).IsFail() :
            ErrorPrint(res, "Failed to draw figure. \n")
            break	

        # View 정보를 디스플레이 합니다. // Display view information (text)
        flpPoint = CFLPoint[Single](0, 0)

        res = layerSource.DrawTextCanvas(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 30)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw text on source layer.\n")
            break

        res = layerDestination.DrawTextCanvas(flpPoint, "Destination Image", EColor.YELLOW, EColor.BLACK, 30)
        if res.IsFail():
            ErrorPrint(res, "Failed to draw text on destination layer.\n")
            break

        # 이미지 뷰를 갱신 합니다. // Update the image view
        viewImageSource.Invalidate(True)
        viewImageDestination.Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait until image views are closed
        while viewImageSource.IsAvailable() and viewImageDestination.IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()