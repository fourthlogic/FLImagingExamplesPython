# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
import FLImagingCLR.ThreeDim.SpacePlanning as SP

import random

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
	# 3D 뷰 선언 # Declare 3D view
	view3DResult = CGUIView3D()

	res = CResult(EResult.UnknownError)

	while True:
		# 알고리즘 객체 선언 # Declare algorithm object
		alg = CSpacePlanningDynamicSP()

		# Bin spec 설정 # Set the bin spec
		binSpec = SP.SBinSpec[Single](12.0, 9.0, 10.0)

		if (res := alg.AddBinSpec(binSpec)).IsFail():
			ErrorPrint(res, "Failed to add bin spec.")
			break

		# Item spec 설정 (수직축 회전 허용) # Set the item specs (vertical-axis rotation allowed)
		itemSpec1 = SP.SItemSpec[Single](3.0, 3.0, 4.0, 1.0, SP.ERotationAllowance.VerticalAxisOnly)
		itemSpec2 = SP.SItemSpec[Single](4.0, 3.0, 3.0, 1.0, SP.ERotationAllowance.VerticalAxisOnly)
		itemSpec3 = SP.SItemSpec[Single](5.0, 3.0, 2.0, 1.0, SP.ERotationAllowance.VerticalAxisOnly)

		if (res := alg.AddItemSpec(itemSpec1)).IsFail() or \
		   (res := alg.AddItemSpec(itemSpec2)).IsFail() or \
		   (res := alg.AddItemSpec(itemSpec3)).IsFail():
			ErrorPrint(res, "Failed to add item spec.")
			break

		# Random sequence 파라미터 설정 # Set the random sequence parameters
		# itemChances: 각 아이템 타입의 상대적 출현 비율 # Relative appearance ratio of each item type
		# Lookahead: 다음 배치 결정 시 고려할 선택지 수 # Number of candidates to consider for next placement
		itemChances = List[Single]()
		itemChances.Add(4.0)
		itemChances.Add(3.0)
		itemChances.Add(2.0)
		parameters = CSpacePlanningBaseSP.SRandomSequenceParameters.CreateInfinite(itemChances, 1)

		if (res := alg.SetRandomSequenceParameters(parameters)).IsFail():
			ErrorPrint(res, "Failed to set random sequence parameters.")
			break

		alg.EnableFallbackPolicy(True)

		# 앞서 설정된 파라미터 대로 학습 수행 # Perform learning according to previously set parameters
		if (res := alg.Learn()).IsFail():
			ErrorPrint(res, "Failed to learn.")
			break

		# 학습된 전략 중 최적 전략 선택 # Select the optimal strategy among learned strategies
		optimalStrategyId = alg.GetOptimalStrategyId()

		if (res := alg.SelectStrategy(optimalStrategyId)).IsFail():
			ErrorPrint(res, "Failed to select strategy.")
			break

		converter = CSpacePlanningCoordinateConverterSP()
		res, converter = InitializeCoordinateConverter(alg, converter)
		if res.IsFail():
			ErrorPrint(res, "Failed to initialize the coordinate converter.")
			break

		flogBins = CFL3DObjectGroup()
		res, flogBins = converter.MakeBinObjectGroup(flogBins)
		if res.IsFail():
			ErrorPrint(res, "Failed to build world-space bin objects.")
			break

		print(f"Optimal strategy: group={optimalStrategyId.eGroup}, id={optimalStrategyId.i32IDInStrategy}")

		# 3D 뷰 생성 # Create 3D view
		if (res := view3DResult.Create(600, 0, 1200, 600)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.")
			break

		view3DResult.SetRenderingTransparencyMode(ERenderingTransparencyMode.DepthPeelingOIT)
		view3DResult.SetRenderingResolutionScale(2)

		i32BinCount = alg.GetBinSpecCount()
		i32ItemCount = alg.GetItemSpecCount()

		# 타이틀은 layer 0에 한 번만 그림 # Draw title once on layer 0
		# 매 스텝마다 갱신되는 상태 텍스트는 layer 1을 Clear 후 재작성 # Per-step status goes on layer 1, cleared each step
		view3DResult.GetLayer(0).DrawTextCanvas(CFLPoint[Double](0, 0), "Dynamic SP - Interactive Placement", EColor.YELLOW, EColor.BLACK, 20)

		# 인터랙티브 모드 실행 # Run in interactive mode
		if (res := alg.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break

		# 아이템 도착 시뮬레이션 (컨베이어 벨트 상황) # Simulate item arrival (conveyor belt scenario)
		# 아이템 타입을 무작위로 생성하여 빈이 꽉 찰 때까지 계속 배치
		# Randomly generate item types and keep placing until the bin is full (EResult.FullOfCapacity)
		placementResults = List[CSpacePlanningBaseSP.SPlacementInfo]()

		i32ArrivalIdx = 0
		i32PlacedCount = 0

		bLoopFailed = False

		while True:
			if not view3DResult.IsAvailable():
				break

			i32ItemType = random.randrange(0, i32ItemCount)

			# 아이템을 대기열에 추가하고 권장 위치에 자동 배치
			# Push item to queue and automatically place it at the recommended position
			placement = None

			res, placement = alg.PushAndPlace(i32ItemType, True, placement)

			i32ArrivalIdx += 1

			if res.IsFail():
				if res == CResult(EResult.FullOfCapacity):
					# 빈이 꽉 참 — 정상 종료 # Bin is full — normal termination
					print(f"Arrival {i32ArrivalIdx}: bin is full. Stopping.")
					break
				# 예상치 못한 오류 # Unexpected error
				ErrorPrint(res, "Failed to push and place.")
				bLoopFailed = True
				break

			i32PlacedCount += 1
			placementResults.Add(placement)

			tpWorldPosition = TPoint3[Single]()
			res, tpWorldPosition = converter.Convert(placement, tpWorldPosition)
			if res.IsFail():
				ErrorPrint(res, "Failed to convert placement coordinates.")
				bLoopFailed = True
				break

			print(
				f"Arrival {i32ArrivalIdx}: placed item type {placement.i32ItemIndex} at bin {placement.i32BinIndex} "
				f"(rotation={int(placement.eRotation)}, bin pos=[{placement.tpPosition.x:.1f}, {placement.tpPosition.y:.1f}, {placement.tpPosition.z:.1f}], "
				f"world center=[{tpWorldPosition.x:.1f}, {tpWorldPosition.y:.1f}, {tpWorldPosition.z:.1f}])"
			)

			flogItems = CFL3DObjectGroup()
			res, flogItems = converter.MakeItemObjectGroup(placementResults, flogItems)
			if res.IsFail():
				ErrorPrint(res, "Failed to build world-space item objects.")
				bLoopFailed = True
				break

			view3DResult.Lock()

			# 매 스텝마다 world-space 오브젝트로 뷰를 재구성
			# Rebuild the view with world-space objects on each step
			view3DResult.ClearObjects()

			for i in range(i32PlacedCount):
				res, i32ObjIndex = view3DResult.PushObject(flogItems.GetObjectByIndex(i), -1)
				obj = view3DResult.GetView3DObject(i32ObjIndex)
				if obj is not None:
					obj.SetOpacity(0.6)

			for i in range(i32BinCount):
				res, i32ObjIndex = view3DResult.PushObject(flogBins.GetObjectByIndex(i), -1)
				objFilled = view3DResult.GetView3DObject(i32ObjIndex)
				if objFilled is not None:
					objFilled.SetOpacity(0.2)

			# 상태 텍스트는 layer 1에 매 스텝 Clear 후 재작성 # Clear layer 1 each step and redraw status text
			# 이 객체는 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to the view and does not need to be released separately
			layer3DStatus = view3DResult.GetLayer(1)
			layer3DStatus.Clear()

			res, f32TotalVolume, f32UsedVolume = alg.GetCurrentVolumeUsage(0, 0.0, 0.0)
			f32VolumeUsage = 100.0 * f32UsedVolume / f32TotalVolume if f32TotalVolume > 0.0 else 0.0

			strStatus = (
				f"Arrival {i32ArrivalIdx}  |  Placed: {i32PlacedCount}  |  Volume Usage: {f32VolumeUsage:.1f}% ({f32UsedVolume:.1f} / {f32TotalVolume:.1f})\n"
				f"World-space rendering enabled"
			)

			layer3DStatus.DrawTextCanvas(CFLPoint[Double](0, 25), strStatus, EColor.YELLOW, EColor.BLACK, 16)

			# 첫 아이템 배치 시 카메라를 전체에 맞게 조정 # Fit camera to all objects on first placement
			if i32PlacedCount == 1:
				view3DResult.ZoomFit()

			view3DResult.Unlock()

			# 이미지 뷰를 갱신 합니다. # Update image view
			view3DResult.Invalidate(True)

			# 배치 과정을 눈으로 확인할 수 있도록 잠시 대기 # Pause briefly so the placement process is visible
			CThreadUtilities.Sleep(600)

		if bLoopFailed:
			break

		if not view3DResult.IsAvailable():
			break

		# 최종 결과 요약 출력 # Print final result summary
		res, f32TotalVolume, f32UsedVolume = alg.GetCurrentVolumeUsage(0, 0.0, 0.0)
		f32VolumeUsage = 100.0 * f32UsedVolume / f32TotalVolume if f32TotalVolume > 0.0 else 0.0

		layer3DStatus = view3DResult.GetLayer(1)
		layer3DStatus.Clear()

		strFinalInfo = (
			f"Done  |  Arrivals: {i32ArrivalIdx}  |  Placed: {i32PlacedCount}  |  "
			f"Volume Usage: {f32VolumeUsage:.1f}% ({f32UsedVolume:.1f} / {f32TotalVolume:.1f})"
		)

		layer3DStatus.DrawTextCanvas(CFLPoint[Double](0, 25), strFinalInfo, EColor.YELLOW, EColor.BLACK, 16)

		view3DResult.Invalidate(True)

		# 3D 뷰가 종료될 때 까지 기다림 # Wait for the 3D view to close
		while view3DResult.IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
    main()
