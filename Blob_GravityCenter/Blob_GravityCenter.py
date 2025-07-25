# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

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
    if (res := fliImage.Load("../../ExampleImages/Blob/AlignBall.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 # Create image view
    if (res := viewImage.Create(200, 0, 968, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.\n")
        return

    # 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
    if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return

    # Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
    if (res := viewImage.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit\n")
        return

    # Blob 객체 생성 # Create Blob object
    blob = CBlob()

    # 처리할 이미지 설정 # Set the image to process
    blob.SetSourceImage(fliImage)
    
    # 논리 조건 설정
    blob.SetLogicalCondition(ELogicalCondition.Less)

    # 임계값 설정,  위의 조건과 아래의 조건이 합쳐지면 50보다 작은 객체를 검출
    blob.SetThreshold(50)
        
    # Blob Result Type mask 생성 (Contour, GravityCenter)
    resultTypeMask = Enum.ToObject(CBlob.EBlobResultType, int(CBlob.EBlobResultType.Contour) | int(CBlob.EBlobResultType.GravityCenter))

    # Result Type 설정
    blob.SetResultType(resultTypeMask)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
    if (res := blob.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute Blob.")
        return
    
    # BoundaryRect의 20보다 작은 너비를 가진 객체들을 제거
    if (res := blob.Filter(CBlob.EFilterItem.BoundaryRectWidth, 20, ELogicalCondition.Less)).IsFail():
        ErrorPrint(res, "Blob filtering algorithm error occurred.")
        return
    
    # BoundaryRect의 20보다 작은 높이를 가진 객체들을 제거
    if (res := blob.Filter(CBlob.EFilterItem.BoundaryRectHeight, 20, ELogicalCondition.Less)).IsFail():
        ErrorPrint(res, "Blob filtering algorithm error occurred.")
        return
    
    # Blob 결과를 얻어오기 위해 FigureArray 선언
    flfaContours = CFLFigureArray()
    flfGravityCenter = CFLFigureArray()

    # Blob 결과들 중 Contours를 얻어옴
    if (res := blob.GetResultContours(flfaContours)[0]).IsFail():
        ErrorPrint(res, "Failed to get contours from the Blob object.")
        return
    
    # Blob 결과들 중 Gravity Center 를 얻어옴
    if (res := blob.GetResultGravityCenters(flfGravityCenter)[0]).IsFail():
        ErrorPrint(res, "Failed to get contours from the Blob object.")
        return

    # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
    layer = viewImage.GetLayer(0)

    # 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
    layer.Clear()

    # flfaContours 는 Figure들의 배열이기 때문에 Layer에 넣기만 해도 모두 드로윙이 가능하다.
    # 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 # The function DrawFigureImage below means drawing a picture based on the image coordinates
    # 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. # The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
    # 여기서 0.25이므로 옅은 반투명 상태라고 볼 수 있다.
    # 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) # Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
    if (res := layer.DrawFigureImage(flfaContours, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, .25)).IsFail():
        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
        return

    # Image View 객체에 Index 출력
    for i in range(flfaContours.GetCount()):
        flpContoursCenter = CFLPoint[Double](flfaContours.GetAt(i));
        flpfGravityCenter = CFLPoint[Double](flfGravityCenter.GetAt(i));
        flfCrossHair = CFLFigureArray();

        flfCrossHair = flpfGravityCenter.MakeCrossHair(10, True);

        # Image View 출력
        strIndex = "[{}]\n\n\n\n".format(i)
        strTextResult = "\n\n\n\n\n\nGravity Center\nX : {:.2f} Y : {:.2f}".format(flpfGravityCenter.x, flpfGravityCenter.y)

        layer.DrawTextImage(flpContoursCenter, strIndex, EColor.LIME, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER)
        layer.DrawTextImage(flpContoursCenter, strTextResult, EColor.YELLOW, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER)
        layer.DrawFigureImage(flfCrossHair, EColor.ORANGERED, 1, EColor.ORANGERED, EGUIViewImagePenStyle.Solid, 1, 0.25)

        # 콘솔에 출력
        print("[{}] Gravity Center x : {:.2f}\ty : {:.2f} \n".format(i, flpfGravityCenter.x, flpfGravityCenter.y))
        

    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()