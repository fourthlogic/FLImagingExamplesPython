# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    # 이미지 객체 선언 # Declare the image object
    fliSrcImage = CFLImage()
    fliMaskImage = CFLImage()

    # 이미지 뷰 선언 # Declare the image view
    viewImageSrc = CGUIViewImage()
    viewImageMask = CGUIViewImage()

    while True:
        # Source 이미지 로드 # Load the source image
        if (res := fliSrcImage.Load("../../ExampleImages/Mask/ChessBoard.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # 원본 이미지와의 결과 비교를 위해 이미지를 복사 # Copy the image to compare the result with the original image
        if (res := fliMaskImage.Assign(fliSrcImage)).IsFail():
            ErrorPrint(res, "Failed to assign the image file.\n")
            break

        # Source 이미지 뷰 생성 # Create the source image view
        if (res := viewImageSrc.Create(400, 0, 912, 612)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
        if (res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        # Mask 이미지 뷰 생성 # Create mask image view
        if (res := viewImageMask.Create(912, 0, 1424, 612)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # Mask 이미지 뷰에 이미지를 디스플레이 # Display the image in the Mask image view
        if (res := viewImageMask.SetImagePtr(fliMaskImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            break

        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        if (res := viewImageSrc.SynchronizePointOfView(viewImageMask)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        # 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
        if (res := viewImageSrc.SynchronizeWindow(viewImageMask)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
        if (res := viewImageSrc.ZoomFit()).IsFail():
            ErrorPrint(res, "Failed to zoom fit\n")
            break

        # Blob 객체 생성 # Create Blob object
        blob = CBlob()

        # 처리할 이미지 설정 # Set the image to process
        if (res := blob.SetSourceImage(fliSrcImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set source image.\n")
            break

        # Threshold 모드 설정. 여기서는 2중 Threshold에 두개의 조건의 And 조건을 참으로 설정한다.
        # Threshold mode setting. Here, set the AND condition of the two conditions to true in the double threshold.
        blob.SetThresholdMode(EThresholdMode.Dual_And)
        # 논리 조건 설정 # Set logical condition
        # blob.SetLogicalCondition(ELogicalCondition.Greater, EThresholdIndex.First)
        # blob.SetLogicalCondition(ELogicalCondition.Less, EThresholdIndex.Second)
        blob.SetLogicalCondition(ELogicalCondition.Greater, ELogicalCondition.Less) # C# 코드와 동일하게 유지 # Keep same as C# code
        # 임계값 설정, 위의 조건과 아래의 조건이 합쳐지면 130보다 크고 240보다 작은 객체를 검출
        # Threshold setting, when the above and below conditions are combined, an object greater than 130 and less than 240 is detected
        blob.SetThreshold(130, 240)

        # 2중 임계 값 설정을 아래와 같이 할 수도 있음. # You can set the double threshold as below.
        # blob.SetThreshold(130.0, EThresholdIndex.First)
        # blob.SetThreshold(240.0, EThresholdIndex.Second)

        # 가운데 구멍난 Contour를 지원하기 위해 Perforated 모드 설정
        # Set perforated mode to support perforated contours
        blob.SetResultType(CBlob.EBlobResultType.Contour)
        blob.SetContourResultType(CBlob.EContourResultType.Perforated)

        # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
        if (res := blob.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute Blob.")
            break

        # Blob 결과를 얻어오기 위해 FigureArray 선언 # Declare FigureArray to get blob result
        flfaContours = CFLFigureArray()

        # Blob 결과들 중 Contour를 얻어옴 # Get Contour from Blob results
        # res는 (CResult, 변경된 flfaContours) 튜플을 반환 # res returns a (CResult, modified flfaContours) tuple
        if (res := blob.GetResultContours(flfaContours)[0]).IsFail():
            ErrorPrint(res, "Failed to get boundary rects from the Blob object.")
            break

        # Mask 객체 생성 # Create Mask object
        mask = CMask()

        # Source 이미지 설정 # Set the source image
        mask.SetSourceImage(fliMaskImage)
        # Blob 결과인 flfaContours를 Src ROI로 설정 # Set blob result flfaContours as Src ROI
        mask.SetSourceROI(flfaContours)
        # Mask 색상 지정 # set mask color
        mvMaskValue = CMultiVar[Double](20, 227, 248)
        mask.SetMask(mvMaskValue)

        # 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
        if (res := mask.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute mask.")
            break

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        layerSrc = viewImageSrc.GetLayer(0)
        layerMask = viewImageMask.GetLayer(0)

        # 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
        layerSrc.Clear()
        layerMask.Clear()

        # ROI영역이 어디인지 알기 위해 디스플레이 한다 # Display to find out where ROI is
        # FLImaging의 Figure객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능
        if (res := layerSrc.DrawFigureImage(flfaContours, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        if (res := layerMask.DrawFigureImage(flfaContours, EColor.LIME)).IsFail():
            ErrorPrint(res, "Failed to draw figure")
            break

        # 이미지 뷰 정보 표시 # Display image view information
        flpPosition00 = CFLPoint[Double](0, 0)

        if (res := layerSrc.DrawTextCanvas(flpPosition00, "Source Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        if (res := layerMask.DrawTextCanvas(flpPosition00, "Mask Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        # Contours 정보값을 각각 확인하는 코드 # Code to check each Contours information value
        for i in range(flfaContours.GetCount()):
            pFlrg = CFLRegion(flfaContours.GetAt(i))

            # Region의 정점 정보를 콘솔에 출력 # Print region vertex information to the console
            print(f"Blob Result No. {i} : [")

            for j in range(pFlrg.GetCount()):
                if j != 0:
                    print(",", end="")

                pFlpVertex = CFLPoint[Double](pFlrg.GetAt(j))

                print(f"({pFlpVertex.x}, {pFlpVertex.y})", end="")

            print("]\n")

            flr = CFLRect[Double]()

            # res는 (CResult, 변경된 flr) 튜플을 반환 # res returns a (CResult, modified flr) tuple
            if (res := pFlrg.GetBoundaryRect(flr)[0]).IsFail():
                ErrorPrint(res, "Failed to get boundary rect.")
                break

            flpDraw = CFLPoint[Double](flr.left, (flr.top + flr.bottom) * 0.5)

            strNumber = f"{i}"

            layerSrc.DrawTextImage(flpDraw, strNumber, EColor.BLACK, EColor.YELLOW, 12, False, 0, EGUIViewImageTextAlignment.CENTER, None, 1.0, 1.0, EGUIViewImageFontWeight.BOLD, False)
        
        # 이전 루프에서 break가 발생했는지 다시 확인 (GetBoundaryRect 에러 시)
        if 'res' in locals() and res.IsFail():
            break


        # 이미지 뷰를 갱신 # Update image view
        viewImageSrc.Invalidate(True)
        viewImageMask.Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
        while viewImageSrc.IsAvailable() and viewImageMask.IsAvailable():
            CThreadUtilities.Sleep(1)

        viewImageSrc.Destroy()
        viewImageMask.Destroy()
        
        break
    
    # End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()