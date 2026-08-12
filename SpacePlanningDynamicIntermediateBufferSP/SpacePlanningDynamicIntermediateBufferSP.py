from FLImagingClrPy import *
import FLImagingCLR.ThreeDim.SpacePlanning as SP

import math
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *

i32BinDestination = 0
i32BinBuffer = 1
i32BinCount = 2

f32BinWorldSpacingX = 18.0
f32AnimationArcHeight = 4.0
f64AnimationDurationMs = 480.0
i32AnimationSleepMs = 1
f32SourcePreviewMaxTiltDegree = 20.0
u64SourceItemTypeRandomSeed = 0x9d84a3d390df0c46
u64SourceRotationRandomSeed = 0x6a09e667f3bcc909


class ESourceState:
	NeedNewSource = 0
	HasSource = 1


class SSourceSlot:
	def __init__(self):
		self.eState = ESourceState.NeedNewSource
		self.i32ItemType = -1
		self.i32ArrivalIndex = 0
		self.quatLocalRotation = None


class SRotationBasis:
	def __init__(self, tpAxisX=None, tpAxisY=None, tpAxisZ=None):
		self.tpAxisX = tpAxisX
		self.tpAxisY = tpAxisY
		self.tpAxisZ = tpAxisZ


class SBinFrame:
	def __init__(self):
		self.tpWorldPivot = None
		self.tpBinPivot = None
		self.basis = None


class SAnimationPose:
	def __init__(self):
		self.tpWorldCenter = None
		self.quatRotation = None


class SRuntimeModelSpecs:
	def __init__(self):
		self.arrBinSpecs = [None] * i32BinCount
		self.listItemSpecs = []


class SItemInstance:
	def __init__(self):
		self.i32ItemSpecIndex = 0
		self.eRotation = None
		self.tpMin = None
		self.tpMax = None


class SBinState:
	def __init__(self):
		self.listItems = []
		self.listCountAbove = []

	def AddInstance(self, instance):
		for i in range(len(self.listItems)):
			if IsBelow(self.listItems[i], instance):
				self.listCountAbove[i] += 1

		self.listItems.append(instance)
		self.listCountAbove.append(0)

	def GetFirstPickableIndexOfType(self, i32ItemSpecIndex):
		for i in range(len(self.listItems)):
			if self.listItems[i].i32ItemSpecIndex == i32ItemSpecIndex and self.listCountAbove[i] == 0:
				return CResult(EResult.OK), i

		return CResult(EResult.DoesNotExist), -1

	def RemovePickableAt(self, i32PlacedIndex):
		if i32PlacedIndex < 0 or i32PlacedIndex >= len(self.listItems) or self.listCountAbove[i32PlacedIndex] != 0:
			return CResult(EResult.DoesNotExist)

		removed = self.listItems[i32PlacedIndex]
		del self.listItems[i32PlacedIndex]
		del self.listCountAbove[i32PlacedIndex]

		for i in range(len(self.listItems)):
			if IsBelow(self.listItems[i], removed):
				self.listCountAbove[i] -= 1

		return CResult(EResult.OK)


def Clamp01(f64Value):
	if f64Value <= 0.0:
		return 0.0
	if f64Value >= 1.0:
		return 1.0

	return float(f64Value)


def Add(tpA, tpB):
	return TPoint3[Single](tpA.x + tpB.x, tpA.y + tpB.y, tpA.z + tpB.z)


def Sub(tpA, tpB):
	return TPoint3[Single](tpA.x - tpB.x, tpA.y - tpB.y, tpA.z - tpB.z)


def Scale(tpValue, f32Scale):
	return TPoint3[Single](tpValue.x * f32Scale, tpValue.y * f32Scale, tpValue.z * f32Scale)


def Dot(tpA, tpB):
	return tpA.x * tpB.x + tpA.y * tpB.y + tpA.z * tpB.z


def GetBinWorldOrigin(i32BinIndex):
	return TPoint3[Single](f32BinWorldSpacingX * i32BinIndex, 0.0, 0.0)


def Lerp(tpStart, tpEnd, f32T):
	return TPoint3[Single](
		tpStart.x + (tpEnd.x - tpStart.x) * f32T,
		tpStart.y + (tpEnd.y - tpStart.y) * f32T,
		tpStart.z + (tpEnd.z - tpStart.z) * f32T
	)


def MakeRotationBasis(tpAxisX, tpAxisY, tpAxisZ):
	return SRotationBasis(tpAxisX, tpAxisY, tpAxisZ)


def MakeQuaternionFromBasis(basis):
	matRotation = CMatrixFor3D[Single](
		basis.tpAxisX.x, basis.tpAxisY.x, basis.tpAxisZ.x,
		basis.tpAxisX.y, basis.tpAxisY.y, basis.tpAxisZ.y,
		basis.tpAxisX.z, basis.tpAxisY.z, basis.tpAxisZ.z
	)

	quat = CFLGeometry3DQuaternion[Single]()
	quat.SetMatrix(matRotation)
	quat.Normalize()
	return quat


def MakeRotationBasisFromQuaternion(quat):
	matRotation = CMatrixFor3D[Single]()
	_, matRotation = quat.GetMatrix(matRotation)

	return MakeRotationBasis(
		TPoint3[Single](matRotation[0, 0], matRotation[1, 0], matRotation[2, 0]),
		TPoint3[Single](matRotation[0, 1], matRotation[1, 1], matRotation[2, 1]),
		TPoint3[Single](matRotation[0, 2], matRotation[1, 2], matRotation[2, 2])
	)


