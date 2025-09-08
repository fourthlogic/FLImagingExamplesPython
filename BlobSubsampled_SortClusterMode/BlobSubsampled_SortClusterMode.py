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
    viewIndex = ["Src0", "Src1", "Src2", "Src3"]


    # 이미지 객체 선언 # Declare the image object
    arrImage = [CFLImage() for v in viewIndex]

    # 이미지 뷰 선언 # Declare the image view
    arrViewImage = [CGUIViewImage() for v in viewIndex]
    res = CResult()
    
    # 이미지 로드 # Load image
    for i in range(len(viewIndex)):
        arrImage[i].Load("../../ExampleImages/Blob/Blob Sort {}.flif".format(i + 1))
        
        x = i % 2
        y = int(i / 2)

        # 이미지 뷰 생성 # Create image view
        if (res := arrViewImage[i].Create(x * 400 + 400, y * 400, x * 400 + 400 + 400, y * 400 + 400)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            return
    
        # 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
        if (res := arrViewImage[i].SetImagePtr(arrImage[i])[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            return
    
        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        if i != 0:
            if (res := arrViewImage[0].SynchronizePointOfView(arrViewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                return

        # Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
        if (res := arrViewImage[i].ZoomFit()).IsFail():
            ErrorPrint(res, "Failed to zoom fit\n")
            return
    
    for k in range(len(viewIndex)):
        # Blob subsampled 객체 생성 # Create Blob subsampled object
        blobSubsampled = CBlobSubsampled()

        # 처리할 이미지 설정 # Set the image to process
        blobSubsampled.SetSourceImage(arrImage[k])
    
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
    
        # Blob 결과를 얻어오기 위한 객체 선언 # Declare an object to retrieve Blob results
        flfaSortClusterModeBoundaryRects = CFLFigureArray()
    
        # 우선순위를 y, x축 순서로 클러스터 정렬 # Sort clusters by Y-axis first, then by X-axis
        if (res := blobSubsampled.SortClusterMode(CBlob.ESortClusterModeMethod.Center_Y_Asc_X_Asc)).IsFail():
            ErrorPrint(res, "Failed to sort from the Blob object.")
            return
    
        # Blob 결과들 중 Boundary Rect를 얻어옴 # Get boundary rect from the set of Blob results
        if (res := blobSubsampled.GetResultBoundaryRects(flfaSortClusterModeBoundaryRects)[0]).IsFail():
            ErrorPrint(res, "Failed to get boundary rects from the Blob object.")
            return
    
        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        layer = arrViewImage[k].GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
        layer.Clear()
    
        flp = CFLPoint[Double]()

        if (res := layer.DrawTextCanvas(flp, ("SortClusterMode (Y Asc, X Asc)"), EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text on the image view.\n")
            return

        # flfaSortClusterModeBoundaryRects 는 Figure들의 배열이기 때문에 Layer에 넣기만 해도 모두 드로윙이 가능하다.
        # 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 # The function DrawFigureImage below means drawing a picture based on the image coordinates
        # 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. # The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
        # 여기서 0.25이므로 옅은 반투명 상태라고 볼 수 있다.
        # 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) # Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
        if (res := layer.DrawFigureImage(flfaSortClusterModeBoundaryRects, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1.0, .25)).IsFail():
            ErrorPrint(res, "Failed to draw figure objects on the image view.\n")
            return
        
        # Image View에 정보 출력 # Display information on the Image View
        for i in range(flfaSortClusterModeBoundaryRects.GetCount()):           
            if isinstance(flfaSortClusterModeBoundaryRects.GetAt(i), CFLFigureArray):
                flfaCluster = flfaSortClusterModeBoundaryRects.GetAt(i)
            else:
                flfaCluster = None

            if flfaCluster is not None:
                for j in range(flfaCluster.GetCount()):
                    if isinstance(flfaCluster.GetAt(j), CFLRect[Double]):
                        flrRect = flfaCluster.GetAt(j)
                    else:
                        flrRect = None

                    if flrRect is not None:
                        print("Recover No. [{}][{}] : ({},{},{},{})".format(i, j, flrRect.left, flrRect.top, flrRect.right, flrRect.bottom))

                    layer.DrawTextImage(flrRect.GetCenter(), f"({i},{j})", EColor.CYAN, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER)


        # 이미지 뷰를 갱신 합니다. # Update image view
        arrViewImage[k].Invalidate()

    bAvailable = True

    while bAvailable:
        for i in range(len(viewIndex)):
            bAvailable &= arrViewImage[i].IsAvailable()

        CThreadUtilities.Sleep(1)


if __name__ == "__main__":
    main()