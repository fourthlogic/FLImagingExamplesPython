from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 경고 코드 // Error print function
def ErrorPrint(res: CResult, msg: str):
    if len(msg) > 1:
        print(msg)
    print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
    input()

def main():
    # 이미지 객체 선언 // Declare the image object
    fliLearnImage = CFLImage()
    fliFindImage = CFLImage()

    # 이미지 뷰 선언 // Declare the image view
    viewImageLearn = CGUIViewImage()
    viewImageFind = CGUIViewImage()

    res = CResult()

    while True:
        # 이미지 로드 // Load image
        if (res := fliLearnImage.Load("../../ExampleImages/Matching/Rectangle Array_0.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        if (res := fliFindImage.Load("../../ExampleImages/Matching/Rectangle Array_1.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        # 이미지 뷰 생성 // Create image view
        if (res := viewImageLearn.Create(400, 0, 912, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        if (res := viewImageFind.Create(912, 0, 1680, 576)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 이미지 뷰에 이미지를 디스플레이 // Display the image in the imageview
        if (res := viewImageLearn.SetImagePtr(fliLearnImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            break

        if (res := viewImageFind.SetImagePtr(fliFindImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.\n")
            break

        # 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
        if (res := viewImageLearn.SynchronizeWindow(viewImageFind)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        layerLearn = viewImageLearn.GetLayer(0)
        layerFind = viewImageFind.GetLayer(1)

        layerLearn.Clear()
        layerFind.Clear()

        flp00 = CFLPoint[Double](0, 0)

        if (res := layerLearn.DrawTextCanvas(flp00, "Measurement Array", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        if (res := layerFind.DrawTextCanvas(flp00, "FIND", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        # Rectangle Array Match 객체 생성 // Create Rectangle Array Match Object
        rectangleArrayMatch = CRectangleArrayMatch()

        # 학습할 영역을 설정합니다. // Set the area to learn.
        flfaMeasurement = CFLFigureArray()
        flrRect00 = CFLRect[Double](587.479194, 364.452004, 929.550836, 616.575019)
        flrRect01 = CFLRect[Double](583.464651, 1215.493013, 924.560595, 1467.566788)
        flrRect02 = CFLRect[Double](1531.503352, 655.504324, 1872.516362, 908.626989)
        flrRect03 = CFLRect[Double](1241.471070, 1222.460787, 1580.517129, 1474.488487)

        flfaMeasurement.PushBack(flrRect00)
        flfaMeasurement.PushBack(flrRect01)
        flfaMeasurement.PushBack(flrRect02)
        flfaMeasurement.PushBack(flrRect03)

        flpCameraPivot = CFLPoint[Double](0, 0)
        eFitting = CRectangleArrayMatch.EFitting.Enable

        # 검출 시 사용될 파라미터를 설정합니다 // Set the parameters to be used for detection
        rectangleArrayMatch.SetSourceImage(fliFindImage)
        rectangleArrayMatch.SetArray(flfaMeasurement)
        rectangleArrayMatch.SetBaseAngle(0.0)
        rectangleArrayMatch.EnablePivotImageCenter(True)
        rectangleArrayMatch.SetPivotOffset(flpCameraPivot)
        rectangleArrayMatch.SetMinScore(0.5)
        rectangleArrayMatch.SetObjectAngleTolerance(180)
        rectangleArrayMatch.SetFitting(eFitting)
        rectangleArrayMatch.SetAllowingObjectDistanceError(-1)

        for i64Index in range(flfaMeasurement.GetCount()):
            if flfaMeasurement.GetAt(i64Index).GetDeclType() != EFigureDeclType.Rect:
                break

            if (res := layerLearn.DrawFigureImage(flfaMeasurement, EColor.BLUE, 3, EColor.BLUE, EGUIViewImagePenStyle.Solid, 0.25, 0.25)).IsFail():
                ErrorPrint(res, "Failed to draw figure.\n")
                break

        # 알고리즘 수행 // Execute the algorithm
        if (res := rectangleArrayMatch.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute.")
            break

        # 검출 결과 배열의 개수를 가져옵니다 // Get the number of detection result arrays
        i64ResultCount = rectangleArrayMatch.GetResultCount()
        f64Score = 0.0
        f64Angle = 0.0
        
        res, f64Score = rectangleArrayMatch.GetResultArrayScore(f64Score)
        res, f64Angle = rectangleArrayMatch.GetResultArrayAngle(f64Angle)

        for i in range(i64ResultCount):
            sResult = CRectangleArrayMatch.SResult()
            rectangleArrayMatch.GetResult(i, sResult)
            flpRegionCenter = sResult.pFlrMeasuredRegion.GetCenter()
            strDisplayResult = f"Array Element ID : {int(sResult.i64Index)}\n Score : {sResult.f64Score:.3f}\n Angle : {sResult.f64Angle:.3f}"

            if (res := layerFind.DrawFigureImage(sResult.pFlrMeasuredRegion, EColor.BLACK, 3)).IsFail():
                ErrorPrint(res, "Failed to draw figure.\n")
                break

            if (res := layerFind.DrawFigureImage(sResult.pFlrMeasuredRegion, EColor.CYAN, 1)).IsFail():
                ErrorPrint(res, "Failed to draw figure.\n")
                break

            if (res := layerFind.DrawTextImage(flpRegionCenter, strDisplayResult, EColor.YELLOW, EColor.BLACK, 11)).IsFail():
                ErrorPrint(res, "Failed to draw text.\n")
                break

            if i == 0:
                strDisplayResultArray = f"Array Score : {f64Score:.3f}  Array Angle : {f64Angle:.3f}"
                print(strDisplayResultArray)

                strDisplayResult = f"Array Score : {f64Score:.3f}\n Array Angle : {f64Angle:.3f}"
                flqRegion = CFLQuad[Double](sResult.pFlrMeasuredRegion)

                f64MaxY = -10000000
                f64MaxX = 1000000

                arrX = [p.x for p in flqRegion.flpPoints]
                arrY = [p.y for p in flqRegion.flpPoints]

                for y in arrY:
                    if f64MaxY > y:
                        f64MaxY = y

                for j in range(4):
                    if f64MaxY == arrY[j] and f64MaxX > arrX[j]:
                        f64MaxX = arrX[j]

                flpArrayResult = CFLPoint[Double](f64MaxX, f64MaxY - 10)

                if (res := layerFind.DrawTextImage(flpArrayResult, strDisplayResult, EColor.GOLD, EColor.BLACK, 14)).IsFail():
                    ErrorPrint(res, "Failed to draw text.\n")
                    break

            strDisplayResultElement = f"Array Element ID : {int(sResult.i64Index)} Score : {sResult.f64Score:.3f} Angle : {sResult.f64Angle:.3f}"
            print(f" - {strDisplayResultElement}")

        # 이미지 뷰를 갱신 합니다 // Update the image view
        viewImageLearn.Invalidate(True)
        viewImageFind.Invalidate(True)

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the imageview to close
        while viewImageLearn.IsAvailable() and viewImageFind.IsAvailable():
            CThreadUtilities.Sleep(1)

        break

if __name__ == "__main__":
    main()