def TransformBinDirection(binBasis, tpLocalDirection):
	return Add(
		Add(Scale(binBasis.tpAxisX, tpLocalDirection.x), Scale(binBasis.tpAxisY, tpLocalDirection.y)),
		Scale(binBasis.tpAxisZ, tpLocalDirection.z)
	)


def BinLocalDirectionFromWorld(binBasis, tpWorldDirection):
	return TPoint3[Single](
		Dot(tpWorldDirection, binBasis.tpAxisX),
		Dot(tpWorldDirection, binBasis.tpAxisY),
		Dot(tpWorldDirection, binBasis.tpAxisZ)
	)


def GetWorldCamera():
	cam = CFL3DCamera()
	cam.SetProjectionType(E3DCameraProjectionType.Perspective)
	cam.SetDirection(CFLPoint3[Single](0.0, -0.85, -0.53))
	cam.SetDirectionUp(CFLPoint3[Single](0.0, 0.53, -0.85))
	cam.SetPosition(CFLPoint3[Single](14.0, 55.0, 30.0))
	return cam


def MakeBinFrameRotation(i32BinIndex):
	quat = CFLGeometry3DQuaternion[Single]()
	if i32BinIndex == i32BinDestination:
		quat.SetEulerAngles(EEulerSequence.Extrinsic_XYZ, 6.0, 8.0, 5.0)
	else:
		quat.SetEulerAngles(EEulerSequence.Extrinsic_XYZ, -7.0, 5.0, -6.0)

	quat.Normalize()
	return quat


def GetBinFrame(i32BinIndex):
	frame = SBinFrame()
	frame.tpWorldPivot = GetBinWorldOrigin(i32BinIndex)
	frame.tpBinPivot = TPoint3[Single](0.0, 0.0, 0.0)
	frame.basis = MakeRotationBasisFromQuaternion(MakeBinFrameRotation(i32BinIndex))
	return frame


def WorldFromBinLocal(i32BinIndex, tpLocal):
	frame = GetBinFrame(i32BinIndex)
	tpDelta = Sub(tpLocal, frame.tpBinPivot)
	return Add(frame.tpWorldPivot, TransformBinDirection(frame.basis, tpDelta))


def BinLocalFromWorld(i32BinIndex, tpWorld):
	frame = GetBinFrame(i32BinIndex)
	tpDeltaWorld = Sub(tpWorld, frame.tpWorldPivot)
	return Add(frame.tpBinPivot, BinLocalDirectionFromWorld(frame.basis, tpDeltaWorld))


def MakeWorldRotationFromLocalRotation(i32BinIndex, quatLocalRotation):
	quatWorldRotation = MakeBinFrameRotation(i32BinIndex) * quatLocalRotation
	quatWorldRotation.Normalize()
	return quatWorldRotation


def MakeQuaternionFromRotationVector(tpRotationVector):
	f32Angle = math.sqrt(Dot(tpRotationVector, tpRotationVector))
	quat = CFLGeometry3DQuaternion[Single]()
	if f32Angle <= 1.0e-6:
		quat.SetEulerAngles(EEulerSequence.Extrinsic_XYZ, 0.0, 0.0, 0.0)
	else:
		f32InvAngle = 1.0 / f32Angle
		quat.SetAxisAndAngle(
			CFLGeometry3DVector[Single](tpRotationVector.x * f32InvAngle, tpRotationVector.y * f32InvAngle, tpRotationVector.z * f32InvAngle),
			f32Angle
		)
	quat.Normalize()
	return quat


def DrawSourcePreviewLocalRotation(rng):
	f32MaxTiltRadian = f32SourcePreviewMaxTiltDegree * math.pi / 180.0
	f32Tilt = math.sqrt(rng.GenerateUniformRandomValueF32(0.0, 1.0)) * f32MaxTiltRadian
	f32Azimuth = rng.GenerateUniformRandomValueF32(0.0, 2.0 * math.pi)
	tpRotationVector = TPoint3[Single](
		f32Tilt * math.cos(f32Azimuth),
		0.0,
		f32Tilt * math.sin(f32Azimuth)
	)
	return MakeQuaternionFromRotationVector(tpRotationVector)


def ApplyTransform(matRotation, tpOffset, tpLocal):
	return TPoint3[Single](
		tpOffset.x + matRotation[0, 0] * tpLocal.x + matRotation[0, 1] * tpLocal.y + matRotation[0, 2] * tpLocal.z,
		tpOffset.y + matRotation[1, 0] * tpLocal.x + matRotation[1, 1] * tpLocal.y + matRotation[1, 2] * tpLocal.z,
		tpOffset.z + matRotation[2, 0] * tpLocal.x + matRotation[2, 1] * tpLocal.y + matRotation[2, 2] * tpLocal.z
	)


def GetObjectExtents(itemSpec, quatRotation):
	matRotation = CMatrixFor3D[Single]()
	_, matRotation = quatRotation.GetMatrix(matRotation)

	f32HalfWidth = itemSpec.width * 0.5
	f32HalfHeight = itemSpec.height * 0.5
	f32HalfDepth = itemSpec.depth * 0.5

	return TPoint3[Single](
		f32HalfWidth * abs(matRotation[0, 0]) + f32HalfHeight * abs(matRotation[0, 1]) + f32HalfDepth * abs(matRotation[0, 2]),
		f32HalfWidth * abs(matRotation[1, 0]) + f32HalfHeight * abs(matRotation[1, 1]) + f32HalfDepth * abs(matRotation[1, 2]),
		f32HalfWidth * abs(matRotation[2, 0]) + f32HalfHeight * abs(matRotation[2, 1]) + f32HalfDepth * abs(matRotation[2, 2])
	)


