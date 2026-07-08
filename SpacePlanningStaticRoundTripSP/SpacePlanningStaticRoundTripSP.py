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

# SpacePlanningStaticSP 고급 예제: top item 만 한 개씩 반대편 상자로 옮긴 뒤 다시 되돌립니다.
# Advanced SpacePlanningStaticSP example: move only top-pickable items to the other bin and back.
# 일부 물품은 XZ 평면 회전, 일부 물품은 모든 축 회전을 허용합니다.
# Some items allow XZ-plane rotation, and one item allows full axis rotation.


# 배치된 물품 하나. tpMin/tpMax 는 회전 적용 후 영역 # Placed item; tpMin/tpMax store rotated bounds
class SItemInstance:
	def __init__(self):
		self.i32ItemSpecIndex = 0
		self.eRotation = None
		self.tpMin = None
		self.tpMax = None


def GetRotatedItemSize(itemSpec, eRotation):
	if eRotation == SP.EAxisRotation.XYZ:
		return TPoint3[Single](itemSpec.width, itemSpec.height, itemSpec.depth)
	if eRotation == SP.EAxisRotation.ZYX:
		return TPoint3[Single](itemSpec.depth, itemSpec.height, itemSpec.width)
	if eRotation == SP.EAxisRotation.XZY:
		return TPoint3[Single](itemSpec.width, itemSpec.depth, itemSpec.height)
	if eRotation == SP.EAxisRotation.ZXY:
		return TPoint3[Single](itemSpec.depth, itemSpec.width, itemSpec.height)
	if eRotation == SP.EAxisRotation.YXZ:
		return TPoint3[Single](itemSpec.height, itemSpec.width, itemSpec.depth)
	if eRotation == SP.EAxisRotation.YZX:
		return TPoint3[Single](itemSpec.height, itemSpec.depth, itemSpec.width)

	return TPoint3[Single](itemSpec.width, itemSpec.height, itemSpec.depth)


def MakeItemInstance(listItemSpecs, placement):
	tpSize = GetRotatedItemSize(listItemSpecs[placement.i32ItemIndex], placement.eRotation)

	instance = SItemInstance()
	instance.i32ItemSpecIndex = placement.i32ItemIndex
	instance.eRotation = placement.eRotation
	instance.tpMin = placement.tpPosition
	instance.tpMax = TPoint3[Single](
		placement.tpPosition.x + tpSize.x,
		placement.tpPosition.y + tpSize.y,
		placement.tpPosition.z + tpSize.z
	)

	return instance


# lower 위에 upper 가 얹혀 있는지 판정 # Check whether upper rests on lower
def IsBelow(lower, upper):
	bXOverlap = (lower.tpMin.x < upper.tpMax.x) and (upper.tpMin.x < lower.tpMax.x)
	bZOverlap = (lower.tpMin.z < upper.tpMax.z) and (upper.tpMin.z < lower.tpMax.z)
	bUpperIsAbove = upper.tpMin.y >= lower.tpMax.y - 0.001

	return bXOverlap and bZOverlap and bUpperIsAbove


# 한 상자의 배치 상태와 상단 물품 판정용 listCountAbove # Bin placement state and listCountAbove for top-item checks
class SBinState:
	def __init__(self):
		self.listItems = []
		self.listCountAbove = []

	def Clear(self):
		self.listItems = []
		self.listCountAbove = []

	# 물품을 추가하고 아래 물품들의 count 갱신 # Add an item and update count of items below it
	def AddInstance(self, instance):
		for i in range(len(self.listItems)):
			if IsBelow(self.listItems[i], instance):
				self.listCountAbove[i] += 1

		self.listItems.append(instance)
		self.listCountAbove.append(0)

	# 지정 타입의 상단 물품을 제거하고 새로 드러난 상단 인덱스를 반환 # Remove one top item and return newly exposed tops
	def RemovePickableOfType(self, i32ItemSpecIndex, listNewlyPickable):
		i32Found = -1
		for j in range(len(self.listItems)):
			if self.listItems[j].i32ItemSpecIndex == i32ItemSpecIndex and self.listCountAbove[j] == 0:
				i32Found = j
				break

		if i32Found < 0:
			return CResult(EResult.DoesNotExist)

		removed = self.listItems[i32Found]
		del self.listItems[i32Found]
		del self.listCountAbove[i32Found]

		for i in range(len(self.listItems)):
			if IsBelow(self.listItems[i], removed):
				i32Old = self.listCountAbove[i]
				self.listCountAbove[i] -= 1

				if i32Old == 1:
					listNewlyPickable.append(i)

		return CResult(EResult.OK)


