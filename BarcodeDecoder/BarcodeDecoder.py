# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

clr.AddReference("mscorlib")
from System.Text import StringBuilder

# 메인 함수 # Main function
def main():
    # 이미지 객체 선언 # Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 # Declare the image view
    viewImage = CGUIViewImage()
    res = CResult()

    # 이미지 로드 # Load image
    if (res := fliImage.Load("../../ExampleImages/Barcode/Barcode.flif")).IsFail():
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

    # Barcode 객체 생성 # Create Barcode object
    barcode = CBarcodeDecoder()
    
    # 처리할 이미지 설정 # Set the image to process
    barcode.SetSourceImage(fliImage)

    # Barcode 타입 설정. 미 설정시 EBarcodeDecodingType.Auto 로 모든 심볼을 탐색한다 동작한다. # Specifies the barcode type. If not set, all barcode symbols will be scanned using EBarcodeDecodingType.Auto
    barcode.SetSymbolType(EBarcodeSymbolType.EAN13)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
    if (res := barcode.Execute()).IsFail():
        ErrorPrint(res, "Failed to Execute.")
        return

    # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
    layer = viewImage.GetLayer(0)

    i64Results = barcode.GetResultCount()

    for i in range(i64Results):
        # Barcode Decoder 결과를 얻어오기 위해 FLQuadD 선언 # Declare FLQuadD to retrieve the result from the Barcode Decoder.
        flqRegion = CFLQuad[Double]()

        # Barcode Decoder 결과들 중 Data Region 을 얻어옴 # Gets the Data Region from the Barcode Decoder results.
        if (res := barcode.GetResultDataRegion(i, flqRegion)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the barcode decoder object.")
            return
                      
        strDecodedMsg = StringBuilder()
        # Barcode Decoder 결과들 중 Decoded String 을 얻어옴 # Gets the decoded string from the results of the Barcode Decoder.
        if (res := barcode.GetResultDecodedString(i, strDecodedMsg)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the barcode decoder object.")
            return
              
        bcs = CBarcodeSpec()
        barcode.GetResultBarcodeSpec(i, bcs)
        
        eSymbol = bcs.GetSymbolType()

        strSymbol = {
            EBarcodeSymbolType.CODE11: "[CODE-11]",
            EBarcodeSymbolType.CODE39: "[CODE-39]",
            EBarcodeSymbolType.Codabar: "[Codabar]",
            EBarcodeSymbolType.Datalogic2Of5: "[Datalogic 2/5]",
            EBarcodeSymbolType.Interleaved2Of5: "[Interleaved 2/5]",
            EBarcodeSymbolType.Industrial2Of5: "[Industrial 2/5]",
            EBarcodeSymbolType.MSI: "[MSI]",
            EBarcodeSymbolType.Plessey: "[Plessy UK]",
            EBarcodeSymbolType.UPCA: "[UPC-A]",
            EBarcodeSymbolType.UPCE: "[UPC-E]",
            EBarcodeSymbolType.EAN8: "[EAN-8]",
            EBarcodeSymbolType.EAN13: "[EAN-13]",
            EBarcodeSymbolType.EAN128: "[EAN-128]",
            EBarcodeSymbolType.CODE93: "[CODE-93]",
            EBarcodeSymbolType.GS1DatabarOmniTrunc: "[GS1 Databar Omni-Trunc]",
            EBarcodeSymbolType.GS1DatabarLimited: "[GS1 Databar Limited]",
            EBarcodeSymbolType.GS1DatabarExpanded: "[GS1 Databar Expanded]",
            EBarcodeSymbolType.USPSIntelligent: "[USPS Intelligent]",
            EBarcodeSymbolType.JapanesePostalCustomer: "[Japanese Postal Customer]",
        }.get(eSymbol, "Other")

        print("No. {} Code : {} {}\n".format(i, strSymbol, strDecodedMsg))
        
        # Barcode의 결과를 디스플레이 한다. # Display the result of the barcode.
        if (res := layer.DrawFigureImage(flqRegion, EColor.LIME, 2, EColor.TRANSPARENCY, EGUIViewImagePenStyle.Solid, 1.0, 0.0)).IsFail():
            ErrorPrint(res, "Failed to draw figure.")
            return

        if (res := layer.DrawTextImage(flqRegion.flpPoints[0], strSymbol, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
            ErrorPrint(res, "Failed to draw string object on the image view.")
            return

        if (res := layer.DrawTextImage(flqRegion.flpPoints[3], strDecodedMsg.ToString(), EColor.CYAN, EColor.BLACK, 20)).IsFail():
            ErrorPrint(res, "Failed to draw string object on the image view.")
            return

    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()