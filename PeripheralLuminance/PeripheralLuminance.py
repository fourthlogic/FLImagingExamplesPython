# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 에러 출력 함수 // Error print function
def ErrorPrint(res: CResult, msg: str):
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
    input()


# 메인 함수 // Main function
def main():
    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImage = CGUIViewImage()

    while True:
        # 이미지 로드 // Load image
        if (res := fliImage.Load("../../ExampleImages/PeripheralLuminance/Bolt.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImage.Create(400, 0, 912, 612)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
        if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        # PeripheralLuminance 객체 생성 // Create PeripheralLuminance object
        peripheralLuminance = CPeripheralLuminance()

        # 측정 영역 피겨 배열 선언 // Declare figure array for measurement region
        flfaMeasurementRegion = CFLFigureArray()

        # 피겨 파일 로드 // Load figure file
        if (res := flfaMeasurementRegion.Load("../../ExampleImages/PeripheralLuminance/Measurement Region.fig")).IsFail():
            ErrorPrint(res, "Failed to execute Peripheral Luminance.")
            break

        # Source 이미지 설정 // Set the Source Image
        peripheralLuminance.SetSourceImage(fliImage)
        # Measurement Region 설정 // Set the Measurement Region
        peripheralLuminance.SetMeasurementRegion(flfaMeasurementRegion)
        # Thickness 설정 // Set Thickness
        peripheralLuminance.SetThickness(2.0)

        # 알고리즘 수행 // Execute the algorithm
        if (res := peripheralLuminance.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Peripheral Luminance.")
            break

        # 결과값을 받아올 List 컨테이너 생성 // Create the List object to push the result
        listResult = List[Double]()

        # 결과 가져오기 // Get results
        if (res := peripheralLuminance.GetResult(listResult)[0]).IsFail():
            ErrorPrint(res, "No Result")
            break

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
        layer = viewImage.GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
        layer.Clear()

        # 결과를 순회하며 출력 // Loop through results and display
        for i32Idx in range(len(listResult)):
            pflfSrc = flfaMeasurementRegion.GetAt(i32Idx)
            strText = "{0:.9f}".format(listResult[i32Idx])  # 소수점 9자리까지 출력 // Print up to 9 decimal places

            # 측정 영역이 어디인지 알기 위해 디스플레이 한다 // Display to show measurement region
            if (res := layer.DrawFigureImage(pflfSrc, EColor.LIME, 1, EColor.LIME, EGUIViewImagePenStyle.Solid, 0.3, 0.3)).IsFail():
                ErrorPrint(res, "Failed to draw Figure\n")
                break

            # 이미지 뷰 정보 표시 // Display image view information
            if (res := layer.DrawTextImage(pflfSrc, strText, EColor.YELLOW, EColor.BLACK, 13, False, 0.0, EGUIViewImageTextAlignment.LEFT_TOP)).IsFail():
                ErrorPrint(res, "Failed to draw text\n")
                break

        # 이미지 뷰를 갱신 합니다. // Update image view
        viewImage.Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
        while viewImage.IsAvailable():
            CThreadUtilities.Sleep(1)

        break


if __name__ == "__main__":
    main()