# 캐시가 기준 파일보다 최신인지 확인 # Check whether the cache is newer than the reference file
def IsCacheUpToDate(strCache, strReference):
	if not os.path.exists(strCache):
		return False

	if not os.path.exists(strReference):
		return False

	return os.path.getmtime(strCache) > os.path.getmtime(strReference)


# 동일 사양으로 알고리즘 구성 및 학습 # Configure and learn with identical specs
def ConfigureAndLearn(alg, binSpec, listItemSpecs, listItemCounts):
	res = CResult(EResult.UnknownError)

	while True:
		# 재학습 시 사양 중복 추가 방지 # Avoid duplicated specs on re-learn
		alg.Clear()

		if (res := alg.AddBinSpec(binSpec)).IsFail():
			break

		bFailed = False
		for itemSpec in listItemSpecs:
			if (res := alg.AddItemSpec(itemSpec)).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		itemCounts = List[Int32]()
		for i32Count in listItemCounts:
			itemCounts.Add(i32Count)

		parameters = SP.SStaticListParameters(itemCounts)
		if (res := alg.SetStaticListParameters(parameters)).IsFail():
			break

		res = alg.Learn()
		break

	return res


# 캐시가 유효하면 Load, 아니면 Learn 후 Save # Load a valid cache, otherwise learn and save
def LearnOrLoadModel(alg, strCache, strSource, binSpec, listItemSpecs, listItemCounts):
	res = CResult(EResult.UnknownError)

	# 캐시가 소스보다 최신이면 학습 결과를 불러옴 # Load the learned result from a newer cache
	if IsCacheUpToDate(strCache, strSource):
		res = alg.Load(strCache)

		# PartialOK 는 파라미터만 로드된 상태이므로 재학습 필요 # PartialOK means parameters were loaded but learning is required
		if res.IsOK() and alg.IsLearned():
			print(f"Loaded cached model: {strCache}")
			return res

	# ConfigureAndLearn 이 Clear 하므로 부분 로드 상태여도 안전 # ConfigureAndLearn clears any partial-load state
	if (res := ConfigureAndLearn(alg, binSpec, listItemSpecs, listItemCounts)).IsFail():
		return res

	# 저장 실패는 예제 진행에 치명적이지 않으므로 경고만 출력 # Save failure is non-fatal for this example
	resSave = alg.Save(strCache)
	if resSave.IsFail():
		print(f"Warning: failed to cache model ({strCache}): {resSave.GetString()}")
	else:
		print(f"Learned and cached model: {strCache}")

	return res


# 학습된 알고리즘에서 world 좌표 변환기 구성 # Build a world-space coordinate converter from a learned algorithm
def SetupConverter(alg, converter, f32WorldXOffset):
	res = CResult(EResult.UnknownError)

	while True:
		res, converter = alg.GetCoordinateConverter(converter)
		if res.IsFail():
			break

		tpWorldPivot = TPoint3[Single](f32WorldXOffset, 0.0, 0.0)
		tpBinPivot = TPoint3[Single](0.0, 0.0, 0.0)
		tpDirectionZ = TPoint3[Single](0.0, 0.0, 1.0)
		tpUpY = TPoint3[Single](0.0, 1.0, 0.0)

		if (res := converter.SetBinTransform(0, tpWorldPivot, tpBinPivot, tpDirectionZ, tpUpY)).IsFail():
			break

		i32ItemCount = alg.GetItemSpecCount()
		bFailed = False
		for i in range(i32ItemCount):
			if (res := converter.SetItemPivotNormalized(i, TPoint3[Single](0.5, 0.5, 0.5))).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		res = converter.Learn()
		break

	return res, converter


