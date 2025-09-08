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
    viewImageRecover = CGUIViewImage()
    res = CResult()

    # 이미지 로드 # Load image
    if (res := fliImage.Load("../../ExampleImages/Blob/Ball.flif")).IsFail():
        ErrorPrint(res, "Failed to load the image file.\n")
        return

    # 이미지 뷰 생성 # Create image view
    if (res := viewImage.Create(200, 0, 968, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.\n")
        return
    
    if (res := viewImageRecover.Create(968, 0, 1736, 576)).IsFail():
        ErrorPrint(res, "Failed to create the image view.\n")
        return

    # 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
    if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return

    if (res := viewImageRecover.SetImagePtr(fliImage)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return
    
    # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
    if (res := viewImage.SynchronizePointOfView(viewImageRecover)[0]).IsFail():
        ErrorPrint(res, "Failed to set image object on the image view.\n")
        return

    # Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
    if (res := viewImage.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit\n")
        return

    if (res := viewImageRecover.ZoomFit()).IsFail():
        ErrorPrint(res, "Failed to zoom fit\n")
        return

    # Blob subsampled 객체 생성 # Create Blob subsampled object
    blobSubsampled = CBlobSubsampled()

    # 처리할 이미지 설정 # Set the image to process
    blobSubsampled.SetSourceImage(fliImage)
    
    # ROI 범위 설정
    flrROI = CFLRect[Double](450, 425, 1024, 800)

    # 처리할 ROI 설정
    blobSubsampled.SetSourceROI(flrROI)
    
    # 논리 조건 설정 # Set logical conditions
    blobSubsampled.SetLogicalCondition(ELogicalCondition.GreaterEqual)
    
    # 임계값 설정  위의 조건과 아래의 조건이 합쳐지면 100이상 객체를 검출 # Set a threshold: detect objects when the combined result of the above and below conditions is greater than or equal to 100.
    blobSubsampled.SetThreshold(100)

    # Subsampling 수준 설정 # Set Subsampling Level
    blobSubsampled.SetSubsamplingLevel(3)

    # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
    if (res := blobSubsampled.Execute()).IsFail():
        ErrorPrint(res, "Failed to execute Blob.")
        return
    
	# 50보다 같거나 큰 장변 길이를 가진 객체들을 제거 # Filter out objects with a major axis length equal to or exceeding 50
    if (res := blobSubsampled.Filter(CBlob.EFilterItem.BoundaryRectWidth, 50, ELogicalCondition.GreaterEqual)).IsFail():
        ErrorPrint(res, "Blob filtering algorithm error occurred.")
        return
    
	# 50보다 같거나 큰 단변 길이를 가진 객체들을 제거 # Filter out objects with a minor axis length equal to or exceeding 50
    if (res := blobSubsampled.Filter(CBlob.EFilterItem.BoundaryRectHeight, 50, ELogicalCondition.GreaterEqual)).IsFail():
        ErrorPrint(res, "Blob filtering algorithm error occurred.")
        return

    # 면적이 50보다 작은 객체들을 제거 # Filter out objects whose area is smaller than 50
    if (res := blobSubsampled.Filter(CBlob.EFilterItem.Area, 50, ELogicalCondition.LessEqual)).IsFail():
        ErrorPrint(res, "Blob filtering algorithm error occurred.")
        return
    
    # Blob 결과를 얻어오기 위한 객체 선언 # Declare an object to retrieve Blob results
    flfaSortedBoundaryRects = CFLFigureArray()
    flfaRecoverBoundaryRects = CFLFigureArray()
    
    flaItem = List[Int32]()
    flaOrder = List[Int32]()
    
    # 첫 번째 조건을 Bound rect center y좌표, 내림차순 정렬 # Sort by the Y-coordinate of the bounding rectangle center in descending order as the primary condition
    flaItem.Add(int(CBlob.EFilterItem.BoundaryRectCenterY))
    flaOrder.Add(int(CBlob.EOrder.Descending))

    # 두 번째 조건을 Bound rect center x좌표, 내림차순 정렬 # Sort by the X-coordinate of the bounding rectangle center in descending order as the second condition
    flaItem.Add(int(CBlob.EFilterItem.BoundaryRectCenterX))
    flaOrder.Add(int(CBlob.EOrder.Descending))
    
    # Blob 결과를 정렬 # Sort the Blob results
    if (res := blobSubsampled.Sort(flaItem, flaOrder)).IsFail():
        ErrorPrint(res, "Failed to sort from the Blob object.")
        return
    
    # Blob 결과들 중 Boundary Rect를 얻어옴 # Get boundary rect from the set of Blob results
    if (res := blobSubsampled.GetResultBoundaryRects(flfaSortedBoundaryRects)[0]).IsFail():
        ErrorPrint(res, "Failed to get boundary rects from the Blob object.")
        return
    
    # Blob 정렬 상태를 초기 상태로 복구 # Restore the Blob results to their initial order
    if (res := blobSubsampled.Sort(CBlob.EFilterItem.Unselected, CBlob.EOrder.Ascending)).IsFail():
        ErrorPrint(res, "Failed to sort from the Blob object.")
        return
    
    # 복구된 Blob 결과들 중 Boundary Rectangle 을 얻어옴 # Get the bounding rectangles of the restored Blob results
    if (res := blobSubsampled.GetResultBoundaryRects(flfaRecoverBoundaryRects)[0]).IsFail():
        ErrorPrint(res, "Failed to get boundary rects from the Blob object.")
        return
    
    # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
    # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
    layer = viewImage.GetLayer(0)
    layerRecover = viewImageRecover.GetLayer(0)

    # 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
    layer.Clear()
    layerRecover.Clear()
    
    flp = CFLPoint[Double]()

    if (res := layer.DrawTextCanvas(flp, ("Sort"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text on the image view.\n")
        return

    if (res := layerRecover.DrawTextCanvas(flp, ("No Sort"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
        ErrorPrint(res, "Failed to draw text on the image view.\n")
        return

    # ROI영역이 어디인지 알기 위해 디스플레이 한다 # Display to find out where ROI is
    # FLImaging의 Figure객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능
    if (res := layer.DrawFigureImage(flrROI, EColor.BLUE)).IsFail():
        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
        return

    if (res := layerRecover.DrawFigureImage(flrROI, EColor.BLUE)).IsFail():
        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
        return

    # flfaSortedBoundaryRects 는 Figure들의 배열이기 때문에 Layer에 넣기만 해도 모두 드로윙이 가능하다.
    # 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 # The function DrawFigureImage below means drawing a picture based on the image coordinates
    # 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. # The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
    # 여기서 0.25이므로 옅은 반투명 상태라고 볼 수 있다.
    # 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) # Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
    if (res := layer.DrawFigureImage(flfaSortedBoundaryRects, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, .25)).IsFail():
        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
        return

    if (res := layerRecover.DrawFigureImage(flfaRecoverBoundaryRects, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, .25)).IsFail():
        ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
        return
    
    # Image View에 정보 출력 # Display information on the Image View
    for i in range(flfaSortedBoundaryRects.GetCount()):           
        if isinstance(flfaSortedBoundaryRects.GetAt(i), CFLRect[Double]):
            flrSortedRect = flfaSortedBoundaryRects.GetAt(i)
        else:
            flrSortedRect = None

        if flrSortedRect is not None:
            print("Sorted No. {} : ({},{},{},{})".format(i, flrSortedRect.left, flrSortedRect.top, flrSortedRect.right, flrSortedRect.bottom))

        layer.DrawTextImage(flrSortedRect.GetCenter(), f"{i}", EColor.CYAN)

        if isinstance(flfaRecoverBoundaryRects.GetAt(i), CFLRect[Double]):
            flrRect = flfaRecoverBoundaryRects.GetAt(i)
        else:
            flrRect = None

        if flrRect is not None:
            print("Sorted No. {} : ({},{},{},{})".format(i, flrRect.left, flrRect.top, flrRect.right, flrRect.bottom))

        layerRecover.DrawTextImage(flrRect.GetCenter(), f"{i}", EColor.CYAN)


    # 이미지 뷰를 갱신 합니다. # Update image view
    viewImage.Invalidate()
    viewImageRecover.Invalidate()

    while viewImage.IsAvailable() & viewImageRecover.IsAvailable():
        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()