def MakePoseFromBinLocalAabbMin(itemSpec, i32BinIndex, tpAabbMinBinLocal, quatLocalRotation):
	pose = SAnimationPose()
	pose.quatRotation = MakeWorldRotationFromLocalRotation(i32BinIndex, quatLocalRotation)
	pose.tpWorldCenter = WorldFromBinLocal(i32BinIndex, Add(tpAabbMinBinLocal, GetObjectExtents(itemSpec, quatLocalRotation)))
	return pose


def LerpArc(start, end, f32T, f32ArcHeight):
	pose = SAnimationPose()
	pose.tpWorldCenter = Lerp(start.tpWorldCenter, end.tpWorldCenter, f32T)
	pose.tpWorldCenter.y += f32ArcHeight * math.sin(math.pi * f32T)
	pose.quatRotation = CFLGeometry3DQuaternion[Single]()
	pose.quatRotation.SetSphericalLinearInterpolation(start.quatRotation, end.quatRotation, f32T)
	return pose


def FindClosestEquivalentCuboidRotation(quatStart, quatTarget):
	# A centered cuboid is invariant under a 180-degree rotation about any local principal axis.
	arrLocalSymmetries = [
		MakeQuaternionFromRotationVector(TPoint3[Single](0.0, 0.0, 0.0)),
		MakeQuaternionFromRotationVector(TPoint3[Single](math.pi, 0.0, 0.0)),
		MakeQuaternionFromRotationVector(TPoint3[Single](0.0, math.pi, 0.0)),
		MakeQuaternionFromRotationVector(TPoint3[Single](0.0, 0.0, math.pi)),
	]

	quatClosest = quatTarget
	f64ClosestDot = -1.0
	for quatLocalSymmetry in arrLocalSymmetries:
		quatCandidate = quatTarget * quatLocalSymmetry
		quatCandidate.Normalize()

		f64Dot = quatStart.Dot(quatCandidate)
		if f64Dot < 0.0:
			quatCandidate = CFLGeometry3DQuaternion[Single](-quatCandidate.x, -quatCandidate.y, -quatCandidate.z, -quatCandidate.w)
			f64Dot = -f64Dot

		if f64Dot > f64ClosestDot:
			quatClosest = quatCandidate
			f64ClosestDot = f64Dot

	return quatClosest


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


def GetSourcePreviewLocalPos(itemSpec, binSpecBuffer):
	tpSize = GetRotatedItemSize(itemSpec, SP.EAxisRotation.XYZ)
	return TPoint3[Single](binSpecBuffer.width + 2.0, 0.0, (binSpecBuffer.depth - tpSize.z) * 0.5)


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


def IsBelow(lower, upper):
	bXOverlap = (lower.tpMin.x < upper.tpMax.x) and (upper.tpMin.x < lower.tpMax.x)
	bZOverlap = (lower.tpMin.z < upper.tpMax.z) and (upper.tpMin.z < lower.tpMax.z)
	bUpperIsAbove = upper.tpMin.y >= lower.tpMax.y - 0.001

	return bXOverlap and bZOverlap and bUpperIsAbove


def WouldCoverBufferItem(binBuffer, item):
	for i in range(len(binBuffer.listItems)):
		if IsBelow(binBuffer.listItems[i], item):
			return True

	return False


def MakePlacementInfo(i32BinIndex, item):
	placement = SP.SPlacementInfo()
	placement.i32BinIndex = i32BinIndex
	placement.i32ItemIndex = item.i32ItemSpecIndex
	placement.eRotation = item.eRotation
	placement.tpPosition = item.tpMin
	return placement


def InitializeCoordinateConverter(alg, converter):
	res = CResult(EResult.UnknownError)

	while True:
		res, converter = alg.GetCoordinateConverter(converter)
		if res.IsFail():
			break

		bFailed = False
		for i in range(alg.GetBinSpecCount()):
			frame = GetBinFrame(i)
			if (res := converter.SetBinTransform(i, frame.tpWorldPivot, frame.tpBinPivot, frame.basis.tpAxisZ, frame.basis.tpAxisY)).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		for i in range(alg.GetItemSpecCount()):
			if (res := converter.SetItemPivotNormalized(i, TPoint3[Single](0.5, 0.5, 0.5))).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		res = converter.Learn()
		break

	return res, converter


def InitializeDefaultSourceItemChances(itemChances):
	itemChances.Clear()
	itemChances.Add(4.0)
	itemChances.Add(3.0)
	itemChances.Add(3.0)
	itemChances.Add(2.0)


def IsCacheUpToDate(strCache, strReference):
	if not os.path.exists(strCache):
		return False

	if not os.path.exists(strReference):
		return False

	return os.path.getmtime(strCache) > os.path.getmtime(strReference)


def DescribeStrategy(alg, sStrategyId):
	res, info = alg.GetStrategyInfo(sStrategyId, SP.SStrategyInfo())
	strName = info.strStrategyName if (res.IsOK() and info.strStrategyName is not None) else "?"
	return f'"{strName}" {{{sStrategyId.eGroup.ToString()}, {sStrategyId.i32IDInStrategy}}}'


