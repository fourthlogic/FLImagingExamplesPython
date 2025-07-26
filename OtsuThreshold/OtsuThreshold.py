# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

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
        if (res := fliISrcImage.Load("../../ExampleImages/Threshold/BallChip.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 뷰 시점 동기화 // Synchronize viewpoints
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

        # Otsu Threshold 객체 생성 // Create Otsu Threshold object
        otsuThreshold = COtsuThreshold()

        # Source 이미지 설정 // Set source image
        otsuThreshold.SetSourceImage(fliISrcImage)

        # Destination 이미지 설정 // Set destination image
        otsuThreshold.SetDestinationImage(fliIDstImage)

        # 논리 조건 설정 // Set condition value
        otsuThreshold.SetLogicalCondition(int(ELogicalCondition.Greater))

        # Threshold 값 추출 // Extract threshold value
        mvThreshold = otsuThreshold.GetResultThreshold()
        print(f"Result Threshold : {int(mvThreshold.GetAt(0))}")

        # 알고리즘 수행 // Execute algorithm
        if (res := otsuThreshold.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute OtsuThreshold.")
            break

        # 레이어 가져오기 // Get image layers
        layer1 = viewImage[0].GetLayer(0)
        layer2 = viewImage[1].GetLayer(0)
        flpPrint = CFLPoint[Double](0, 0)

        # Text 출력 // Display text
        if (res := layer1.DrawTextImage(flpPrint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        if (res := layer2.DrawTextImage(flpPrint, f"Destination Image( {int(mvThreshold.GetAt(0))} < threshold)", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        # 이미지 뷰 갱신 // Update image view
        viewImage[0].Invalidate(True)
        viewImage[1].Invalidate(True)

        # 이미지 뷰 종료될 때까지 대기 // Wait for the image view to close
        while viewImage[0].IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()