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
        if (res := fliISrcImage.Load("../../ExampleImages/Threshold/Mountain.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 뷰 시점 동기화 // Synchronize view points
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 윈도우 위치 동기화 // Synchronize window positions
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window")
            break

        # 이미지 뷰에 이미지 디스플레이 // Display image in the view
        if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        if (res := viewImage[1].SetImagePtr(fliIDstImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        # Watersheds Threshold Marker 객체 생성 // Create Watersheds Threshold Marker object
        watershedsThreshold = CWatershedsThresholdMarker()

        # Source 이미지 설정 // Set source image
        watershedsThreshold.SetSourceImage(fliISrcImage)

        # Destination 이미지 설정 // Set destination image
        watershedsThreshold.SetDestinationImage(fliIDstImage)

        # threshold 모드 설정(Single) // Set threshold mode (Single)
        watershedsThreshold.SetThresholdMode(EThresholdMode.Single)

        # 임계값 설정 // Set threshold value
        watershedsThreshold.SetThreshold(100)

        # 논리 조건 설정 // Set logical condition
        watershedsThreshold.SetLogicalCondition(int(ELogicalCondition.Greater), EThresholdIndex.First)

        # 알고리즘 수행 // Execute algorithm
        if (res := watershedsThreshold.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Watersheds Threshold Marker.")
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
        flpPoint = CFLPoint[float](0, 0)
        if (res := layer1.DrawTextImage(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text on source layer.")
            break

        if (res := layer2.DrawTextImage(flpPoint, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text on destination layer.")
            break

        # 이미지 뷰 갱신 // Update image view
        viewImage[0].Invalidate(True)
        viewImage[1].Invalidate(True)

        # 이미지 뷰 종료될 때까지 대기 // Wait for view to close
        while viewImage[0].IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()