# 지정한 상자 상태를 뷰에 그림 # Draw a bin state into the view
def PushBinToView(view3D, converter, bin):
	res = CResult(EResult.UnknownError)

	while True:
		flogBin = CFL3DObjectGroup()
		res, flogBin = converter.MakeBinObjectGroup(flogBin)
		if res.IsFail():
			break

		res, i32BinObjIndex = view3D.PushObject(flogBin.GetObjectByIndex(0), -1)
		binObj = view3D.GetView3DObject(i32BinObjIndex)
		if binObj is not None:
			binObj.SetOpacity(0.15)

		if len(bin.listItems) == 0:
			res = CResult(EResult.OK)
			break

		listPlacements = List[SP.SPlacementInfo]()
		for i in range(len(bin.listItems)):
			placement = SP.SPlacementInfo()
			placement.i32BinIndex = 0
			placement.i32ItemIndex = bin.listItems[i].i32ItemSpecIndex
			placement.eRotation = bin.listItems[i].eRotation
			placement.tpPosition = bin.listItems[i].tpMin
			listPlacements.Add(placement)

		flogItems = CFL3DObjectGroup()
		res, flogItems = converter.MakeItemObjectGroup(listPlacements, flogItems)
		if res.IsFail():
			break

		for i in range(len(bin.listItems)):
			res, i32ObjIndex = view3D.PushObject(flogItems.GetObjectByIndex(i), -1)
			obj = view3D.GetView3DObject(i32ObjIndex)
			if obj is not None:
				obj.SetOpacity(0.6)

		res = CResult(EResult.OK)
		break

	return res


# source 의 상단 물품을 dstAlg 추천 위치로 모두 이송 # Move all top-pickable source items to destination recommendations
def TransferAllItems(srcBin, dstAlg, dstBin, listItemSpecs, strLabel, fnOnStep):
	res = CResult(EResult.UnknownError)

	if (res := dstAlg.ClearInteractiveStates()).IsFail():
		return res

	if (res := dstAlg.Execute()).IsFail():
		return res

	# 현재 상단 물품을 목적지 대기열에 추가 # Push currently top-pickable items into the destination queue
	for i in range(len(srcBin.listItems)):
		if srcBin.listCountAbove[i] != 0:
			continue

		if (res := dstAlg.PushItem(srcBin.listItems[i].i32ItemSpecIndex, 1)).IsFail():
			return res

	i32Step = 0
	while len(srcBin.listItems) > 0:
		# 목적지 추천 물품/위치 조회 # Get the next destination recommendation
		placement = SP.SPlacementInfo()
		res, placement = dstAlg.GetRecommendedNextPlacement(placement)
		if res.IsFail():
			break

		# 같은 타입의 상단 물품 제거 # Remove a top item of the recommended type
		listNewlyPickable = []
		if (res := srcBin.RemovePickableOfType(placement.i32ItemIndex, listNewlyPickable)).IsFail():
			return res

		bFailed = False
		for i32Idx in listNewlyPickable:
			if (res := dstAlg.PushItem(srcBin.listItems[i32Idx].i32ItemSpecIndex, 1)).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		# 목적지에 추천 위치 그대로 배치 # Place into the destination at the recommended position
		if (res := dstAlg.AddPlacement(placement)).IsFail():
			return res

		dstBin.AddInstance(MakeItemInstance(listItemSpecs, placement))

		i32Step += 1
		print(
			f"[{strLabel}] step {i32Step:2d}: picked item type {placement.i32ItemIndex} "
			f"-> placed at bin {placement.i32BinIndex} "
			f"[{placement.tpPosition.x:.1f}, {placement.tpPosition.y:.1f}, {placement.tpPosition.z:.1f}]  "
			f"(source left: {len(srcBin.listItems)})"
		)

		if fnOnStep is not None:
			fnOnStep()

	return res