def ConfigureAndLearnDefaultModel(alg, itemChances):
	res = CResult(EResult.UnknownError)

	while True:
		alg.Clear()

		arrDefaultBinSpecs = [
			SP.SBinSpec[Single](9.0, 12.0, 10.0),
			SP.SBinSpec[Single](6.0, 5.0, 6.0)
		]

		bFailed = False
		for binSpec in arrDefaultBinSpecs:
			if (res := alg.AddBinSpec(binSpec)).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		arrDefaultItemSpecs = [
			SP.SItemSpec[Single](3.0, 3.0, 4.0, 1.0, SP.ERotationAllowance.VerticalAxisOnly),
			SP.SItemSpec[Single](2.0, 4.3, 5.9, 1.0, SP.ERotationAllowance.VerticalAxisOnly),
			SP.SItemSpec[Single](4.0, 3.0, 3.5, 1.0, SP.ERotationAllowance.VerticalAxisOnly),
			SP.SItemSpec[Single](5.0, 3.0, 2.5, 1.0, SP.ERotationAllowance.FullRotation)
		]

		for itemSpec in arrDefaultItemSpecs:
			if (res := alg.AddItemSpec(itemSpec)).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		parameters = SP.SRandomSequenceParameters.CreateInfinite(itemChances, 2)
		if (res := alg.SetRandomSequenceParameters(parameters)).IsFail() or \
		   (res := alg.EnableImmediateScoreEvaluation(False)).IsFail():
			break

		if (res := alg.Learn()).IsFail() or \
		   (res := alg.SetExecutionMode(SP.EExecutionMode.EvaluateScore)).IsFail() or \
		   (res := alg.Execute()).IsFail():
			break

		if not alg.HasValidOptimalStrategy():
			res = CResult(EResult.NoResult)
		break

	return res


def LearnOrLoadDefaultModel(alg, itemChances, strCache, strSource):
	res = CResult(EResult.UnknownError)

	if IsCacheUpToDate(strCache, strSource):
		res = alg.Load(strCache)

		if res.IsOK() and alg.IsLearned() and alg.HasValidOptimalStrategy():
			res, parameters = alg.GetRandomSequenceParameters(SP.SRandomSequenceParameters.CreateInfinite(itemChances, 2))
			if res.IsFail():
				return res

			itemChances.Clear()
			for f32Chance in parameters.itemChances:
				itemChances.Add(f32Chance)

			sSelected = alg.GetSelectedStrategyId()
			print(f"Loaded cached model: {strCache} (strategy {DescribeStrategy(alg, sSelected)})")
			return res

	InitializeDefaultSourceItemChances(itemChances)

	if (res := ConfigureAndLearnDefaultModel(alg, itemChances)).IsFail():
		return res

	sOptimal = alg.GetOptimalStrategyId()
	if (res := alg.SelectStrategy(sOptimal)).IsFail():
		return res

	resSave = alg.Save(strCache)
	if resSave.IsFail():
		print(f"Warning: failed to cache model ({strCache}): {resSave.GetString()}")
	else:
		print(f"Learned and cached model: {strCache} (strategy {DescribeStrategy(alg, sOptimal)})")

	return res


def LoadRuntimeSpecsFromModel(alg, modelSpecs):
	res = CResult(EResult.UnknownError)

	if alg.GetBinSpecCount() < i32BinCount or alg.GetItemSpecCount() <= 0:
		return CResult(EResult.InvalidData)

	for i in range(i32BinCount):
		modelSpecs.arrBinSpecs[i] = alg.GetBinSpec(i)

	modelSpecs.listItemSpecs = []
	for i in range(alg.GetItemSpecCount()):
		modelSpecs.listItemSpecs.append(alg.GetItemSpec(i))

	return CResult(EResult.OK)


def IsSameItemSpec(lhs, rhs):
	return lhs.width == rhs.width and \
		lhs.height == rhs.height and \
		lhs.depth == rhs.depth and \
		lhs.load == rhs.load and \
		lhs.eAllowed == rhs.eAllowed


def ValidateSameItemSpecs(alg, listItemSpecs):
	if alg.GetItemSpecCount() != len(listItemSpecs):
		return CResult(EResult.Mismatched)

	for i in range(alg.GetItemSpecCount()):
		itemSpec = alg.GetItemSpec(i)

		if not IsSameItemSpec(itemSpec, listItemSpecs[i]):
			return CResult(EResult.Mismatched)

	return CResult(EResult.OK)


def PushBinToView(view3D, converter, flogBins, bin, i32BinIndex):
	res = CResult(EResult.UnknownError)

	while True:
		res, i32BinObjIndex = view3D.PushObject(flogBins.GetObjectByIndex(i32BinIndex), -1)
		binObj = view3D.GetView3DObject(i32BinObjIndex)
		if binObj is not None:
			binObj.SetOpacity(0.15)

		if len(bin.listItems) == 0:
			res = CResult(EResult.OK)
			break

		listPlacements = List[SP.SPlacementInfo]()
		for i in range(len(bin.listItems)):
			listPlacements.Add(MakePlacementInfo(i32BinIndex, bin.listItems[i]))

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


def CaptureObjectLocalVertices(view3D, i32ObjIndex, tpWorldCenter):
	viewObject = view3D.GetView3DObject(i32ObjIndex)
	if viewObject is None:
		return CResult(EResult.DoesNotExist), []

	object3D = viewObject.Get3DObject()
	if object3D is None:
		return CResult(EResult.DoesNotExist), []

	listLocalVertices = []
	listVertices = object3D.m_listVertex
	for i in range(listVertices.Count):
		listLocalVertices.append(Sub(listVertices[i], tpWorldCenter))

	return CResult(EResult.OK), listLocalVertices


