# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

# 메인 함수 # Main function
def main():
    # 이미지 객체 선언 # Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 # Declare the image view
    viewImage = CGUIViewImage()
    res = CResult()

    # 이미지 로드 # Load image
    if (res := fliImage.Load("../../ExampleImages/UnifiedDataCode/FLImaging.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.")
        return

    # 이미지 뷰 생성 # Create image view
    if (res := viewImage.Create(200, 0, 968, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    # 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
    if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        return

    # Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
    if (res := viewImage.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit")
        return

    # UnifiedDataCode 객체 생성 # Create UnifiedDataCode object
    qrcodeDecoder = CUnifiedDataCodeDecoder()
    
    # 처리할 이미지 설정 # Set the image to process
    qrcodeDecoder.SetSourceImage(fliImage)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
    if (res := qrcodeDecoder.Execute()).IsFail():
        ErrorPrint(res, "Failed to Execute.")
        return

    # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
    layer = viewImage.GetLayer(0)

    i64Results = qrcodeDecoder.GetResultCount()

    for i in range(i64Results):
        # UnifiedDataCode Decoder 결과를 얻어오기 위해 FLQuadD 선언 # Declare FLQuadD to retrieve the result from the UnifiedDataCode Decoder.
        flqRegion = CFLQuad[Double]()

        # UnifiedDataCode Decoder 결과들 중 Data Region 을 얻어옴 # Gets the Data Region from the UnifiedDataCode Decoder results.
        if (res := qrcodeDecoder.GetResultDataRegion(i, flqRegion)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the data matrix decoder object.")
            return
        
        strDecodedMsg = StringBuilder()
        # UnifiedDataCode Decoder 결과들 중 Decoded String 을 얻어옴 # Gets the decoded string from the results of the UnifiedDataCode Decoder.
        if (res := qrcodeDecoder.GetResultDecodedString(i, strDecodedMsg)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the data matrix decoder object.")
            return
              
        print("No. {} : {}".format(i, strDecodedMsg))
        
        # UnifiedDataCode의 결과를 디스플레이 한다. # Display the result of the UnifiedDataCode.
        if (res := layer.DrawFigureImage(flqRegion, EColor.LIME, 2)).IsFail():
            ErrorPrint(res, "Failed to draw figure.")
            return

        if (res := layer.DrawTextImage(flqRegion.flpPoints[3], strDecodedMsg.ToString(), EColor.CYAN, EColor.BLACK, 20, False, flqRegion.flpPoints[3].GetAngle(flqRegion.flpPoints[2]))).IsFail():
            ErrorPrint(res, "Failed to draw string object on the image view.")
            return

    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()