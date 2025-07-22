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
        res = fliImageSrc.Load("../../ExampleImages/Mura/Spot.flif")
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

        # 결과 이미지 뷰 생성 // Create result image view
        if (res := viewImageDst.Create(548, 0, 996, 448)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 결과 이미지 디스플레이 // Display result image
        if (res := viewImageDst.SetImagePtr(fliImageDst))[0].IsFail():
            ErrorPrint(res[0], "Failed to set image object on the image view.\n")
            break

        # 시점 및 창 동기화 // Synchronize viewpoints and window sizes
        if (res := viewImageSrc.SynchronizePointOfView(viewImageDst))[0].IsFail():
            print("Failed to synchronize view\n")
            break
        if (res := viewImageSrc.SynchronizeWindow(viewImageDst))[0].IsFail():
            print("Failed to synchronize view\n")
            break

        # Mura 객체 생성 // Create Mura object
        sMura = CMura()

        # 처리할 이미지 설정 // Set the image to process
        sMura.SetSourceImage(fliImageSrc)

        # Auto Threshold 모드 설정 // Set auto threshold mode
        sMura.EnableAutoThresholdMode(True)

        # Kernel Size Rate 설정 // Set kernel size rate
        sMura.SetKernelSizeRate(0.25)

        # Mura Color Type 설정 // Set mura color type
        sMura.SetMuraColorType(CMura.EMuraColorType.All)

        # 알고리즘 실행 // Execute algorithm
        if (res := sMura.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Mura.")
            break

        # 결과 이미지 얻기 // Get result image
        sMura.GetResultMuraImage(fliImageDst)

        # 결과 이미지 디스플레이 // Display result image
        if (res := viewImageDst.SetImagePtr(fliImageDst))[0].IsFail():
            ErrorPrint(res[0], "Failed to set image object on the image view.\n")
            break

        # 컨투어 결과 얻기 위한 FigureArray 선언 // Declare FigureArray for contours
        flfaContours = CFLFigureArray()

        # Mura 결과 중 Contour 획득 // Get contours from Mura result
        if (res := sMura.GetResultContours(flfaContours)[0]).IsFail():
            ErrorPrint(res, "Failed to get boundary rects from the Mura object.")
            break

        # 레이어 얻기 및 초기화 // Get and clear layer
        layer = viewImageDst.GetLayer(0)
        layer.Clear()

        # 도형 그리기 // Draw figures
        if (res := layer.DrawFigureImage(flfaContours, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, 0.25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
            break

        # Rect 정보값 표시 // Display rect info
        for i in range(flfaContours.GetCount()):
            pFlrg = flfaContours.GetAt(i)
            strText = f"{i}"
            layer.DrawTextImage(pFlrg.GetCenter(), strText, EColor.CYAN)

        # 이미지 뷰 갱신 // Refresh views
        viewImageSrc.Invalidate(True)
        viewImageDst.Invalidate(True)

        # 뷰 종료 대기 // Wait for view to close
        while viewImageSrc.IsAvailable():
            CThreadUtilities.Sleep(1)
        break

if __name__ == '__main__':
    main()
