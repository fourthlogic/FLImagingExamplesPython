# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time

def main():
    view3DSrc = CGUIView3D()
    view3DInclude = CGUIView3D()
    view3DExclude = CGUIView3D()
    view3DAdd = CGUIView3D()
    view3DRemove = CGUIView3D()
    view3DXOR = CGUIView3D()

    arrView3D = [view3DSrc, view3DInclude, view3DExclude, view3DAdd, view3DRemove, view3DXOR]
    res = CResult()

    while True:
        if (res := view3DInclude.Create(0, 0, 300, 300)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.\n")
            break
        
        if (res := view3DSrc.Create(300, 0, 600, 300)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.\n")
            break
        
        if (res := view3DExclude.Create(600, 0, 900, 300)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.\n")
            break
        
        if (res := view3DAdd.Create(0, 300, 300, 600)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.\n")
            break
        
        if (res := view3DRemove.Create(300, 300, 600, 600)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.\n")
            break
        
        if (res := view3DXOR.Create(600, 300, 900, 600)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.\n")
            break
        
        fl3DObjLeft = CFL3DObject()
        fl3DObjRight = CFL3DObject()

        if (res := fl3DObjLeft.Load("../../ExampleImages/ROIUtilities3D/Left Cam.ply")).IsFail():
            ErrorPrint(res, "Failed load the ply file.\n")
            break

        if (res := fl3DObjRight.Load("../../ExampleImages/ROIUtilities3D/Right Cam.ply")).IsFail():
            ErrorPrint(res, "Failed load the ply file.\n")
            break

        for i in range(6):
            arrView3D[i].PushObject(fl3DObjLeft)
            arrView3D[i].PushObject(fl3DObjRight)
            arrView3D[i].ZoomFit()

            cam = arrView3D[i].GetCamera()
            cam.SetPosition(CFLPoint3[Single](0.71, 0.02, 10.94))
            cam.SetDirectionUp(CFLPoint3[Single](1, 0, 0))
            arrView3D[i].SetCamera(cam)

            if i > 0:
                arrView3D[i].SynchronizePointOfView(arrView3D[i - 1])
                arrView3D[i].SynchronizeWindow(arrView3D[i - 1])

        flfr = CFLFrustum3[Single]()
        if (res := flfr.Load("../../ExampleImages/ROIUtilities3D/frustumROI.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.\n")
            break

        for i in range(6):
            arrView3D[i].PushBackROI(flfr)

        roiUtil3D = CROIUtilities3D()
        roiUtil3D.PushBack3DObject(fl3DObjLeft)
        roiUtil3D.PushBack3DObject(fl3DObjRight)
        roiUtil3D.PushBackROI(flfr)

        roiUtil3D.SetSelectionType(CROIUtilities3D.EResultSelectionType.Include)
        if (res := roiUtil3D.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Include).\n")
            break

        arr2ResultROIIndexInclude = List[List[int]]()        
        if (res := roiUtil3D.GetResult(arr2ResultROIIndexInclude)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Include).\n")
            break

        roiUtil3DAdd = CROIUtilities3D(roiUtil3D)
        roiUtil3DAdd.ClearROI()

        if arr2ResultROIIndexInclude.Count > 0:
            i32ObjectIdx = 0
            i32ObjectCount = view3DInclude.GetObjectCount()
            for i in range(i32ObjectCount):
                pObj = view3DInclude.GetView3DObject(i)
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue
                pObjData = pObj.Get3DObject()
                if pObjData is None:
                    continue
                flaCollisionIndex = arr2ResultROIIndexInclude[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 255, 0, 0)
                pObj.UpdateAll()
                view3DInclude.UpdateObject(i)
            view3DInclude.UpdateScreen()

        roiUtil3D.SetSelectionType(CROIUtilities3D.EResultSelectionType.Exclude)
        if (res := roiUtil3D.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Exclude).\n")
            break

        arr2ResultROIIndexExclude = List[List[int]]()
        
        if (res := roiUtil3D.GetResult(arr2ResultROIIndexExclude)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Exclude).\n")
            break

        roiUtil3DRemove = CROIUtilities3D(roiUtil3D)
        roiUtil3DXOR = CROIUtilities3D(roiUtil3D)
        roiUtil3DRemove.ClearROI()
        roiUtil3DXOR.ClearROI()

        if arr2ResultROIIndexExclude.Count > 0:
            i32ObjectIdx = 0
            i32ObjectCount = view3DExclude.GetObjectCount()
            for i in range(i32ObjectCount):
                pObj = view3DExclude.GetView3DObject(i)
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue
                pObjData = pObj.Get3DObject()
                if pObjData is None:
                    continue
                flaCollisionIndex = arr2ResultROIIndexExclude[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 0, 0, 255)
                pObj.UpdateAll()
                view3DExclude.UpdateObject(i)
            view3DExclude.UpdateScreen()

        flfrAdd = CFLFrustum3[Single]()
        if (res := flfrAdd.Load("../../ExampleImages/ROIUtilities3D/frustumROI_Add.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.\n")
            break

        roiUtil3DAdd.PushBackROI(flfrAdd)
        view3DAdd.PushBackROI(flfrAdd)

        roiUtil3DAdd.SetSelectionType(CROIUtilities3D.EResultSelectionType.Add)
        if (res := roiUtil3DAdd.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Add).\n")
            break

        arr2ResultROIIndexAdd = List[List[int]]()
        
        if (res := roiUtil3DAdd.GetResult(arr2ResultROIIndexAdd)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Add).\n")
            break

        if arr2ResultROIIndexAdd.Count > 0:
            i32ObjectIdx = 0
            i32ObjectCount = view3DAdd.GetObjectCount()
            for i in range(i32ObjectCount):
                pObj = view3DAdd.GetView3DObject(i)
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue
                pObjData = pObj.Get3DObject()
                if pObjData is None:
                    continue
                flaCollisionIndex = arr2ResultROIIndexAdd[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 255, 0, 0)
                pObj.UpdateAll()
                view3DAdd.UpdateObject(i)
            view3DAdd.UpdateScreen()

        flfrRemove1 = CFLFrustum3[Single]()
        flfrRemove2 = CFLFrustum3[Single]()
        if (res := flfrRemove1.Load("../../ExampleImages/ROIUtilities3D/frustumROI_Remove1.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.\n")
            break

        if (res := flfrRemove2.Load("../../ExampleImages/ROIUtilities3D/frustumROI_Remove2.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.\n")
            break

        roiUtil3DRemove.PushBackROI(flfrRemove1)
        roiUtil3DRemove.PushBackROI(flfrRemove2)
        view3DRemove.PushBackROI(flfrRemove1)
        view3DRemove.PushBackROI(flfrRemove2)
        roiUtil3DRemove.SetSelectionType(CROIUtilities3D.EResultSelectionType.Remove)

        if (res := roiUtil3DRemove.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Remove).\n")
            break

        arr2ResultROIIndexRemove = List[List[int]]()
        
        if (res := roiUtil3DRemove.GetResult(arr2ResultROIIndexRemove)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Remove).\n")
            break

        if arr2ResultROIIndexRemove.Count > 0:
            i32ObjectIdx = 0
            i32ObjectCount = view3DRemove.GetObjectCount()
            for i in range(i32ObjectCount):
                pObj = view3DRemove.GetView3DObject(i)
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue
                pObjData = pObj.Get3DObject()
                if pObjData is None:
                    continue
                flaCollisionIndex = arr2ResultROIIndexRemove[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 0, 0, 255)
                pObj.UpdateAll()
                view3DRemove.UpdateObject(i)
            view3DRemove.UpdateScreen()

        flfrXOR = CFLFrustum3[Single]()
        if (res := flfrXOR.Load("../../ExampleImages/ROIUtilities3D/frustumROI_XOR.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.\n")
            break

        roiUtil3DXOR.PushBackROI(flfrXOR)
        view3DXOR.PushBackROI(flfrXOR)
        roiUtil3DXOR.SetSelectionType(CROIUtilities3D.EResultSelectionType.XOR)

        if (res := roiUtil3DXOR.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(XOR).\n")
            break

        arr2ResultROIIndexXOR = List[List[int]]()
        
        if (res := roiUtil3DXOR.GetResult(arr2ResultROIIndexXOR)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(XOR).\n")
            break

        if arr2ResultROIIndexXOR.Count > 0:
            i32ObjectIdx = 0
            i32ObjectCount = view3DXOR.GetObjectCount()
            for i in range(i32ObjectCount):
                pObj = view3DXOR.GetView3DObject(i)
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue
                pObjData = pObj.Get3DObject()
                if pObjData is None:
                    continue
                flaCollisionIndex = arr2ResultROIIndexXOR[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 0, 0, 255)
                pObj.UpdateAll()
                view3DXOR.UpdateObject(i)
            view3DXOR.UpdateScreen()

        flp = CFLPoint[Single](5, 0)
        labelText = [
            ("Source", view3DSrc),
            ("Include", view3DInclude),
            ("Exclude", view3DExclude),
            ("Add(Include Result+Add)", view3DAdd),
            ("Remove(Exclude Result-Remove)", view3DRemove),
            ("XOR(Exclude Result^XOR)", view3DXOR)
        ]

        for label, view in labelText:
            if (res := view.GetLayer(0).DrawTextCanvas(flp, label, EColor.YELLOW, EColor.BLACK, 18)).IsFail():
                ErrorPrint(res, "Failed to draw text\n")
                break

        for i in range(6):
            arrView3D[i].Invalidate(True)

        while all(view.IsAvailable() for view in arrView3D):
            time.sleep(0.01)

        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()