def UpdateItemObjectPose(view3D, i32ObjIndex, listLocalVertices, pose):
	viewObject = view3D.GetView3DObject(i32ObjIndex)
	if viewObject is None:
		return CResult(EResult.DoesNotExist)

	object3D = viewObject.Get3DObject()
	if object3D is None or object3D.m_listVertex.Count != len(listLocalVertices):
		return CResult(EResult.DoesNotExist)

	matRotation = CMatrixFor3D[Single]()
	res, matRotation = pose.quatRotation.GetMatrix(matRotation)
	if res.IsFail():
		return res

	for i in range(len(listLocalVertices)):
		tpVertex = ApplyTransform(matRotation, pose.tpWorldCenter, listLocalVertices[i])
		if (res := object3D.SetVertexAt(i, tpVertex)).IsFail():
			return res

	viewObject.UpdateVertex(True)
	return CResult(EResult.OK)


def PushItemObjectAtPose(view3D, converter, itemSpec, i32ItemSpecIndex, i32RenderBinIndex, pose, f32Opacity, captureLocalVertices):
	res = CResult(EResult.UnknownError)
	i32ObjIndex = -1
	listLocalVertices = []

	while True:
		tpCenterBinLocal = BinLocalFromWorld(i32RenderBinIndex, pose.tpWorldCenter)
		tpUnrotatedMinBinLocal = TPoint3[Single](
			tpCenterBinLocal.x - itemSpec.width * 0.5,
			tpCenterBinLocal.y - itemSpec.height * 0.5,
			tpCenterBinLocal.z - itemSpec.depth * 0.5
		)

		placement = SP.SPlacementInfo()
		placement.i32BinIndex = i32RenderBinIndex
		placement.i32ItemIndex = i32ItemSpecIndex
		placement.eRotation = SP.EAxisRotation.XYZ
		placement.tpPosition = tpUnrotatedMinBinLocal

		listPlacement = List[SP.SPlacementInfo]()
		listPlacement.Add(placement)

		flogItem = CFL3DObjectGroup()
		res, flogItem = converter.MakeItemObjectGroup(listPlacement, flogItem)
		if res.IsFail():
			break

		res, i32ObjIndex = view3D.PushObject(flogItem.GetObjectByIndex(0), i32ObjIndex)
		viewObject = view3D.GetView3DObject(i32ObjIndex)
		if viewObject is not None:
			viewObject.SetOpacity(f32Opacity)

		res, listCapturedLocalVertices = CaptureObjectLocalVertices(view3D, i32ObjIndex, pose.tpWorldCenter)
		if res.IsFail():
			break

		renderBinBasis = GetBinFrame(i32RenderBinIndex).basis
		for i in range(len(listCapturedLocalVertices)):
			listCapturedLocalVertices[i] = BinLocalDirectionFromWorld(renderBinBasis, listCapturedLocalVertices[i])

		if (res := UpdateItemObjectPose(view3D, i32ObjIndex, listCapturedLocalVertices, pose)).IsFail():
			break

		view3D.UpdateObject(i32ObjIndex)

		if captureLocalVertices:
			listLocalVertices = listCapturedLocalVertices

		res = CResult(EResult.OK)
		break

	return res, i32ObjIndex, listLocalVertices


def PushSourcePreviewToView(view3D, converter, itemSpec, i32ItemSpecIndex, binSpecBuffer, quatLocalRotation):
	poseSource = MakePoseFromBinLocalAabbMin(itemSpec, i32BinBuffer, GetSourcePreviewLocalPos(itemSpec, binSpecBuffer), quatLocalRotation)
	res, _, _ = PushItemObjectAtPose(view3D, converter, itemSpec, i32ItemSpecIndex, i32BinBuffer, poseSource, 0.85, False)
	return res


def PushInFlightItemToView(view3D, converter, itemSpec, i32ItemSpecIndex, pose):
	return PushItemObjectAtPose(view3D, converter, itemSpec, i32ItemSpecIndex, i32BinDestination, pose, 0.95, True)


def RebuildInteractiveState(alg, arrBins, i32ExcludedBinIndex, i32ExcludedPlacedIndex):
	res = CResult(EResult.UnknownError)

	while True:
		if (res := alg.ClearInteractiveStates()).IsFail():
			break

		if (res := alg.SetExecutionMode(SP.EExecutionMode.Interactive)).IsFail() or \
		   (res := alg.Execute()).IsFail():
			break

		bFailed = False
		for i32BinIndex in range(i32BinCount):
			bin = arrBins[i32BinIndex]
			for i in range(len(bin.listItems)):
				if i32BinIndex == i32ExcludedBinIndex and i == i32ExcludedPlacedIndex:
					continue

				placement = MakePlacementInfo(i32BinIndex, bin.listItems[i])
				if (res := alg.PushItem(placement.i32ItemIndex, 1)).IsFail() or \
				   (res := alg.AddPlacement(placement)).IsFail():
					bFailed = True
					break

			if bFailed:
				break

		if bFailed:
			break

		res = CResult(EResult.OK)
		break

	return res


def FindRecommendedPlacementInBin(alg, i32BinIndex):
	listCandidates = List[SP.SPlacementInfo]()
	res, listCandidates = alg.GetRecommendedNextPlacements(256, listCandidates)
	if res.IsFail():
		return res, None

	for i in range(listCandidates.Count):
		if listCandidates[i].i32BinIndex == i32BinIndex:
			return CResult(EResult.OK), listCandidates[i]

	return CResult(EResult.DoesNotExist), None


