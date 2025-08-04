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
    
    # 논리 조건 설정 # Set logical conditions
    blob.SetLogicalCondition(ELogicalCondition.Less)
    
    # 임계값 설정  위의 조건과 아래의 조건이 합쳐지면 50보다 작은 객체를 검출 # Set a threshold: detect objects when the combined result of the above and below conditions is less than 50.
    blob.SetThreshold(50)
        
    # Blob Result Type mask 생성 (Contour, Circularity) # Generate a mask of Blob result type (Contour, Circularity)
    resultTypeMask = Enum.ToObject(CBlob.EBlobResultType, int(CBlob.EBlobResultType.Contour) | int(CBlob.EBlobResultType.Circularity))
    
    # 결과 타입 설정 # Set result type
    blob.SetResultType(resultTypeMask)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
    if (res := blob.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute Blob.")
        return
    
    # Circularity가 0.85 보다 작은 객체들을 제거(원형에 가깝지 않은 객체 제거, 최대값 : 1.0) # Remove objects with circularity less than 0.85 (filtering out objects that are not close to circular, max value: 1.0)
    if (res := blob.Filter(CBlob.EFilterItem.Circularity, 0.85, ELogicalCondition.Less)).IsFail():
        ErrorPrint(res, "Blob filtering algorithm error occurred.")
        return
    
    # Blob 결과를 얻어오기 위한 객체 선언 # Declare an object to retrieve Blob results
    flfaContours = CFLFigureArray()
    flaCircularity = List[Double]();
    
    # Blob 결과들 중 Contours 을 얻어옴 # Get contours from the set of Blob results
    if (res := blob.GetResultContours(flfaContours)[0]).IsFail():
        ErrorPrint(res, "Failed to get contours from the Blob object.")
        return
    
    # Blob 결과들 중 Circularity 을 얻어옴 # Get circularity from the set of Blob results
    if (res := blob.GetResultCircularities(flaCircularity)[0]).IsFail():
        ErrorPrint(res, "Failed to get circularity from the Blob object.")
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
    
    # Image View에 정보 출력 # Display information on the Image View
    for i in range(flfaContours.GetCount()):
        
        strIndex = f"[{i}]\n"
        flsTextResult = f"\nCircularity {flaCircularity[i]:.2f}"

        flpCenter = CFLPoint[Double](flfaContours.GetAt(i));

        # Image View 결과 출력
        layer.DrawTextImage(flpCenter, strIndex, EColor.LIME, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER);
        layer.DrawTextImage(flpCenter, flsTextResult, EColor.YELLOW, EColor.BLACK, 10, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER);

        # 콘솔 결과 출력
        print(f"[{i}] Circularity {flaCircularity[i]:.2f}\n")


    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()

    while viewImage.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()