# 메인 함수 # Main function
def main():
	# 3D 뷰 선언 # Declare 3D view
	view3DResult = CGUIView3D()

	res = CResult(EResult.UnknownError)

	while True:
		# 물품 사양과 개수 설정 # Set item specs and counts
		listItemSpecs = [
			SP.SItemSpec[Single](3.0, 3.0, 4.0, 1.0, SP.ERotationAllowance.VerticalAxisOnly),
			SP.SItemSpec[Single](2.0, 4.3, 5.9, 1.0, SP.ERotationAllowance.VerticalAxisOnly),
			SP.SItemSpec[Single](4.0, 3.0, 3.5, 1.0, SP.ERotationAllowance.VerticalAxisOnly),
			SP.SItemSpec[Single](5.0, 3.0, 2.5, 1.0, SP.ERotationAllowance.FullRotation)
		]
		listItemCounts = [4, 3, 3, 3]

		binSpecA = SP.SBinSpec[Single](9.0, 12.0, 10.0)
		binSpecB = SP.SBinSpec[Single](10.0, 11.0, 9.0)

		# A/B 상자를 서로 다른 사양으로 학습 # Learn bins A/B with different specs
		algA = CSpacePlanningStaticSP()
		algB = CSpacePlanningStaticSP()

		# 모델 캐시 파일 설정 # Set model cache files
		strSource = os.path.abspath(__file__)
		strCacheA = f"SpacePlanningStaticRoundTrip_A.{algA.GetFileExtension()}"
		strCacheB = f"SpacePlanningStaticRoundTrip_B.{algB.GetFileExtension()}"

		if (res := LearnOrLoadModel(algA, strCacheA, strSource, binSpecA, listItemSpecs, listItemCounts)).IsFail():
			ErrorPrint(res, "Failed to prepare model for bin A.")
			break

		if (res := LearnOrLoadModel(algB, strCacheB, strSource, binSpecB, listItemSpecs, listItemCounts)).IsFail():
			ErrorPrint(res, "Failed to prepare model for bin B.")
			break

		# A/B 를 world 좌표계에서 나란히 배치 # Place A/B side by side in world coordinates
		converterA = CSpacePlanningCoordinateConverterSP()
		converterB = CSpacePlanningCoordinateConverterSP()

		res, converterA = SetupConverter(algA, converterA, 0.0)
		if res.IsFail():
			ErrorPrint(res, "Failed to set up coordinate converter A.")
			break

		res, converterB = SetupConverter(algB, converterB, 18.0)
		if res.IsFail():
			ErrorPrint(res, "Failed to set up coordinate converter B.")
			break

		# 학습 결과로 A 의 초기 적재 상태 구성 # Build initial bin A state from learned placements
		binA = SBinState()
		binB = SBinState()

		listLearnedA = List[SP.SPlacementInfo]()
		res, listLearnedA = algA.GetLearnedPlacements(listLearnedA)
		if res.IsFail():
			ErrorPrint(res, "Failed to get learned placements for bin A.")
			break

		for i in range(listLearnedA.Count):
			p = listLearnedA[i]
			binA.AddInstance(MakeItemInstance(listItemSpecs, p))

		# 3D 뷰 생성 # Create 3D view
		if (res := view3DResult.Create(600, 0, 1300, 650)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.")
			break

		view3DResult.SetRenderingTransparencyMode(ERenderingTransparencyMode.DepthPeelingOIT)
		view3DResult.SetRenderingResolutionScale(2)

		view3DResult.GetLayer(0).DrawTextCanvas(CFLPoint[Double](0, 0), "Static SP Round Trip - pick top items only", EColor.YELLOW, EColor.BLACK, 20)

		bZoomFitted = False

		# 매 스텝 두 상자 다시 그리기 # Redraw both bins on each step
		def fnRender():
			nonlocal bZoomFitted

			if not view3DResult.IsAvailable():
				return

			view3DResult.Lock()
			view3DResult.ClearObjects()

			PushBinToView(view3DResult, converterA, binA)
			PushBinToView(view3DResult, converterB, binB)

			if not bZoomFitted:
				view3DResult.ZoomFit()
				bZoomFitted = True

			view3DResult.Unlock()
			view3DResult.Invalidate(True)

			CThreadUtilities.Sleep(500)

		# 초기 상태 표시 # Show the initial state
		fnRender()

		# A -> B 이송 # Transfer A -> B
		print("Starting transfer A->B.")
		if (res := TransferAllItems(binA, algB, binB, listItemSpecs, "A->B", fnRender)).IsFail():
			if view3DResult.IsAvailable():
				ErrorPrint(res, "Transfer A->B failed.")
			break

		print("A->B complete. Switching to B->A after 2 seconds.")
		CThreadUtilities.Sleep(2000)

		# B -> A 이송 (왕복) # Transfer B -> A (round trip)
		print("Starting transfer B->A.")
		if (res := TransferAllItems(binB, algA, binA, listItemSpecs, "B->A", fnRender)).IsFail():
			if view3DResult.IsAvailable():
				ErrorPrint(res, "Transfer B->A failed.")
			break

		print("Round trip complete.")

		# 3D 뷰가 종료될 때 까지 기다림 # Wait for the 3D view to close
		while view3DResult.IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
	main()