def TryPlaceSourceInBuffer(alg, converter, arrBins, listItemSpecs, binSpecBuffer, sourceSlot, fnOnStep, fnAnimateMove):
	res = CResult(EResult.UnknownError)
	bPlaced = False
	i32SourceItemType = sourceSlot.i32ItemType
	i32ArrivalIndex = sourceSlot.i32ArrivalIndex

	while True:
		if (res := RebuildInteractiveState(alg, arrBins, -1, -1)).IsFail():
			break

		if (res := alg.PushItem(i32SourceItemType, 1)).IsFail():
			break

		res, placement = FindRecommendedPlacementInBin(alg, i32BinBuffer)
		if res.IsFail():
			if res == CResult(EResult.DoesNotExist) or res == CResult(EResult.FullOfCapacity):
				print(f"[source] arrival {i32ArrivalIndex:2d}: Buffer cannot accept item type {i32SourceItemType}.")
				res = CResult(EResult.OK)
			break

		item = MakeItemInstance(listItemSpecs, placement)
		if WouldCoverBufferItem(arrBins[i32BinBuffer], item):
			print(f"[source] arrival {i32ArrivalIndex:2d}: item type {i32SourceItemType} can be placed in Buffer, but would cover a buffered item.")
			res = CResult(EResult.OK)
			break

		poseStart = None
		poseEnd = None
		if fnAnimateMove is not None:
			itemSpec = listItemSpecs[placement.i32ItemIndex]
			poseStart = MakePoseFromBinLocalAabbMin(itemSpec, i32BinBuffer, GetSourcePreviewLocalPos(itemSpec, binSpecBuffer), sourceSlot.quatLocalRotation)
			poseEnd = SAnimationPose()
			res, poseEnd.tpWorldCenter, poseEnd.quatRotation = converter.ConvertPose(
				placement,
				TPoint3[Single](),
				CFLGeometry3DQuaternion[Single]()
			)
			if res.IsFail():
				break

		if (res := alg.AddPlacement(placement)).IsFail():
			break

		sourceSlot.eState = ESourceState.NeedNewSource
		if fnAnimateMove is not None:
			fnAnimateMove(placement.i32ItemIndex, poseStart, poseEnd)

		arrBins[i32BinBuffer].AddInstance(item)

		print(
			f"[source] arrival {i32ArrivalIndex:2d}: Source item type {placement.i32ItemIndex} rotation {int(placement.eRotation)} "
			f"-> Buffer [{placement.tpPosition.x:.1f}, {placement.tpPosition.y:.1f}, {placement.tpPosition.z:.1f}]  "
			f"(Destination:{len(arrBins[i32BinDestination].listItems)}, Buffer:{len(arrBins[i32BinBuffer].listItems)})"
		)

		if fnOnStep is not None:
			fnOnStep()

		bPlaced = True
		res = CResult(EResult.OK)
		break

	return res, bPlaced


def MoveOnePendingItemToDestination(alg, converter, arrBins, listItemSpecs, binSpecBuffer, sourceSlot, fnOnStep, fnAnimateMove):
	res = CResult(EResult.UnknownError)
	i32SourceItemType = sourceSlot.i32ItemType
	i32ArrivalIndex = sourceSlot.i32ArrivalIndex

	while True:
		if (res := RebuildInteractiveState(alg, arrBins, -1, -1)).IsFail():
			break

		bFailed = False
		for i in range(len(arrBins[i32BinBuffer].listItems)):
			if arrBins[i32BinBuffer].listCountAbove[i] != 0:
				continue

			if (res := alg.PushItem(arrBins[i32BinBuffer].listItems[i].i32ItemSpecIndex, 1)).IsFail():
				bFailed = True
				break

		if bFailed:
			break

		if (res := alg.PushItem(i32SourceItemType, 1)).IsFail():
			break

		res, placement = FindRecommendedPlacementInBin(alg, i32BinDestination)
		if res.IsFail():
			if res == CResult(EResult.DoesNotExist) or res == CResult(EResult.FullOfCapacity):
				res = CResult(EResult.FullOfCapacity)
			break

		resPick, i32BufferPickIndex = arrBins[i32BinBuffer].GetFirstPickableIndexOfType(placement.i32ItemIndex)
		bUseBufferedItem = resPick.IsOK()

		if not bUseBufferedItem and placement.i32ItemIndex != i32SourceItemType:
			res = CResult(EResult.DoesNotExist)
			break

		poseStart = None
		poseEnd = None
		if fnAnimateMove is not None:
			if bUseBufferedItem:
				placementStart = MakePlacementInfo(i32BinBuffer, arrBins[i32BinBuffer].listItems[i32BufferPickIndex])
				poseStart = SAnimationPose()
				res, poseStart.tpWorldCenter, poseStart.quatRotation = converter.ConvertPose(
					placementStart,
					TPoint3[Single](),
					CFLGeometry3DQuaternion[Single]()
				)
				if res.IsFail():
					break
			else:
				itemSpec = listItemSpecs[placement.i32ItemIndex]
				poseStart = MakePoseFromBinLocalAabbMin(itemSpec, i32BinBuffer, GetSourcePreviewLocalPos(itemSpec, binSpecBuffer), sourceSlot.quatLocalRotation)

			poseEnd = SAnimationPose()
			res, poseEnd.tpWorldCenter, poseEnd.quatRotation = converter.ConvertPose(
				placement,
				TPoint3[Single](),
				CFLGeometry3DQuaternion[Single]()
			)
			if res.IsFail():
				break

		if (res := alg.AddPlacement(placement)).IsFail():
			break

		if bUseBufferedItem:
			if (res := arrBins[i32BinBuffer].RemovePickableAt(i32BufferPickIndex)).IsFail():
				break
		else:
			sourceSlot.eState = ESourceState.NeedNewSource

		if fnAnimateMove is not None:
			fnAnimateMove(placement.i32ItemIndex, poseStart, poseEnd)

		arrBins[i32BinDestination].AddInstance(MakeItemInstance(listItemSpecs, placement))

		if (res := RebuildInteractiveState(alg, arrBins, -1, -1)).IsFail():
			break

		strSource = "Buffered" if bUseBufferedItem else "Source"
		print(
			f"[destination] arrival {i32ArrivalIndex:2d}: {strSource} item type {placement.i32ItemIndex} rotation {int(placement.eRotation)} "
			f"-> Destination [{placement.tpPosition.x:.1f}, {placement.tpPosition.y:.1f}, {placement.tpPosition.z:.1f}]  "
			f"(Destination:{len(arrBins[i32BinDestination].listItems)}, Buffer:{len(arrBins[i32BinBuffer].listItems)})"
		)

		if fnOnStep is not None:
			fnOnStep()

		res = CResult(EResult.OK)
		break

	return res


