# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

# 메인 함수 // Main function
def main():
    # 이미지 객체 선언 // Declare the image object
    fliImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImage = CGUIViewImage()
    res = CResult()

    # 이미지 로드 // Load image
    if (res := fliImage.Load("../../ExampleImages/ShapeMatch/Cross_Dark.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.")
        return

    # 이미지 뷰 생성 // Create image view
    if (res := viewImage.Create(200, 0, 968, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    # 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
    if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.")
        return

    # Image 크기에 맞게 view의 크기를 조정 // Zoom the view to fit the image size
    if (res := viewImage.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit")
        return
    
    # Shape Match 객체 생성 // Create Shape Match object
    shapeMatch = CShapeMatchFigure()
    
    # 학습할 도형 설정 // Set figure to learn
    flrgObject = CFLRegion()
    flrgObject.Load("../../ExampleImages/ShapeMatch/Figure Object")
    shapeMatch.SetFigureObject(flrgObject)

    # 검출할 객체의 색상을 설정합니다. // Sets the color of the object to be detected.
    shapeMatch.SetObjectColor(EShapeMatchObjectColor.Dark)
    
    # 도형 학습 // Learn shape
    if (res := shapeMatch.Learn()).IsFail():
        ErrorPrint(res, "Failed to Learn.")
        return

    # 처리할 이미지 설정 // Set the image to process
    shapeMatch.SetSourceImage(fliImage)

    # 검출 시 사용될 유효 변경 크기범위를 설정합니다. // Set the effective change size range to be used for detection.
    shapeMatch.SetScaleRange(0.9, 1.1)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
    if (res := shapeMatch.Execute()).IsFail():
        ErrorPrint(res, "Failed to Execute.")
        return

    # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
    layer = viewImage.GetLayer(0)

    i64ResultCount = shapeMatch.GetResultCount()

    for i in range(i64ResultCount):
        matchResult = CShapeMatchFigureResult()
        shapeMatch.GetResult(i, matchResult)

        # 도형 검출 결과를 Console창에 출력합니다. // Output the shape detection result to the console window.
        print(" < Instance : {} >".format(i))
        print("  1. Shape Type : Region")
        print("    Pivot X: {:.2f}".format(matchResult.flpPivot.x))
        print("    Pivot Y: {:.2f}".format(matchResult.flpPivot.y))
        print("  2. Score : {:.2f}\n  3. Scale : {:.2f}\n".format(matchResult.f32Score, matchResult.f32Scale))
        
        # Image View 결과 출력        
        if (res := layer.DrawFigureImage(matchResult.flfaResultObject, EColor.CYAN, 3)).IsFail():
            ErrorPrint(res, "Failed to draw figure.")
            return
           
        strText = "Score : {:.2f}\nScale : {:.2f}\nPivot : ({:.2f}, {:.2f})".format(matchResult.f32Score, matchResult.f32Scale, matchResult.flpPivot.x, matchResult.flpPivot.y)

        if (res := layer.DrawTextImage(matchResult.flpPivot, strText, EColor.YELLOW, EColor.BLACK, 15)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            return

    # 이미지 뷰를 갱신 합니다. // Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()