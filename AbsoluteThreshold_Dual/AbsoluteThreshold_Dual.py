# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
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

        # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... 형태를 반환한다.
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

        # Absolute Threshold 객체 생성 // Create Absolute Threshold object
        absoluteThreshold = CAbsoluteThreshold()

        # Source 이미지 설정 // Set source image
        absoluteThreshold.SetSourceImage(fliISrcImage)

        # Destination 이미지 설정 // Set destination image
        absoluteThreshold.SetDestinationImage(fliIDstImage)

        # threshold 모드 설정(Dual) // Set Threshold Mode(Dual)
        absoluteThreshold.SetThresholdMode(EThresholdMode.Dual_And)

        # 임계값 설정 (다채널 경우 CMultiVarD 사용) // Set threshold value (Use CMultiVarD for multi-channel)
        absoluteThreshold.SetThreshold(100, EThresholdIndex.First)
        absoluteThreshold.SetThreshold(168, EThresholdIndex.Second)

        # 논리 조건 설정 // Set condition value
        absoluteThreshold.SetLogicalCondition(int(ELogicalCondition.Greater), EThresholdIndex.First)
        absoluteThreshold.SetLogicalCondition(int(ELogicalCondition.Less), EThresholdIndex.Second)

        # 알고리즘 수행 // Execute the algorithm
        if (res := absoluteThreshold.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute AbsoluteThreshold.")
            break

        # 레이어는 따로 해제하지 않아도 View가 해제 될 때 같이 해제된다. // The layer is released together when View is released without releasing it separately.
        layer1 = viewImage[0].GetLayer(0)

        if res.IsFail():
            ErrorPrint(res, "Failed to get layer from source view.")
            break

        layer2 = viewImage[1].GetLayer(0)

        if res.IsFail():
            ErrorPrint(res, "Failed to get layer from destination view.")
            break

        # 이미지 뷰 정보 표시 // Display image view information 
        flpPoint = CFLPoint[Double](0, 0)

        # Text 출력 // Display Text
        if (res := layer1.DrawTextImage(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text on source layer.")
            break

        if (res := layer2.DrawTextImage(flpPoint, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw text on destination layer.")
            break

        # 이미지 뷰를 갱신 합니다. // Update the image view.
        viewImage[0].Invalidate(True)
        viewImage[1].Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
        while viewImage[0].IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()