def ProcessSourceArrival(alg, converter, arrBins, listItemSpecs, binSpecBuffer, sourceSlot, fnOnStep, fnAnimateMove):
	i32MaxAttemptCount = len(arrBins[i32BinBuffer].listItems) + 2
	for _ in range(i32MaxAttemptCount):
		res, bPlacedInBuffer = TryPlaceSourceInBuffer(alg, converter, arrBins, listItemSpecs, binSpecBuffer, sourceSlot, fnOnStep, fnAnimateMove)
		if res.IsFail():
			return res

		if bPlacedInBuffer:
			return CResult(EResult.OK)

		if (res := MoveOnePendingItemToDestination(alg, converter, arrBins, listItemSpecs, binSpecBuffer, sourceSlot, fnOnStep, fnAnimateMove)).IsFail():
			return res

		if sourceSlot.eState == ESourceState.NeedNewSource:
			return CResult(EResult.OK)

	return CResult(EResult.FullOfCapacity)


def DrawSourceItemType(rng, itemChances, i32ItemSpecCount):
	if i32ItemSpecCount <= 0:
		return -1

	if itemChances.Count == i32ItemSpecCount:
		f32TotalChance = 0.0
		for i in range(itemChances.Count):
			f32TotalChance += itemChances[i] if itemChances[i] > 0.0 else 0.0

		if f32TotalChance > 0.0:
			f32Pick = rng.GenerateUniformRandomValueF32(0.0, f32TotalChance)
			f32Accumulated = 0.0
			for i in range(itemChances.Count):
				f32Accumulated += itemChances[i] if itemChances[i] > 0.0 else 0.0
				if f32Pick <= f32Accumulated:
					return i

			return itemChances.Count - 1

	return rng.GenerateUniformRandomValueI32(0, i32ItemSpecCount - 1)


