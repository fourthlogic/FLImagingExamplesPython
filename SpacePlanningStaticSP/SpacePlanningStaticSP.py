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
	arrView3DResults = [CGUIView3D() for _ in range(3)]

	res = CResult(EResult.UnknownError)

	while True:
		# 알고리즘 객체 선언 # Declare algorithm object
		alg = CSpacePlanningStaticSP()

		# Bin spec 설정 # Set the bin spec
		binSpec = SP.SBinSpec[Single](8.0, 6.0, 8.0)

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
		itemCounts.Add(4)
		itemCounts.Add(3)
		itemCounts.Add(2)
		parameters = SP.SStaticListParameters(itemCounts)

		if (res := alg.SetStaticListParameters(parameters)).IsFail():
			ErrorPrint(res, "Failed to set static list parameters.")
			break

		# 같은 item 수량을 직접 순서, 순서 무관, seed shuffle의 세 방식으로 평가
		# Evaluate the same item counts as a direct sequence, order-free supply, and seeded shuffle
		sequenceA = List[Int32]()
		for i32ItemIndex in [0, 1, 2, 0, 1, 2, 0, 1, 0]:
			sequenceA.Add(i32ItemIndex)

		evaluationCaseA = SP.CScoreEvaluationCaseSequenceSP(sequenceA, 1)
		evaluationCaseB = SP.CScoreEvaluationCaseOrderFreeSP(itemCounts)
		evaluationCaseC = SP.CScoreEvaluationCaseShuffledSP(itemCounts, 2, 20260729)

		if (res := alg.AddScoreEvaluationCase(evaluationCaseA, "Alternating sequence")).IsFail() or \
		   (res := alg.AddScoreEvaluationCase(evaluationCaseB, "Order-free counts")).IsFail() or \
		   (res := alg.AddScoreEvaluationCase(evaluationCaseC, "Seeded shuffle")).IsFail() or \
		   (res := alg.EnableImmediateScoreEvaluation(False)).IsFail():
			ErrorPrint(res, "Failed to configure score-evaluation cases.")
			break

		print("Learning...")

		# Learn은 전략을 준비하고, EvaluateScore mode의 Execute가 같은 case들을 평가
		# Learn prepares strategies; Execute in EvaluateScore mode evaluates the same cases
		if (res := alg.Learn()).IsFail():
			ErrorPrint(res, "Failed to learn.")
			break

		if (res := alg.SetExecutionMode(SP.EExecutionMode.EvaluateScore)).IsFail() or \
		   (res := alg.Execute()).IsFail():
			ErrorPrint(res, "Failed to evaluate scores.")
			break

		if not alg.HasValidScoreEvaluation():
			ErrorPrint(CResult(EResult.NoResult), "Score evaluation did not commit results.")
			break

		# 한 고정 strategy에 대해 case별 요약과 실제 배치 순서를 보관
		# Keep each case summary and actual placement order for one fixed strategy
		evaluationStrategyId = SP.SSpacePlanningStrategyId(SP.EStrategyGroup.Search, 0)
		i32EvaluationCaseCount = alg.GetScoreEvaluationCaseCount()
		if i32EvaluationCaseCount != 3:
			ErrorPrint(CResult(EResult.NoResult), "Expected three committed score-evaluation cases.")
			break

		arrCaseInfos = [SP.SScoreEvaluationCaseInfo() for _ in range(3)]
		arrEvaluationResults = [SP.SScoreEvaluationResult() for _ in range(3)]
		bResultFailed = False

		for i in range(i32EvaluationCaseCount):
			res, arrCaseInfos[i] = alg.GetScoreEvaluationCaseInfo(i, arrCaseInfos[i])
			if res.IsFail():
				ErrorPrint(res, "Failed to get score-evaluation results.")
				bResultFailed = True
				break

			res, arrEvaluationResults[i] = alg.GetScoreEvaluationResult(
				evaluationStrategyId,
				arrCaseInfos[i].u64CaseId,
				arrEvaluationResults[i]
			)
			if res.IsFail():
				ErrorPrint(res, "Failed to get score-evaluation results.")
				bResultFailed = True
				break

			print(
				f"Case {chr(ord('A') + i)} - {arrCaseInfos[i].strName}: placed "
				f"{arrEvaluationResults[i].i32PlacedItemCount}/{arrCaseInfos[i].i32TotalItemCount}, "
				f"utilization {arrEvaluationResults[i].f64VolumeUtilization * 100.0:.2f}%"
			)

		if bResultFailed:
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

		arrFlogItems = [CFL3DObjectGroup() for _ in range(3)]
		bConvertFailed = False
		for i in range(i32EvaluationCaseCount):
			res, arrFlogItems[i] = converter.MakeItemObjectGroup(arrEvaluationResults[i].lstPlacements, arrFlogItems[i])
			if res.IsFail():
				ErrorPrint(res, "Failed to build world-space item objects.")
				bConvertFailed = True
				break

			print(f"\nCase {chr(ord('A') + i)} placements:")
			for j in range(arrEvaluationResults[i].lstPlacements.Count):
				tpWorldPosition = TPoint3[Single]()
				res, tpWorldPosition = converter.Convert(arrEvaluationResults[i].lstPlacements[j], tpWorldPosition)
				if res.IsFail():
					ErrorPrint(res, "Failed to convert placement coordinates.")
					bConvertFailed = True
					break

				print(
					f"  {j}: bin {arrEvaluationResults[i].lstPlacements[j].i32BinIndex}, "
					f"item {arrEvaluationResults[i].lstPlacements[j].i32ItemIndex} "
					f"-> world center [{tpWorldPosition.x:.1f}, {tpWorldPosition.y:.1f}, {tpWorldPosition.z:.1f}]"
				)

			if bConvertFailed:
				break

		if bConvertFailed:
			break

		i32BinCount = alg.GetBinSpecCount()
		i32ViewWidth = 600
		i32ViewHeight = 500

		bPushFailed = False
		for i in range(i32EvaluationCaseCount):
			view3DResult = arrView3DResults[i]
			info = arrCaseInfos[i]
			evaluationResult = arrEvaluationResults[i]
			i32PlacedCount = evaluationResult.lstPlacements.Count

			if (res := view3DResult.Create(i32ViewWidth * i, 0, i32ViewWidth * (i + 1), i32ViewHeight)).IsFail():
				ErrorPrint(res, "Failed to create a 3D view.")
				bPushFailed = True
				break

			view3DResult.SetRenderingTransparencyMode(ERenderingTransparencyMode.DepthPeelingOIT)
			view3DResult.SetRenderingResolutionScale(2)

			# 결과 뷰에 해당 case의 world-space 아이템 및 bin 오브젝트 추가
			# Push this case's world-space item and bin objects to its result view
			for j in range(i32PlacedCount):
				res, i32ObjIndex = view3DResult.PushObject(arrFlogItems[i].GetObjectByIndex(j), -1)
				if res.IsFail():
					ErrorPrint(res, "Failed to push 3D object.")
					bPushFailed = True
					break

				objView3D = view3DResult.GetView3DObject(i32ObjIndex)
				if objView3D is not None:
					objView3D.SetOpacity(0.6)

			if bPushFailed:
				break

			for j in range(i32BinCount):
				res, i32ObjIndex = view3DResult.PushObject(flogBins.GetObjectByIndex(j), -1)
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
			layer3DResult.DrawTextCanvas(
				CFLPoint[Double](0, 0),
				f"Case {chr(ord('A') + i)} - {info.strName}",
				EColor.YELLOW,
				EColor.BLACK,
				20
			)

			# 결과 정보를 3D 뷰에 텍스트로 표시 # Draw result summary text on the 3D view
			strResultInfo = (
				f"Evaluation strategy: group={evaluationStrategyId.eGroup}, id={evaluationStrategyId.i32IDInStrategy}\n"
				f"Placed items: {evaluationResult.i32PlacedItemCount}/{info.i32TotalItemCount}\n"
				f"Volume utilization: {evaluationResult.f64VolumeUtilization * 100.0:.1f}%\n"
				f"Coordinate converter: world-space center pivot"
			)
			layer3DResult.DrawTextCanvas(CFLPoint[Double](0, 25), strResultInfo, EColor.YELLOW, EColor.BLACK, 16)

			# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춰준다.
			# With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen.
			view3DResult.ZoomFit()

			# 이미지 뷰를 갱신 합니다. # Update image view
			view3DResult.Invalidate(True)

		if bPushFailed:
			break

		bSynchronizeFailed = False
		for i in range(1, i32EvaluationCaseCount):
			if (res := arrView3DResults[0].SynchronizePointOfView(arrView3DResults[i])[0]).IsFail():
				ErrorPrint(res, "Failed to synchronize 3D view points.")
				bSynchronizeFailed = True
				break

			if (res := arrView3DResults[0].SynchronizeWindow(arrView3DResults[i])[0]).IsFail():
				ErrorPrint(res, "Failed to synchronize 3D view windows.")
				bSynchronizeFailed = True
				break

		if bSynchronizeFailed:
			break

		# 3D 뷰 중 하나가 종료될 때까지 기다림 # Wait until any of the three 3D views is closed
		while arrView3DResults[0].IsAvailable() and \
			  arrView3DResults[1].IsAvailable() and \
			  arrView3DResults[2].IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
	main()
