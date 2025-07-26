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
    if (res := fliImage.Load("../../ExampleImages/QRCode/Plate.flif")).IsFail():
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

    # QRCode 객체 생성 # Create QRCode object
    qrcodeVerifier = CQRCodeVerifier()
    
    # 처리할 이미지 설정 # Set the image to process
    qrcodeVerifier.SetSourceImage(fliImage)

    # Decode 데이터 영역 색상 설정. EQRCodeColor.Auto 로 설정 시 자동으로 Decode 된다. # Sets the color of the decoded data region. If set to EQRCodeColor.Auto, decoding is performed automatically.
    qrcodeVerifier.SetColorMode(EDataCodeColor.WhiteOnBlack)
    
    # ISO/IEC 15415 양식 인쇄 품질 평가를 활성화합니다. 기본값은 true이며 처리하지 않아도 됩니다. # Enables ISO/IEC 15415 Form Print Quality Assessment. The default is true and does not require processing.
    qrcodeVerifier.EnablePrintQuality_ISOIEC_15415(True)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
    if (res := qrcodeVerifier.Execute()).IsFail():
        ErrorPrint(res, "Failed to Execute.")
        return

    # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
    layer = viewImage.GetLayer(0)

    i64Results = qrcodeVerifier.GetResultCount()

    for i in range(i64Results):
        # QRCode Verifier 결과를 얻어오기 위해 FLQuadD 선언 # Declare FLQuadD to retrieve the result from the QRCode Verifier.
        flqRegion = CFLQuad[Double]()

        # QRCode Verifier 결과들 중 Data Region 을 얻어옴 # Gets the Data Region from the QRCode Verifier results.
        if (res := qrcodeVerifier.GetResultDataRegion(i, flqRegion)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the data matrix decoder object.")
            return
        
        # Data Matrix Verifier 결과들 중 Grid Region 을 얻어옴
        flfaGridRegion = CFLFigureArray()

        if (res := qrcodeVerifier.GetResultGridRegion(i, flfaGridRegion)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the data matrix decoder object.")
            return
        
        strDecodedMsg = StringBuilder()
        # QRCode Verifier 결과들 중 Decoded String 을 얻어옴 # Gets the decoded string from the results of the QRCode Verifier.
        if (res := qrcodeVerifier.GetResultDecodedString(i, strDecodedMsg)[0]).IsFail():
            ErrorPrint(res, "Failed to get data region from the data matrix decoder object.")
            return
              
        print("No. {} : {}".format(i, strDecodedMsg))
        
        # QRCode의 결과를 디스플레이 한다. # Display the result of the QRCode.
        if (res := layer.DrawFigureImage(flqRegion, EColor.LIME, 2)).IsFail():
            ErrorPrint(res, "Failed to draw figure.")
            return

        if (res := layer.DrawFigureImage(flfaGridRegion, EColor.LIME, 2)).IsFail():
            ErrorPrint(res, "Failed to draw figure.")
            return

        if (res := layer.DrawTextImage(flqRegion.flpPoints[3], strDecodedMsg.ToString(), EColor.CYAN, EColor.BLACK, 20, False, flqRegion.flpPoints[3].GetAngle(flqRegion.flpPoints[2]))).IsFail():
            ErrorPrint(res, "Failed to draw string object on the image view.")
            return
        
        codeSpec = CQRCodeSpec()
        qrcodeVerifier.GetResultQRCodeSpec(i, codeSpec)

        eECLevel = codeSpec.GetQRCodeErrorCorrectionLevel()
        eSymbol1 = getattr(EQRCodeSymbolType1, "None")
        eSymbol2 = getattr(EQRCodeSymbolType2, "None")
        codeSpec.GetSymbolType(eSymbol1, eSymbol2)

        strAdditionalData = {
            EQRCodeErrorCorrectionLevel.Low: "[Low",
            EQRCodeErrorCorrectionLevel.Medium: "[Medium",
            EQRCodeErrorCorrectionLevel.Quartile: "[Quartile",
            EQRCodeErrorCorrectionLevel.High: "[High",
            }.get(eECLevel, "Other")

        if eSymbol1 != getattr(EQRCodeSymbolType1, "None"):
            i32SymbolValue = int(eSymbol1)
            i32Symbol = 0

            for j in range(20):
                if ((i32SymbolValue >> j) & 1) == 1:
                    i32Symbol = j + 1
                    break

            strAdditionalData += f"-{i32Symbol}]"
            
        if eSymbol2 != getattr(EQRCodeSymbolType2, "None"):
            i32SymbolValue = int(eSymbol2)
            i32Symbol = 0

            for j in range(20):
                if ((i32SymbolValue >> j) & 1) == 1:
                    i32Symbol = j + 21
                    break

            strAdditionalData += f"-{i32Symbol}]"

        print("No. {} : {} {}\n".format(i, strAdditionalData, strDecodedMsg))

        # Data Matrix Verifier 결과들 중 인쇄 품질을 얻어옴 # Get print quality among Data Matrix Verifier results
        printQuality = CQRCodePrintQuality_ISOIEC_15415()
        
        if (res := qrcodeVerifier.GetResultPrintQuality_ISOIEC_15415(i, printQuality)[0]).IsFail():
            ErrorPrint(res, "Failed to get print quality from the data matrix decoder object.")
            continue

        # 등급 계산이 처리되었는 지 확인
        if printQuality.IsGraded():
            strGrade = "[ISO/IEC 15415]\r\nDecoding Grade : {:.1f}\r\nAxialNonuniformity Grade : {:.1f}\r\nGridNonuniformity Grade : {:.1f}\r\nSymbolContrast Grade : {:.1f}\r\nUnusedErrorCorrection Grade : {:.1f}\r\nModulation Grade : {:.1f}\r\nFormat Information Grade : {:.1f}\r\nVersion Information Grade : {:.1f}\r\nFixedPatternDamage Grade : {:.1f}\r\nHorizontalPrintGrowth Grade : {:.1f}\r\nVerticalPrintGrowth Grade : {:.1f}\r\nOverallSymbol Grade : {:.1f}".format(printQuality.f64DecodingGrade, printQuality.f64AxialNonuniformityGrade, printQuality.f64GridNonuniformityGrade, printQuality.f64SymbolContrastGrade, printQuality.f64UnusedErrorCorrectionGrade, printQuality.f64ModulationGrade, printQuality.f64FormatInformationGrade, printQuality.f64VersionInformationGrade, printQuality.f64FixedPatternDamageGrade, printQuality.f64HorizontalPrintGrowthGrade, printQuality.f64VerticalPrintGrowthGrade, printQuality.f64OverallSymbolGrade)

            print(strGrade)

            flrBoundary = flqRegion.GetBoundaryRect()
            flpPoint = CFLPoint[Double](flrBoundary.left, flrBoundary.top)

            if (res := layer.DrawTextImage(flpPoint, strGrade, EColor.YELLOW, EColor.BLACK, 15, False, 0.0, EGUIViewImageTextAlignment.RIGHT_TOP)).IsFail():
                ErrorPrint(res, "Failed to draw string object on the image view.\n")
                continue

    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()