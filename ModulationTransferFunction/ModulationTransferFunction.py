from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 정의 // Error print function definition
def ErrorPrint(res: CResult, msg: str):
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
    input()

def main():
    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImage = CGUIViewImage()

    res = CResult()

    while True:
        # 이미지 로드 // Load image
        if (res := fliImage.Load("../../ExampleImages/ModulationTransferFunction/ISO12233Crop.flif")).IsFail():
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

        # ModulationTransferFunction 객체 생성 // Create ModulationTransferFunction object
        modulationTransferFunction = CModulationTransferFunction()

        # ROI 범위 설정 // Set the ROI value
        flfSourceROI = CFLRect[Double](349.0, 43.0, 396.0, 85.0)

        # Source 이미지 설정 // Set the Source Image
        modulationTransferFunction.SetSourceImage(fliImage)
        # Source ROI 설정 // Set the Source ROI
        modulationTransferFunction.SetSourceROI(flfSourceROI)

        # 알고리즘 수행 // Execute the algorithm
        if (res := modulationTransferFunction.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Modulation Transfer Function.")
            break

        # 결과값을 받아올 List 컨테이너 생성 // Create the List object to push the result
        listMTF = List[Double]()

        # 이미지 전체(혹은 ROI 영역) 픽셀값의 MTF를 구하는 함수 // Function that calculates MTF of the image (or the region of ROI)
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
        if (res := modulationTransferFunction.GetResults(listMTF)[0]).IsFail():
            ErrorPrint(res, "No Result")
            break

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
        layer = viewImage.GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
        layer.Clear()

        # ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
        if (res := layer.DrawFigureImage(flfSourceROI, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")

        strText = ""

        for i32PageIdx in range(len(listMTF)):
            #strText += f"Page.No {i32PageIdx} "
            strText += f"MTF {listMTF[i32PageIdx]:.9f} "
            #strText += "\n\n"

        print(strText)
        flpPoint = CFLPoint[Double](0, 0)

        # 이미지 뷰 정보 표시 // Display image view information
        if (res := layer.DrawTextCanvas(flpPoint, strText, EColor.YELLOW, EColor.BLACK, 25)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        # 이미지 뷰를 갱신 합니다. // Update image view
        viewImage.Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
        while viewImage.IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == '__main__':
    main()
