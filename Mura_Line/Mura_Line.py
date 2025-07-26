from FLImagingClrPy import *
from time import sleep

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, string):
    if len(string) > 1:
        print(string)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")


def main():
    # 이미지 객체 선언 // Declare the image object
    fliImageSrc = CFLImage()
    fliImageDst = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageSrc = CGUIViewImage()
    viewImageDst = CGUIViewImage()

    while True:
        # 이미지 로드 // Load image
        res = fliImageSrc.Load("../../ExampleImages/Mura/Line.flif")
        if res.IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImageSrc.Create(100, 0, 548, 448)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
        if (res := viewImageSrc.SetImagePtr(fliImageSrc))[0].IsFail():
            ErrorPrint(res[0], "Failed to set image object on the image view.\n")
            break

        # Image 크기에 맞게 view의 크기를 조정 // Zoom the view to fit the image size
        if (res := viewImageSrc.ZoomFit()).IsFail():
            ErrorPrint(res, "Failed to zoom fit\n")
            break

        # 결과 이미지 뷰 생성 // Create the result image view
        if (res := viewImageDst.Create(548, 0, 996, 448)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 뷰 동기화 (시점) // Synchronize point of view
        if (res := viewImageSrc.SynchronizePointOfView(viewImageDst))[0].IsFail():
            print("Failed to synchronize view\n")
            break

        # 뷰 동기화 (창 크기) // Synchronize window size
        if (res := viewImageSrc.SynchronizeWindow(viewImageDst))[0].IsFail():
            print("Failed to synchronize view\n")
            break

        # Mura 객체 생성 // Create Mura object
        sMura = CMura()
        # 처리할 이미지 설정 // Set the image to process
        sMura.SetSourceImage(fliImageSrc)
        # 자동 임계값 모드 비활성화 // Disable auto threshold mode
        sMura.EnableAutoThresholdMode(False)
        # 커널 크기 비율 설정 // Set kernel size rate
        sMura.SetKernelSizeRate(0.25)
        # Mura 색상 타입 설정 // Set Mura color type
        sMura.SetMuraColorType(CMura.EMuraColorType.BlackOnWhite)
        # 논리 조건 설정 // Set logical condition
        sMura.SetLogicalCondition(ELogicalCondition.GreaterEqual)
        # 임계값 설정 // Set threshold value
        sMura.SetThreshold(0.8)

        # 알고리즘 실행 // Execute algorithm
        if (res := sMura.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Mura.")
            break

        # 결과 이미지 획득 // Get result image
        sMura.GetResultMuraImage(fliImageDst)

        # 결과 이미지 뷰에 출력 // Display result image
        if (res := viewImageDst.SetImagePtr(fliImageDst))[0].IsFail():
            ErrorPrint(res[0], "Failed to set image object on the image view.\n")
            break

        # 뷰 줌 // view zoom Fit
        if (res := viewImageDst.ZoomFit()).IsFail():
            ErrorPrint(res, "Failed to zoom fit\n")
            break

        # Mura 결과 필터링 (길이 기준) // Filter Mura results (based on long side length)
        if (res := sMura.Filter(CMura.EFilterItem.MinimumEnclosingRectangleLongSideLength, 50, ELogicalCondition.LessEqual)).IsFail():
            ErrorPrint(res, "Blob filtering algorithm error occurs.")
            break

        # 결과 컨투어 획득 // Get contour results
        flfaContours = CFLFigureArray()

        if (res := sMura.GetResultContours(flfaContours)[0]).IsFail():
            ErrorPrint(res, "Failed to get boundary rects from the Mura object.")
            break

        # 도형 레이어 획득 및 초기화 // Get and clear figure layer
        layer = viewImageDst.GetLayer(0)
        layer.Clear()

        # 도형 출력 // Draw contours
        if (res := layer.DrawFigureImage(flfaContours, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, 0.25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
            break

        # 이미지 갱신 // Refresh image views
        viewImageSrc.Invalidate(True)
        viewImageDst.Invalidate(True)

        while viewImageSrc.IsAvailable():
            CThreadUtilities.Sleep(1)
        break


if __name__ == '__main__':
    main()
