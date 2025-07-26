# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

import time

def main():
	# 3D 뷰 선언
	# Declaration of the 3D view 
    view3DSrc = CGUIView3D()
    view3DInclude = CGUIView3D()
    view3DExclude = CGUIView3D()
    view3DAdd = CGUIView3D()
    view3DRemove = CGUIView3D()
    view3DXOR = CGUIView3D()

    arrView3D = [view3DSrc, view3DInclude, view3DExclude, view3DAdd, view3DRemove, view3DXOR]
    res = CResult()

    while True:
		# 3D 뷰 생성 # Create the 3D view  # L, T, R, B(Left, Top, Right, Bottom) 
        if (res := view3DInclude.Create(0, 0, 300, 300)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.")
            break
        
        if (res := view3DSrc.Create(300, 0, 600, 300)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.")
            break
        
        if (res := view3DExclude.Create(600, 0, 900, 300)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.")
            break
        
        if (res := view3DAdd.Create(0, 300, 300, 600)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.")
            break
        
        if (res := view3DRemove.Create(300, 300, 600, 600)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.")
            break
        
        if (res := view3DXOR.Create(600, 300, 900, 600)).IsFail():
            ErrorPrint(res, "Failed to create 3D view.")
            break
        
		# 3D 객체 선언 # Declare a 3D object
        fl3DObjLeft = CFL3DObject()
        fl3DObjRight = CFL3DObject()
        
		# 3D 객체 로드 # Load a 3D object
        if (res := fl3DObjLeft.Load("../../ExampleImages/ROIUtilities3D/Left Cam.ply")).IsFail():
            ErrorPrint(res, "Failed load the ply file.")
            break

        if (res := fl3DObjRight.Load("../../ExampleImages/ROIUtilities3D/Right Cam.ply")).IsFail():
            ErrorPrint(res, "Failed load the ply file.")
            break

        for i in range(6):
			# 3D 뷰에 3D 객체 추가 # Add 3D objects to the 3D view
            arrView3D[i].PushObject(fl3DObjLeft)
            arrView3D[i].PushObject(fl3DObjRight)
			# 추가한 3D 객체가 화면 안에 들어오도록 Zoom Fit # Perform Zoom Fit to ensure added 3D objects are within the view
            arrView3D[i].ZoomFit()
            
			# 3D 뷰어의 시점(카메라) 변경 # Change the viewpoint (camera) of the 3D viewer
            cam = arrView3D[i].GetCamera()
            cam.SetPosition(CFLPoint3[Single](0.71, 0.02, 10.94))
            cam.SetDirectionUp(CFLPoint3[Single](1, 0, 0))
            arrView3D[i].SetCamera(cam)

            if i > 0:
				# 3D 뷰 시점 동기화 # Synchronize the viewpoint of the 3D view
                arrView3D[i].SynchronizePointOfView(arrView3D[i - 1])
				# 윈도우 동기화 # Synchronize the window
                arrView3D[i].SynchronizeWindow(arrView3D[i - 1])
                
		# 절두체 ROI 선언 # Declare the frustum ROI
        flfr = CFLFrustum3[Single]()
		# 파일에서 절두체 ROI 로드 # Load the frustum ROI from a file
        if (res := flfr.Load("../../ExampleImages/ROIUtilities3D/frustumROI.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.")
            break
        
		# 3D 뷰에 ROI 추가 # Add the ROI to the 3D view
        for i in range(6):
            arrView3D[i].PushBackROI(flfr)
            
        ###############################
        #           Include           #
        ###############################
		# CROIUtilities3D 객체 선언
		# Declare the CROIUtilities3D object
        roiUtil3D = CROIUtilities3D()
		# CROIUtilities3D 객체에 3D Object 추가 # Add 3D objects to the CROIUtilities3D object
        roiUtil3D.PushBack3DObject(fl3DObjLeft)
        roiUtil3D.PushBack3DObject(fl3DObjRight)
		# CROIUtilities3D 객체에 절두체 ROI 추가 # Add the frustum ROI to the CROIUtilities3D object
        roiUtil3D.PushBackROI(flfr)
        
		# 선택 타입 설정 : ROI 안에 포함되는 정점만 선택 
		# Set the selection type to include only vertices inside the ROI
        roiUtil3D.SetSelectionType(CROIUtilities3D.EResultSelectionType.Include)
		# CROIUtilities3D 실행 # Execute the CROIUtilities3D object
        if (res := roiUtil3D.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Include).")
            break
        
		# CROIUtilities3D 에서 결과 얻어 오기 # Retrieve the results from CROIUtilities3D
        arr2ResultROIIndexInclude = List[List[int]]()        
        if (res := roiUtil3D.GetResult(arr2ResultROIIndexInclude)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Include).")
            break
        
        if arr2ResultROIIndexInclude.Count > 0:
            i32ObjectIdx = 0
			# 3D 뷰어에 추가된 3D 객체의 개수 # Number of 3D objects added to the 3D viewer
            i32ObjectCount = view3DInclude.GetObjectCount()
            for i in range(i32ObjectCount):
				# 3D 뷰어에 추가된 i번째 3D 객체 # The i-th 3D object added to the 3D viewer
                pObj = view3DInclude.GetView3DObject(i)

				# 해당 객체가 없거나, 해당 객체에 대해 선택이 비활성화 되어 있다면 continue # Skip if the object is null or selection is disabled
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue
                
				# i번째 3D 객체의 데이터(CFL3DObject) # Data of the i-th 3D object (CFL3DObject)
                pObjData = pObj.Get3DObject()

				# 해당 객체가 없다면 continue # Skip if the object data is null
                if pObjData is None:
                    continue
                
				# i번째 3D 객체에 대한 결과값 배열. 이 배열은 i번째 3D 객체에 대해, ROI 내부에 위치한 정점의 인덱스로 이루어짐 # Result array for the i-th 3D object. Contains indices of vertices within the ROI.
                flaCollisionIndex = arr2ResultROIIndexInclude[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                
				# i번째 3D 객체에 대해, ROI 내부에 위치한 정점을 빨간색으로 표시 # Mark vertices within the ROI of the i-th 3D object in red
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 255, 0, 0)
                    
				# 3D 뷰어에 추가된 i번째 3D 객체에 대해 렌더링 업데이트 # Update rendering for the i-th 3D object added to the 3D viewer
                pObj.UpdateAll()
                view3DInclude.UpdateObject(i)
                
			# 3D 뷰어 업데이트 # Update the 3D viewer
            view3DInclude.UpdateScreen()
        
		# EResultSelectionType.Add 연산을 위해 CROIUtilities3D 객체 선언 및 roiUtil3D 를 복사 생성. 
		# Include 연산으로 얻은 결과값까지 복사됨
		# Declare and copy construct a CROIUtilities3D object for the EResultSelectionType.Add operation. 
		# The results from the Include operation are copied.
        roiUtil3DAdd = CROIUtilities3D(roiUtil3D)
		# 복사한 객체에서 ROI를 모두 클리어 # Clear all ROIs from the copied object
        roiUtil3DAdd.ClearROI()


        ###############################
        #           Exclude           #
        ###############################    
		# 선택 타입 설정 : ROI 바깥의 정점만 선택 
		# Set selection type: Select only vertices outside the ROI
        roiUtil3D.SetSelectionType(CROIUtilities3D.EResultSelectionType.Exclude)

		# CROIUtilities3D 실행 # Execute CROIUtilities3D
        if (res := roiUtil3D.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Exclude).")
            break

		# CROIUtilities3D 에서 결과 얻어 오기 # Retrieve results from CROIUtilities3D
        arr2ResultROIIndexExclude = List[List[int]]()
        
        if (res := roiUtil3D.GetResult(arr2ResultROIIndexExclude)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Exclude).")
            break
        
        if arr2ResultROIIndexExclude.Count > 0:
            i32ObjectIdx = 0

			# 3D 뷰어에 추가된 3D 객체의 개수 # Number of 3D objects added to the 3D viewer
            i32ObjectCount = view3DExclude.GetObjectCount()
            for i in range(i32ObjectCount):
				# 3D 뷰어에 추가된 i번째 3D 객체 # The i-th 3D object added to the 3D viewer
                pObj = view3DExclude.GetView3DObject(i)

				# 해당 객체가 없거나, 해당 객체에 대해 선택이 비활성화 되어 있다면 continue # Skip if the object is null or selection is disabled
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue

				# i번째 3D 객체의 데이터(CFL3DObject) # Data of the i-th 3D object (CFL3DObject)
                pObjData = pObj.Get3DObject()
                if pObjData is None:
                    continue

				# 해당 객체가 없다면 continue # Skip if the object data is null
                flaCollisionIndex = arr2ResultROIIndexExclude[i32ObjectIdx]
                i32ObjectIdx += 1

				# i번째 3D 객체에 대한 결과값 배열. 이 배열은 i번째 3D 객체에 대해, ROI 외부에 위치한 정점의 인덱스로 이루어짐 # Result array for the i-th 3D object. Contains indices of vertices outside the ROI.
                if flaCollisionIndex.Count == 0:
                    continue

				# i번째 3D 객체에 대해, ROI 바깥에 위치한 정점을 파란색으로 표시 # Mark vertices outside the ROI of the i-th 3D object in blue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 0, 0, 255) # BLUE

				# 3D 뷰어에 추가된 i번째 3D 객체에 대해 렌더링 업데이트 # Update rendering for the i-th 3D object added to the 3D viewer
                pObj.UpdateAll()
                view3DExclude.UpdateObject(i)

			# 3D 뷰어 업데이트 # Update the 3D viewer
            view3DExclude.UpdateScreen()
            
		# EResultSelectionType.Remove 연산을 위해 CROIUtilities3D 객체 선언 및 roiUtil3D 를 복사 생성. Exclude 연산으로 얻은 결과값까지 복사됨
		# Declare a CROIUtilities3D object for EResultSelectionType.Remove operation and copy roiUtil3D. Results from the Exclude operation are copied.
        roiUtil3DRemove = CROIUtilities3D(roiUtil3D)
        
		# EResultSelectionType.XOR 연산을 위해 CROIUtilities3D 객체 선언 및 roiUtil3D 를 복사 생성. Exclude 연산으로 얻은 결과값까지 복사됨
		# Declare a CROIUtilities3D object for EResultSelectionType.XOR operation and copy roiUtil3D. Results from the Exclude operation are copied.
        roiUtil3DXOR = CROIUtilities3D(roiUtil3D)

		# 복사한 객체에서 ROI를 모두 클리어 # Clear all ROIs from the copied objects
        roiUtil3DRemove.ClearROI()
        roiUtil3DXOR.ClearROI()


        ###############################
        #   Add(to Include Result)    #
        ###############################
		# 기존 선택 영역(위에서 Include로 선택한 영역)에 추가로 선택할 영역을 ROI로 설정
		# Set an additional ROI to be selected in the existing selection area (previously selected with Include)
        flfrAdd = CFLFrustum3[Single]()
        if (res := flfrAdd.Load("../../ExampleImages/ROIUtilities3D/frustumROI_Add.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.")
            break
        
		# CROIUtilities3D 객체에 절두체 ROI 추가 # Add the frustum ROI to the CROIUtilities3D object
        roiUtil3DAdd.PushBackROI(flfrAdd)
		# 3D 뷰에 ROI 추가 # Add the frustum ROI to the 3D view
        view3DAdd.PushBackROI(flfrAdd)
        
		# 선택 타입 설정 : 기존 결과에 ROI 안에 포함되는 정점을 추가 
		# Set selection type: Add vertices within the ROI to the existing results
        roiUtil3DAdd.SetSelectionType(CROIUtilities3D.EResultSelectionType.Add)

		# CROIUtilities3D 실행 # Execute CROIUtilities3D
        if (res := roiUtil3DAdd.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Add).")
            break
        
		# CROIUtilities3D 에서 결과 얻어 오기 # Retrieve results from CROIUtilities3D
        arr2ResultROIIndexAdd = List[List[int]]()
        
        if (res := roiUtil3DAdd.GetResult(arr2ResultROIIndexAdd)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Add).")
            break

        if arr2ResultROIIndexAdd.Count > 0:
            i32ObjectIdx = 0
			# 3D 뷰어에 추가된 3D 객체의 개수 # Number of 3D objects added to the 3D viewer
            i32ObjectCount = view3DAdd.GetObjectCount()
            for i in range(i32ObjectCount):
				# 3D 뷰어에 추가된 i번째 3D 객체 # The i-th 3D object added to the 3D viewer
                pObj = view3DAdd.GetView3DObject(i)

				# 해당 객체가 없거나, 해당 객체에 대해 선택이 비활성화 되어 있다면 continue # Skip if the object is null or selection is disabled
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue

				# i번째 3D 객체의 데이터(CFL3DObject) # Data of the i-th 3D object (CFL3DObject)
                pObjData = pObj.Get3DObject()

				# 해당 객체가 없다면 continue # Skip if the object data is null
                if pObjData is None:
                    continue

				# i번째 3D 객체에 대한 결과값 배열. # Result array for the i-th 3D object
                flaCollisionIndex = arr2ResultROIIndexAdd[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue

				# i번째 3D 객체에 대해, ROI 내부에 위치한 정점을 빨간색으로 표시 # Mark vertices within the ROI of the i-th 3D object in red
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 255, 0, 0) # RED

				# 3D 뷰어에 추가된 i번째 3D 객체에 대해 렌더링 업데이트 # Update rendering for the i-th 3D object added to the 3D viewer
                pObj.UpdateAll()
                view3DAdd.UpdateObject(i)
			# 3D 뷰어 업데이트 # Update the 3D viewer
            view3DAdd.UpdateScreen()
            

        ###############################
        # Remove(from Exclude Result) #
        ###############################
		# 기존 선택 영역(위에서 Exclude로 선택한 영역)에서 제거할 영역을 ROI로 설정
		# Set ROIs to remove areas from the existing selection (previously selected with Exclude)
        flfrRemove1 = CFLFrustum3[Single]()
        flfrRemove2 = CFLFrustum3[Single]()

        if (res := flfrRemove1.Load("../../ExampleImages/ROIUtilities3D/frustumROI_Remove1.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.")
            break
        
        if (res := flfrRemove2.Load("../../ExampleImages/ROIUtilities3D/frustumROI_Remove2.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.")
            break
        
		# CROIUtilities3D 객체에 절두체 ROI 추가 # Add the frustum ROIs to the CROIUtilities3D object
        roiUtil3DRemove.PushBackROI(flfrRemove1)
        roiUtil3DRemove.PushBackROI(flfrRemove2)
		# 3D 뷰에 ROI 추가 # Add the frustum ROIs to the 3D view
        view3DRemove.PushBackROI(flfrRemove1)
        view3DRemove.PushBackROI(flfrRemove2)
        
		# 선택 타입 설정 : 기존 결과에서 ROI 안의 정점을 제거 # Set selection type: Remove vertices within the ROI from the existing results
        roiUtil3DRemove.SetSelectionType(CROIUtilities3D.EResultSelectionType.Remove)
        
		# CROIUtilities3D 실행 # Execute CROIUtilities3D
        if (res := roiUtil3DRemove.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(Remove).")
            break
        
		# CROIUtilities3D 에서 결과 얻어 오기 # Retrieve results from CROIUtilities3D
        arr2ResultROIIndexRemove = List[List[int]]()
        if (res := roiUtil3DRemove.GetResult(arr2ResultROIIndexRemove)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(Remove).")
            break

        if arr2ResultROIIndexRemove.Count > 0:
            i32ObjectIdx = 0
			# 3D 뷰어에 추가된 3D 객체의 개수 # Number of 3D objects added to the 3D viewer
            i32ObjectCount = view3DRemove.GetObjectCount()
            for i in range(i32ObjectCount):
				# 3D 뷰어에 추가된 i번째 3D 객체 # The i-th 3D object added to the 3D viewer
                pObj = view3DRemove.GetView3DObject(i)

				# 해당 객체가 없거나, 해당 객체에 대해 선택이 비활성화 되어 있다면 continue # Skip if the object is null or selection is disabled
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue

				# i번째 3D 객체의 데이터(CFL3DObject) # Data of the i-th 3D object (CFL3DObject)
                pObjData = pObj.Get3DObject()

				# 해당 객체가 없다면 continue # Skip if the object data is null
                if pObjData is None:
                    continue

				# i번째 3D 객체에 대한 결과값 배열. # Result array for the i-th 3D object
                flaCollisionIndex = arr2ResultROIIndexRemove[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue

				# i번째 3D 객체에 대해, 기존 결과에서 ROI 안의 정점을 제거 후 선택된 정점을 파란색으로 표시 # Mark selected vertices after removing vertices within the ROI of the i-th 3D object in blue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 0, 0, 255) # BLUE

				# 3D 뷰어에 추가된 i번째 3D 객체에 대해 렌더링 업데이트 # Update rendering for the i-th 3D object added to the 3D viewer
                pObj.UpdateAll()
                view3DRemove.UpdateObject(i)
			# 3D 뷰어 업데이트 # Update the 3D viewer
            view3DRemove.UpdateScreen()
            

        ###############################
        #   XOR(from Exclude Result)  #
        ###############################
		# 기존 선택 영역(위에서 Exclude로 선택한 영역)에서 XOR 선택할 영역을 ROI로 설정 
		# Set an ROI to perform XOR operation on the existing selection (previously selected with Exclude)
        flfrXOR = CFLFrustum3[Single]()
        if (res := flfrXOR.Load("../../ExampleImages/ROIUtilities3D/frustumROI_XOR.fig")).IsFail():
            ErrorPrint(res, "Failed load the figure file.")
            break
        
		# CROIUtilities3D 객체에 절두체 ROI 추가 # Add the frustum ROI to the CROIUtilities3D object
        roiUtil3DXOR.PushBackROI(flfrXOR)
		# 3D 뷰에 ROI 추가 # Add the frustum ROI to the 3D view
        view3DXOR.PushBackROI(flfrXOR)
        
		# 선택 타입 설정 : 기존 결과에서 ROI 안의 정점을 XOR 연산하여 선택 
		# Set selection type: Perform XOR operation with vertices inside the ROI on the existing results
        roiUtil3DXOR.SetSelectionType(CROIUtilities3D.EResultSelectionType.XOR)
        
		# CROIUtilities3D 실행 # Execute CROIUtilities3D
        if (res := roiUtil3DXOR.Execute()).IsFail():
            ErrorPrint(res, "Failed to execute(XOR).")
            break
        
		# CROIUtilities3D 에서 결과 얻어 오기 # Retrieve results from CROIUtilities3D
        arr2ResultROIIndexXOR = List[List[int]]()        
        if (res := roiUtil3DXOR.GetResult(arr2ResultROIIndexXOR)[0]).IsFail():
            ErrorPrint(res, "Failed to get result(XOR).")
            break

        if arr2ResultROIIndexXOR.Count > 0:
            i32ObjectIdx = 0
			# 3D 뷰어에 추가된 3D 객체의 개수 # Number of 3D objects added to the 3D viewer
            i32ObjectCount = view3DXOR.GetObjectCount()

            for i in range(i32ObjectCount):
				# 3D 뷰어에 추가된 i번째 3D 객체 # The i-th 3D object added to the 3D viewer
                pObj = view3DXOR.GetView3DObject(i)

				# 해당 객체가 없거나, 해당 객체에 대해 선택이 비활성화 되어 있다면 continue # Skip if the object is null or selection is disabled
                if pObj is None or not pObj.IsSelectionEnabled():
                    continue

				# i번째 3D 객체의 데이터(CFL3DObject) # Data of the i-th 3D object (CFL3DObject)
                pObjData = pObj.Get3DObject()

				# 해당 객체가 없다면 continue # Skip if the object data is null
                if pObjData is None:
                    continue

				# i번째 3D 객체에 대한 결과값 배열. # Result array for the i-th 3D object
                flaCollisionIndex = arr2ResultROIIndexXOR[i32ObjectIdx]
                i32ObjectIdx += 1
                if flaCollisionIndex.Count == 0:
                    continue
                
				# i번째 3D 객체에 대해, 기존 결과에서 ROI 안의 정점을 XOR 연산한 결과 정점들을 파란색으로 표시 # Mark the vertices resulting from XOR operation within the ROI of the i-th 3D object in blue
                for j in range(flaCollisionIndex.Count):
                    pObjData.SetVertexColorAt(flaCollisionIndex[j], 0, 0, 255) # BLUE

				# 3D 뷰어에 추가된 i번째 3D 객체에 대해 렌더링 업데이트 # Update rendering for the i-th 3D object added to the 3D viewer
                pObj.UpdateAll()
                view3DXOR.UpdateObject(i)

			# 3D 뷰어 업데이트 # Update the 3D viewer
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
			# 아래 함수 DrawTextCanvas는 Screen좌표를 기준으로 문자열을 뷰어에 출력한다.
            # Draw the position text to canvas
			# 색상 파라미터를 EColor.TRANSPARENCY 로 넣어주면 투명색으로 처리된다.
			# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 -> 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
			# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle -> Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
            if (res := view.GetLayer(0).DrawTextCanvas(flp, label, EColor.YELLOW, EColor.BLACK, 18)).IsFail():
                ErrorPrint(res, "Failed to draw text")
                break
            
		# 3D 뷰를 갱신 # Update 3D view
        for i in range(6):
            arrView3D[i].Invalidate(True)
            
        # 3D 뷰들이 종료될 때까지 대기
        # Wait until 3D views are closed
        while all(view.IsAvailable() for view in arrView3D):
            time.sleep(0.01)

        break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()