# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time

def main():
    viewImage = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]
    res = CResult()

    while True:
        if (res := viewImage[0].Create(0, 0, 400, 440)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        if (res := viewImage[1].Create(400, 0, 800, 440)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        if (res := viewImage[2].Create(800, 0, 1200, 440)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        viewImage[0].SynchronizeWindow(viewImage[1])
        viewImage[0].SynchronizeWindow(viewImage[2])

        pObj3D = CFL3DObject()
        pObj3D.Load("../../ExampleImages/ProjectionUtilities3D/Cylinder.step")

        fliFinal = [CFLImage(), CFLImage(), CFLImage()]
        fliRes = CFLImage()
        figureText = CFLFigureText[Int32]()

        pu = CProjectionUtilities3D()
        pu.PushBack3DObject(pObj3D)
        pu.SetResultImageSize(400, 400)
        pu.SetBackgroundColorOfResultImage(21, 21, 21)

        # 1-1. 첫 번째 카메라
        camSet1 = CFL3DCamera()
        camSet1.SetProjectionType(E3DCameraProjectionType.Perspective)
        camSet1.SetPosition(CFLPoint3[Single](-1.41, -317.67, 280.92))
        camSet1.SetDirection(CFLPoint3[Single](0.01, 0.87, -0.50))
        camSet1.SetDirectionUp(CFLPoint3[Single](-0.01, 0.50, 0.87))
        camSet1.SetAngleOfViewY(45)
        camSet1.SetTarget(CFLPoint3[Single](2.13, -59.49, 132.75))
        camSet1.SetNearZ(271.84)
        camSet1.SetFarZ(459.30)

        pu.SetCamera(camSet1)
        res = pu.Execute()
        res = pu.GetResult(fliRes)
        figureText.Set(CFLPoint[Int32](10, 10), "1. Projection(Camera Set 1)", int(EColor.YELLOW), int(EColor.BLACK), 20, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.BOLD, False)
        fliRes.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))
        fliFinal[0].Assign(fliRes)

        # 1-2. 두 번째 카메라
        camSet2 = CFL3DCamera()
        camSet2.SetProjectionType(E3DCameraProjectionType.Perspective)
        camSet2.SetPosition(CFLPoint3[Single](-80.38, 97.35, 341.92))
        camSet2.SetDirection(CFLPoint3[Single](0.42, -0.27, -0.86))
        camSet2.SetDirectionUp(CFLPoint3[Single](0.77, 0.61, 0.19))
        camSet2.SetAngleOfViewY(45)
        camSet2.SetTarget(CFLPoint3[Single](-5.45, 49.05, 189.72))
        camSet2.SetNearZ(148.33)
        camSet2.SetFarZ(390.77)

        pu.SetCamera(camSet2)
        res = pu.Execute()
        res = pu.GetResult(fliRes)
        figureText.Set(CFLPoint[Int32](10, 10), "1. Projection(Camera Set 2)", int(EColor.YELLOW), int(EColor.BLACK), 20, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.BOLD, False)
        fliRes.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))
        fliFinal[0].PushBackPage(fliRes)

        viewImage[0].SetImagePtr(fliFinal[0])
        viewImage[0].SetFixThumbnailView(True)
        viewImage[0].ShowImageMiniMap(False)
        viewImage[0].ShowPageIndex(False)

        # 2. Interpolation projection
        pu.SetTopologyType(ETopologyType3D.Wireframe)
        for i in range(11):
            f32T = i * 0.1
            camInterpolation = CFL3DCamera()
            CFL3DCamera.Interpolate(camSet1, camSet2, f32T, camInterpolation)
            pu.SetCamera(camInterpolation)
            res = pu.Execute()
            res = pu.GetResult(fliRes)
            text = f"2. Projection(Camera Interpolation T={f32T:.1f})"
            figureText.Set(CFLPoint[Int32](10, 10), text, int(EColor.YELLOW), int(EColor.BLACK), 17, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.SEMIBOLD, False)
            fliRes.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))

            if i == 0:
                fliFinal[1].Assign(fliRes)
            else:
                fliFinal[1].PushBackPage(fliRes)

        viewImage[1].SetImagePtr(fliFinal[1])
        viewImage[1].SetFixThumbnailView(True)
        viewImage[1].ShowImageMiniMap(False)
        viewImage[1].ShowPageIndex(False)

        # 3. ZoomFit
        pu.SetTopologyType(ETopologyType3D.PointCloud)
        pu.SetPointSize(5.0)
        pu.ZoomFitCamera()
        res = pu.Execute()
        res = pu.GetResult(fliFinal[2])
        figureText.Set(CFLPoint[Int32](10, 10), "3. Projection(ZoomFit)", int(EColor.YELLOW), int(EColor.BLACK), 20, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.BOLD, False)
        fliFinal[2].PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))

        viewImage[2].SetImagePtr(fliFinal[2])
        viewImage[2].SetFixThumbnailView(True)
        viewImage[2].ShowImageMiniMap(False)
        viewImage[2].ShowPageIndex(False)

        while viewImage[0].IsAvailable() and viewImage[1].IsAvailable() and viewImage[2].IsAvailable():
            time.sleep(0.01)
        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()