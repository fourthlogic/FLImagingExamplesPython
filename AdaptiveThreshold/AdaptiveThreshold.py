# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

# 메인 함수 // Main function
def main():
    # 이미지 객체 선언 // Declare the image object
    fliISrcImage = CFLImage()
    fliIDstImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage()]

    while True:
        # 이미지 로드 // Load image
        if (res := fliISrcImage.Load("../../ExampleImages/Threshold/Sun.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window")
            break

        # 이미지 뷰에 이미지를 디스플레이 // Display the image in the image view
        if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        if (res := viewImage[1].SetImagePtr(fliIDstImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        # Adaptive Threshold 객체 생성 // Create Adaptive Threshold object
        adaptiveThreshold = CAdaptiveThreshold()

        # Source 이미지 설정 // Set source image
        adaptiveThreshold.SetSourceImage(fliISrcImage)

        # Destination 이미지 설정 // Set destination image
        adaptiveThreshold.SetDestinationImage(fliIDstImage)

        # 커널 사이즈 설정 // Set kernel size
        adaptiveThreshold.SetKernel(7, 7)

        # 임계값 옵셋 설정 // Set threshold offset
        adaptiveThreshold.SetThresholdOffset(5)

        # 알고리즘 수행 // Execute the algorithm
        if (res := adaptiveThreshold.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute AdaptiveThreshold.")
            break

        # 레이어 가져오기 // Get image layers
        layer1 = viewImage[0].GetLayer(0)
        if res.IsFail():
            ErrorPrint(res, "Failed to get layer from source view.")
            break

        layer2 = viewImage[1].GetLayer(0)
        if res.IsFail():
            ErrorPrint(res, "Failed to get layer from destination view.")
            break

        # Text 출력 // Display text
        flpPoint = CFLPoint[Double](0, 0)
        if (res := layer1.DrawTextImage(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text on source layer.")
            break

        if (res := layer2.DrawTextImage(flpPoint, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text on destination layer.")
            break

        # 이미지 뷰 갱신 // Update image view
        viewImage[0].Invalidate(True)
        viewImage[1].Invalidate(True)

        # 이미지 뷰가 종료될 때까지 대기 // Wait for image view to close
        while viewImage[0].IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()