def main():
	CLibraryUtilities.Initialize()

	view3DResult = CGUIView3D()
	res = CResult(EResult.UnknownError)

	while True:
		alg = CSpacePlanningDynamicSP()

		strSource = os.path.abspath(__file__)
		strCache = f"SpacePlanningDynamicIntermediateBuffer.{alg.GetFileExtension()}"

		itemChances = List[Single]()
		if (res := LearnOrLoadDefaultModel(alg, itemChances, strCache, strSource)).IsFail():
			ErrorPrint(res, "Failed to prepare the default model.")
			break

		modelSpecs = SRuntimeModelSpecs()
		if (res := LoadRuntimeSpecsFromModel(alg, modelSpecs)).IsFail():
			ErrorPrint(res, "Failed to load runtime specs from the model.")
			break

		if (res := ValidateSameItemSpecs(alg, modelSpecs.listItemSpecs)).IsFail():
			ErrorPrint(res, "Loaded item specs do not match the runtime specs.")
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

		if (res := view3DResult.Create(600, 0, 1300, 650)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.")
			break

		view3DResult.SetRenderingTransparencyMode(ERenderingTransparencyMode.DepthPeelingOIT)
		view3DResult.SetRenderingResolutionScale(2)
		view3DResult.GetLayer(0).DrawTextCanvas(CFLPoint[Double](0, 0), "Dynamic SP - Source / Buffer / Destination", EColor.YELLOW, EColor.BLACK, 20)

		arrBins = [SBinState(), SBinState()]
		bZoomFitted = False
		sourceSlot = SSourceSlot()

		def fnDraw():
			nonlocal bZoomFitted

			if not view3DResult.IsAvailable():
				return

			view3DResult.Lock()
			view3DResult.ClearObjects()

			PushBinToView(view3DResult, converter, flogBins, arrBins[i32BinDestination], i32BinDestination)
			PushBinToView(view3DResult, converter, flogBins, arrBins[i32BinBuffer], i32BinBuffer)

			if sourceSlot.eState == ESourceState.HasSource:
				PushSourcePreviewToView(view3DResult, converter, modelSpecs.listItemSpecs[sourceSlot.i32ItemType], sourceSlot.i32ItemType, modelSpecs.arrBinSpecs[i32BinBuffer], sourceSlot.quatLocalRotation)

			layer3DStatus = view3DResult.GetLayer(1)
			layer3DStatus.Clear()

			resVolume, f32TotalDestination, f32UsedDestination = alg.GetCurrentVolumeUsage(i32BinDestination, 0.0, 0.0)
			resVolume, f32TotalBuffer, f32UsedBuffer = alg.GetCurrentVolumeUsage(i32BinBuffer, 0.0, 0.0)

			if sourceSlot.eState == ESourceState.HasSource:
				strStatus = (
					f"Destination: {len(arrBins[i32BinDestination].listItems)} items, {f32UsedDestination:.1f} / {f32TotalDestination:.1f}  |  "
					f"Buffer: {len(arrBins[i32BinBuffer].listItems)} items, {f32UsedBuffer:.1f} / {f32TotalBuffer:.1f}  |  "
					f"Source {sourceSlot.i32ArrivalIndex}: item type {sourceSlot.i32ItemType}"
				)
			else:
				strStatus = (
					f"Destination: {len(arrBins[i32BinDestination].listItems)} items, {f32UsedDestination:.1f} / {f32TotalDestination:.1f}  |  "
					f"Buffer: {len(arrBins[i32BinBuffer].listItems)} items, {f32UsedBuffer:.1f} / {f32TotalBuffer:.1f}"
				)

			layer3DStatus.DrawTextCanvas(CFLPoint[Double](0, 25), strStatus, EColor.YELLOW, EColor.BLACK, 16)

			if not bZoomFitted and (sourceSlot.eState == ESourceState.HasSource or len(arrBins[i32BinDestination].listItems) > 0 or len(arrBins[i32BinBuffer].listItems) > 0):
				view3DResult.SetCamera(GetWorldCamera())
				bZoomFitted = True

			view3DResult.Unlock()
			view3DResult.Invalidate(True)

		def fnRender():
			fnDraw()
			if view3DResult.IsAvailable():
				CThreadUtilities.Sleep(500)

		def fnAnimateMove(i32ItemType, poseStart, poseEnd):
			if not view3DResult.IsAvailable():
				return

			poseEndMinimumMotion = SAnimationPose()
			poseEndMinimumMotion.tpWorldCenter = poseEnd.tpWorldCenter
			poseEndMinimumMotion.quatRotation = FindClosestEquivalentCuboidRotation(poseStart.quatRotation, poseEnd.quatRotation)

			fnDraw()

			view3DResult.Lock()
			resPush, i32InFlightObjIndex, listLocalVertices = PushInFlightItemToView(
				view3DResult,
				converter,
				modelSpecs.listItemSpecs[i32ItemType],
				i32ItemType,
				poseStart
			)
			view3DResult.Unlock()
			if resPush.IsFail():
				return

			view3DResult.Invalidate(True)

			f64Start = time.perf_counter()
			while view3DResult.IsAvailable():
				f32T = Clamp01(((time.perf_counter() - f64Start) * 1000.0) / f64AnimationDurationMs)
				poseNext = LerpArc(poseStart, poseEndMinimumMotion, f32T, f32AnimationArcHeight)

				view3DResult.LockUpdate()
				resUpdate = UpdateItemObjectPose(view3DResult, i32InFlightObjIndex, listLocalVertices, poseNext)
				view3DResult.UnlockUpdate()

				if resUpdate.IsFail():
					break

				view3DResult.UpdateObject(i32InFlightObjIndex)

				if f32T >= 1.0:
					break

				CThreadUtilities.Sleep(i32AnimationSleepMs)

		if (res := RebuildInteractiveState(alg, arrBins, -1, -1)).IsFail():
			ErrorPrint(res, "Failed to initialize the interactive state.")
			break

		fnRender()

		rngSourceItemType = CXorshiroRandomGenerator()
		rngSourceItemType.Seed(u64SourceItemTypeRandomSeed)
		rngSourceRotation = CXorshiroRandomGenerator()
		rngSourceRotation.Seed(u64SourceRotationRandomSeed)
		i32NextArrivalIndex = 1

		while view3DResult.IsAvailable():
			if sourceSlot.eState == ESourceState.NeedNewSource:
				sourceSlot.eState = ESourceState.HasSource
				sourceSlot.i32ItemType = DrawSourceItemType(rngSourceItemType, itemChances, len(modelSpecs.listItemSpecs))
				sourceSlot.i32ArrivalIndex = i32NextArrivalIndex
				sourceSlot.quatLocalRotation = DrawSourcePreviewLocalRotation(rngSourceRotation)
				i32NextArrivalIndex += 1

				fnRender()
				print(f"[source] arrival {sourceSlot.i32ArrivalIndex:2d}: item type {sourceSlot.i32ItemType}")

			if (res := ProcessSourceArrival(alg, converter, arrBins, modelSpecs.listItemSpecs, modelSpecs.arrBinSpecs[i32BinBuffer], sourceSlot, fnRender, fnAnimateMove)).IsFail():
				if res == CResult(EResult.FullOfCapacity):
					print(f"Arrival {sourceSlot.i32ArrivalIndex}: Destination and Buffer cannot accept the source item. Stopping.")
				elif view3DResult.IsAvailable():
					ErrorPrint(res, "Failed to process the source item.")
				break

		print(f"Dynamic intermediate buffer packing complete. Destination:{len(arrBins[i32BinDestination].listItems)}, Buffer:{len(arrBins[i32BinBuffer].listItems)}")

		while view3DResult.IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
	main()
