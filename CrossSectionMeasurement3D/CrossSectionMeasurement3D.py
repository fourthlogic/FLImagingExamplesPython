# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


def AddSegment(listVertices, listSegmentIndices, listSegmentElementCount, listSegmentColors, tp3Start, tp3End, tp3Color):
	i32VertexIndex = listVertices.Count
	listVertices.Add(tp3Start)
	listVertices.Add(tp3End)
	listSegmentIndices.Add(i32VertexIndex)
	listSegmentIndices.Add(i32VertexIndex + 1)
	listSegmentElementCount.Add(2)
	listSegmentColors.Add(tp3Color)


def ColorToPoint3(color):
	i32Color = Convert.ToInt32(color)
	return TPoint3[Byte](i32Color & 0xff, (i32Color >> 8) & 0xff, (i32Color >> 16) & 0xff)


# 메인 함수 # Main function
def main():
	floSourceObject = CFL3DObject()
	floResultObject = CFL3DObject()
	view3D = CGUIView3D()
	res = CResult()

	while True:
		# 3D Object 로드 # Load the 3D object
		if (res := floSourceObject.Load("../../ExampleImages/SurfaceMatch3D/Car example.ply")).IsFail():
			ErrorPrint(res, "Failed to load the object file.\n")
			break

		# 3D 뷰 생성 # Create the 3D view
		if (res := view3D.Create(0, 0, 1024, 768)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		if (res := view3D.PushObject(floSourceObject)).IsFail():
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break

		# CrossSectionMeasurement3D 객체 생성 # Create CrossSectionMeasurement3D object
		crossSectionMeasurement3D = CCrossSectionMeasurement3D()
		crossSectionMeasurement3D.SetSourceObject(floSourceObject)
		tp3CrossSectionCenter = TPoint3[Single](-122.0, -48.0, -342.0)
		tp3CrossSectionNormal = TPoint3[Single](0.0, 1.0, 1.0)
		crossSectionMeasurement3D.SetCrossSection(tp3CrossSectionCenter, tp3CrossSectionNormal)
		crossSectionMeasurement3D.SetMeasurementPlane(CCrossSectionMeasurement3D.EMeasurementDirectionFromSection.Vertical)
		crossSectionMeasurement3D.SetSectionMeasurementMode(CCrossSectionMeasurement3D.ESectionMeasurementMode.GlobalSpan)
		crossSectionMeasurement3D.SetMeasurementInterval(3.0)
		crossSectionMeasurement3D.SetMinLength(0.1)
		crossSectionMeasurement3D.SetMaxLength(1e+09)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := crossSectionMeasurement3D.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute Cross Section Measurement 3D.")
			break

		listIntersectionLines = List[List[TPoint3[Single]]]()
		listMeasurementPoints = List[List[TPoint3[Single]]]()
		listMeasurementDistances = List[List[Single]]()

		crossSectionMeasurement3D.GetResultIntersectionLines(listIntersectionLines)
		crossSectionMeasurement3D.GetResultMeasurementPoints(listMeasurementPoints)
		crossSectionMeasurement3D.GetResultMeasurementDistances(listMeasurementDistances)

		listVertices = List[TPoint3[Single]]()
		listSegmentIndices = List[Int32]()
		listSegmentElementCount = List[Int32]()
		listSegmentColors = List[TPoint3[Byte]]()
		tp3IntersectionColor = ColorToPoint3(EColor.LIGHTGREEN)
		tp3MeasurementColor = ColorToPoint3(EColor.CYAN)

		for i in range(listIntersectionLines.Count):
			listLine = listIntersectionLines[i]

			for j in range(0, listLine.Count - 1):
				AddSegment(listVertices, listSegmentIndices, listSegmentElementCount, listSegmentColors, listLine[j], listLine[j + 1], tp3IntersectionColor)

		i32MeasurementCount = 0
		for i in range(listMeasurementPoints.Count):
			listPoints = listMeasurementPoints[i]

			for j in range(0, listPoints.Count - 1, 2):
				AddSegment(listVertices, listSegmentIndices, listSegmentElementCount, listSegmentColors, listPoints[j], listPoints[j + 1], tp3MeasurementColor)
				i32MeasurementCount += 1

		floResultObject.SetVertices(listVertices)
		floResultObject.SetSegmentIndices(listSegmentIndices)
		floResultObject.SetSegmentElementCountInformation(listSegmentElementCount)
		floResultObject.SetSegmentColors(listSegmentColors)

		viewResultObject = CGUIView3DObject(floResultObject)
		viewResultObject.SetTopologyType(ETopologyType3D.Segment)

		if (res := view3D.PushObject(viewResultObject)).IsFail():
			ErrorPrint(res, "Failed to display the result object.\n")
			break

		view3D.GetView3DObject(0).SetOpacity(0.5)

		layer3D = view3D.GetLayer(0)
		layer3D.Clear()
		layer3D.DrawTextCanvas(CFLPoint[Double](0, 0), "Cross Section Measurement 3D", EColor.YELLOW, EColor.BLACK, 20)
		layer3D.DrawTextCanvas(CFLPoint[Double](0, 30), f"Intersection Lines : {listIntersectionLines.Count}\nMeasurement Planes : {listMeasurementPoints.Count}\nMeasurements : {i32MeasurementCount}", EColor.YELLOW, EColor.BLACK, 15)
		for i in range(min(listMeasurementPoints.Count, listMeasurementDistances.Count)):
			listPoints = listMeasurementPoints[i]
			listDistances = listMeasurementDistances[i]

			d = 0
			for j in range(0, listPoints.Count - 1, 2):
				if d >= listDistances.Count:
					break

				tp3Text = TPoint3[Double]((listPoints[j].x + listPoints[j + 1].x) * .5, (listPoints[j].y + listPoints[j + 1].y) * .5, (listPoints[j].z + listPoints[j + 1].z) * .5)
				layer3D.DrawText3D(tp3Text, f"{listDistances[d]:.3f}", EColor.DEEPPINK, EColor.BLACK, 10)
				d += 1

		view3D.ZoomFit()
		view3D.Invalidate(True)

		while view3D.IsAvailable():
			CThreadUtilities.Sleep(1)

		break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
	main()
