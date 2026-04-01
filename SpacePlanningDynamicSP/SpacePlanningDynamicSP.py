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
	# 3D 뷰 선언 # Declare 3D views
	view3DResult = CGUIView3D()

	res = CResult(EResult.UnknownError)

	while True:
		# 알고리즘 객체 선언 # Declare algorithm object
		alg = CSpacePlanningDynamicSP()

		# Bin spec 설정 # Set the bin spec
		binSpec = CSpacePlanningBaseSP.SBinSpec[Single](12.0, 9.0, 10.0)

		if (res := alg.AddBinSpec(binSpec)).IsFail():
			ErrorPrint(res, "Failed to add bin spec.")
			break

		# Item spec 설정 (회전 없음) # Set the item specs (no rotation)
		itemSpec1 = CSpacePlanningBaseSP.SItemSpec[Single](3.0, 3.0, 4.0, 1.0, CSpacePlanningBaseSP.ERotationType.NoRotation)
		itemSpec2 = CSpacePlanningBaseSP.SItemSpec[Single](4.0, 3.0, 3.0, 1.0, CSpacePlanningBaseSP.ERotationType.NoRotation)
		itemSpec3 = CSpacePlanningBaseSP.SItemSpec[Single](5.0, 3.0, 2.0, 1.0, CSpacePlanningBaseSP.ERotationType.NoRotation)

		if (res := alg.AddItemSpec(itemSpec1)).IsFail() or \
		   (res := alg.AddItemSpec(itemSpec2)).IsFail() or \
		   (res := alg.AddItemSpec(itemSpec3)).IsFail():
			ErrorPrint(res, "Failed to add item spec.")
			break

		# Random sequence list 파라미터 설정 # Set the Random sequence parameters
		itemChances = List[Single]()
		itemChances.Add(4.0)
		itemChances.Add(3.0)
		itemChances.Add(2.0)
		parameters = CSpacePlanningBaseSP.SRandomSequenceParameters.CreateInfinite(itemChances, 1)

		if (res := alg.SetRandomSequenceParameters(parameters)).IsFail():
			ErrorPrint(res, "Failed to set Random sequence parameters.")
			break

		# 앞서 설정된 파라미터 대로 학습 수행 # Perform learning according to previously set parameters
		if (res := alg.Learn()).IsFail():
			ErrorPrint(res, "Failed to learn.")
			break

		# 배치 결과 3D 오브젝트 그룹 취득 # Get the placement result 3D object group
		# 구조: [0, ItemCount) = 배치된 아이템, [ItemCount, end) = 빈(bin) * 2개씩 (속 채움, 외곽선)
		# Structure: [0, ItemCount) = placed items, [ItemCount, end) = bins * 2 each (filled, wireframe)
		flog = CFL3DObjectGroup()
		res, flog = alg.Get3DObject(flog)
		if res.IsFail():
			ErrorPrint(res, "Failed to get 3D object.")
			break

		i32BinCount = alg.GetBinSpecCount()
		i32ItemCount = alg.GetItemSpecCount()

		if (res := view3DResult.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.")
			break

		view3DResult.SetRenderingTransparencyMode(ERenderingTransparencyMode.DepthPeelingOIT)
		view3DResult.SetRenderingResolutionScale(2)

		# 결과 뷰에 아이템 및 Bin 오브젝트 추가 # Push item and bin objects to the result view
		bPushFailed = False
		for i in range(i32ItemCount):
			res, i32ObjIndex = view3DResult.PushObject(flog.GetObjectByIndex(i), -1)
			if res.IsFail():
				ErrorPrint(res, "Failed to push 3D object.")
				bPushFailed = True
				break

			objView3D = view3DResult.GetView3DObject(i32ObjIndex)
			if objView3D is not None:
				objView3D.SetOpacity(0.6)

		if bPushFailed:
			break

		for i in range(i32BinCount):
			res, i32ObjIndex = view3DResult.PushObject(flog.GetObjectByIndex(i32ItemCount + 2 * i), -1)
			if res.IsFail():
				ErrorPrint(res, "Failed to push 3D object.")
				bPushFailed = True
				break

			objFilled = view3DResult.GetView3DObject(i32ObjIndex)
			if objFilled is not None:
				objFilled.SetOpacity(0.2)

			res, i32ObjIndex = view3DResult.PushObject(flog.GetObjectByIndex(i32ItemCount + 2 * i + 1), -1)
			if res.IsFail():
				ErrorPrint(res, "Failed to push 3D object.")
				bPushFailed = True
				break

			objWireframe = view3DResult.GetView3DObject(i32ObjIndex)
			if objWireframe is not None:
				objWireframe.SetOpacity(0.6)

		if bPushFailed:
			break

		# 화면에 출력하기 위해 3D 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 from the 3D view for display
		# 이 객체는 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to the view and does not need to be released separately
		layer3DResult = view3DResult.GetLayer(0)

		flpLeftTop = CFLPoint[Double](0, 0)
		layer3DResult.DrawTextCanvas(flpLeftTop, "Result 3D View", EColor.YELLOW, EColor.BLACK, 20)

		# 결과 정보를 3D 뷰에 텍스트로 표시 # Draw result summary text on the 3D view
		res, f32TotalVolume, f32UsedVolume = alg.GetCurrentVolumeUsage(0, 0.0, 0.0)
		if res.IsFail():
			ErrorPrint(res, "Failed to get volume usage.")
			break

		f32VolumeUsage = 100.0 * f32UsedVolume / f32TotalVolume if f32TotalVolume > 0.0 else 0.0
		strResultInfo = (
			f"Optimal strategy index: {alg.GetOptimalStrategyIndex()}\n"
			f"Volume Usage: {f32VolumeUsage:.1f}%({f32UsedVolume:.1f}/{f32TotalVolume:.1f})"
		)
		layer3DResult.DrawTextCanvas(CFLPoint[Double](0, 25), strResultInfo, EColor.YELLOW, EColor.BLACK, 16)

		# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춰준다.
		# With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen.
		view3DResult.ZoomFit()

		# 이미지 뷰를 갱신 합니다. # Update image view
		view3DResult.Invalidate(True)

		# 3D 뷰가 종료될 때 까지 기다림 # Wait for the 3D view to close
		while view3DResult.IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
    main()
