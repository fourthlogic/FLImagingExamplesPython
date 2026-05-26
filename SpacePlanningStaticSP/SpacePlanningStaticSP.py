# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
import FLImagingCLR.ThreeDim.SpacePlanning as SP


# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


def InitializeCoordinateConverter(alg, converter):
	res = CResult(EResult.UnknownError)

	while True:
		res, converter = alg.GetCoordinateConverter(converter)
		if res.IsFail():
			break

		i32BinCount = alg.GetBinSpecCount()
		bFailedInLoop = False
		for i in range(i32BinCount):
			tpWorldPivot = TPoint3[Single](16.0 * i, 0.0, 0.0)
			tpBinPivot = TPoint3[Single](0.0, 0.0, 0.0)
			tpDirectionZ = TPoint3[Single](0.03, 0.0, 1.0)
			tpUpY = TPoint3[Single](0.0, 1.0, 0.3)

			if (res := converter.SetBinTransform(i, tpWorldPivot, tpBinPivot, tpDirectionZ, tpUpY)).IsFail():
				bFailedInLoop = True
				break

		if bFailedInLoop:
			break

		i32ItemCount = alg.GetItemSpecCount()
		for i in range(i32ItemCount):
			if (res := converter.SetItemPivotNormalized(i, TPoint3[Single](0.5, 0.5, 0.5))).IsFail():
				bFailedInLoop = True
				break

		if bFailedInLoop:
			break

		res = converter.Learn()
		break

	return res, converter


# 메인 함수 # Main function
def main():
	# 3D 뷰 선언 # Declare 3D views
	view3DResult = CGUIView3D()

	res = CResult(EResult.UnknownError)

	while True:
		# 알고리즘 객체 선언 # Declare algorithm object
		alg = CSpacePlanningStaticSP()

		# Bin spec 설정 # Set the bin spec
		binSpec = SP.SBinSpec[Single](12.0, 9.0, 10.0)

		if (res := alg.AddBinSpec(binSpec)).IsFail():
			ErrorPrint(res, "Failed to add bin spec.")
			break

		# Item spec 설정 (회전 없음) # Set the item specs (no rotation)
		itemSpec1 = SP.SItemSpec[Single](3.0, 3.0, 4.0, 1.0, SP.ERotationAllowance.NoRotation)
		itemSpec2 = SP.SItemSpec[Single](4.0, 3.0, 3.0, 1.0, SP.ERotationAllowance.NoRotation)
		itemSpec3 = SP.SItemSpec[Single](5.0, 3.0, 2.0, 1.0, SP.ERotationAllowance.NoRotation)

		if (res := alg.AddItemSpec(itemSpec1)).IsFail() or \
		   (res := alg.AddItemSpec(itemSpec2)).IsFail() or \
		   (res := alg.AddItemSpec(itemSpec3)).IsFail():
			ErrorPrint(res, "Failed to add item spec.")
			break

		# Static list 파라미터 설정 # Set the static list parameters
		itemCounts = List[Int32]()
		itemCounts.Add(8)
		itemCounts.Add(8)
		itemCounts.Add(4)
		parameters = CSpacePlanningBaseSP.SStaticListParameters(itemCounts)

		if (res := alg.SetStaticListParameters(parameters)).IsFail():
			ErrorPrint(res, "Failed to set static list parameters.")
			break

		print("Learning...", end='')

		# 앞서 설정된 파라미터 대로 학습 수행 # Perform learning according to previously set parameters
		if (res := alg.Learn()).IsFail():
			ErrorPrint(res, "Failed to learn.")
			break

		converter = CSpacePlanningCoordinateConverterSP()
		res, converter = InitializeCoordinateConverter(alg, converter)
		if res.IsFail():
			ErrorPrint(res, "Failed to initialize the coordinate converter.")
			break

		placementResults = List[CSpacePlanningBaseSP.SPlacementInfo]()
		res, placementResults = alg.GetLearnedPlacements(placementResults)
		if res.IsFail():
			ErrorPrint(res, "Failed to get learned placements.")
			break

		flogBins = CFL3DObjectGroup()
		flogItems = CFL3DObjectGroup()

		res, flogBins = converter.MakeBinObjectGroup(flogBins)
		if res.IsFail():
			ErrorPrint(res, "Failed to build world-space 3D objects.")
			break

		res, flogItems = converter.MakeItemObjectGroup(placementResults, flogItems)
		if res.IsFail():
			ErrorPrint(res, "Failed to build world-space 3D objects.")
			break

		bConvertFailed = False
		for i in range(placementResults.Count):
			tpWorldPosition = TPoint3[Single]()
			res, tpWorldPosition = converter.Convert(placementResults[i], tpWorldPosition)
			if res.IsFail():
				ErrorPrint(res, "Failed to convert placement coordinates.")
				bConvertFailed = True
				break

			print(
				f"Placement {i}: bin {placementResults[i].i32BinIndex}, item {placementResults[i].i32ItemIndex} "
				f"-> world center [{tpWorldPosition.x:.1f}, {tpWorldPosition.y:.1f}, {tpWorldPosition.z:.1f}]"
			)

		if bConvertFailed:
			break

		i32BinCount = alg.GetBinSpecCount()
		i32PlacedCount = placementResults.Count

		if (res := view3DResult.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.")
			break

		view3DResult.SetRenderingTransparencyMode(ERenderingTransparencyMode.DepthPeelingOIT)
		view3DResult.SetRenderingResolutionScale(2)

		# 결과 뷰에 world-space 아이템 및 bin 오브젝트 추가
		# Push world-space item and bin objects to the result view
		bPushFailed = False
		for i in range(i32PlacedCount):
			res, i32ObjIndex = view3DResult.PushObject(flogItems.GetObjectByIndex(i), -1)
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
			res, i32ObjIndex = view3DResult.PushObject(flogBins.GetObjectByIndex(i), -1)
			if res.IsFail():
				ErrorPrint(res, "Failed to push 3D object.")
				bPushFailed = True
				break

			objFilled = view3DResult.GetView3DObject(i32ObjIndex)
			if objFilled is not None:
				objFilled.SetOpacity(0.2)

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
		optimalStrategyId = alg.GetOptimalStrategyId()
		strResultInfo = (
			f"Optimal strategy: group={optimalStrategyId.eGroup}, id={optimalStrategyId.i32IDInStrategy}\n"
			f"Volume Usage: {f32VolumeUsage:.1f}%({f32UsedVolume:.1f}/{f32TotalVolume:.1f})\n"
			f"Coordinate converter: world-space center pivot"
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
