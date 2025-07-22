# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time

def main():
    view3D = Array[CGUIView3D]([CGUIView3D(), CGUIView3D()])

    while True:
        if (res := view3D[0].Create(100, 0, 612, 512)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.\n")
            break

        if (res := view3D[1].Create(612, 0, 1124, 512)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.\n")
            break

        view3D[0].SynchronizeWindow(view3D[1])

        view3D[0].SetTopologyType(ETopologyType3D.Wireframe)
        view3D[1].SetTopologyType(ETopologyType3D.Wireframe)

        res, i32ReturnIndex = view3D[0].PushObject(CGUIView3DObject(), -1)
        if res.IsFail():
            ErrorPrint(res, "Failed to display 3D object.\n")
            break
        
        objView3D = view3D[0].GetView3DObject(i32ReturnIndex)
        if objView3D is None:
            res = CResult(EResult.NullPointer)
            ErrorPrint(res, "Failed to get View3D object.\n")
            break

        fl3DObject = objView3D.Get3DObject()
        if fl3DObject is None:
            res = CResult(EResult.NullPointer)
            ErrorPrint(res, "Failed to get 3D object.\n")
            break

        f64ChordalDeviation = 0.0

        if (res := fl3DObject.LoadSTEP("../../ExampleImages/StepReaderConvertTo3DObject/Cylinder.step", f64ChordalDeviation)).IsFail():
            ErrorPrint(res, "Failed to load step file.\n")
            break

        view3D[0].UpdateObject(i32ReturnIndex)
        view3D[0].ZoomFit()

        sr = CStepReader()
        f64ChordalDeviation = 0.00001

        res, i32ReturnIndex = view3D[1].PushObject(CGUIView3DObject(), -1)

        if res.IsFail():
            ErrorPrint(res, "Failed to display 3D object.\n")
            break

        objView3D2 = view3D[1].GetView3DObject(i32ReturnIndex)
        if objView3D2 is None:
            ErrorPrint(res, "Failed to get View3D object.\n")
            break

        fl3DObject2 = objView3D2.Get3DObject()
        if fl3DObject2 is None:
            res = CResult(EResult.NullPointer)
            ErrorPrint(res, "Failed to get 3D object.\n")
            break

        if (res := sr.Load("../../ExampleImages/StepReaderConvertTo3DObject/Cylinder.step")).IsFail():
            ErrorPrint(res, "Failed to load step file.\n")
            break

        if (res := sr.GetResult3DObject(fl3DObject2, f64ChordalDeviation)[0]).IsFail():
            ErrorPrint(res, "Failed to get 3D object from the StepReader.\n")
            break

        view3D[1].UpdateObject(i32ReturnIndex)
        view3D[1].ZoomFit()

        camera = CGUIView3DCamera()
        camera.SetDirection(CFLPoint3[Single](-0.2, 0.8, -0.6))
        camera.SetDirectionUp(CFLPoint3[Single](-0.2, 1.0, 0.1))
        camera.SetPosition(CFLPoint3[Single](56.2, -276.5, 324.0))
        camera.SetTarget(CFLPoint3[Single](9.6, -34.5, 151.4))

        view3D[0].SetCamera(camera)
        view3D[1].SetCamera(camera)

        flp = CFLPoint[Double](0, 0)
        if (res := view3D[0].GetLayer(2).DrawTextCanvas(flp, "Chordal Deviation = 0.0", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text\n")
            break

        if (res := view3D[1].GetLayer(2).DrawTextCanvas(flp, "Chordal Deviation = 0.00001", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text\n")
            break

        view3D[0].SetCanvasColor(EColor.WHITE)
        view3D[1].SetCanvasColor(EColor.WHITE)

        view3D[0].UpdateScreen()
        view3D[1].UpdateScreen()

        while view3D[0].IsAvailable() and view3D[1].IsAvailable():
            CThreadUtilities.Sleep(1)

        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()