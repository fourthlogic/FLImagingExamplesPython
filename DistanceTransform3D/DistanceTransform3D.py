# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import math

# 메인 함수 # Main function
def main():

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	view3DSrc = CGUIView3D()
	view3DDst = CGUIView3D()

	while True:
		# Source 3D 뷰 생성 # Create the Source 3D view
		if (res := view3DSrc.Create(100, 0, 600, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# Destination 3D 뷰 생성 # Create the destination 3D view
		if (res := view3DDst.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# 우선 빈 CGUIView3DObject 객체를 뷰에 추가한 후 해당 객체의 인덱스를 i32ReturnIndex 에 얻어 오기
		# First, add an empty CGUIView3DObject object to the view, then retrieve the index of that object into i32ReturnIndex.
		res, i32ReturnIndex = view3DSrc.PushObject(CGUIView3DObject(), -1)
		
		if res.IsFail():
			ErrorPrint(res, "Failed to display 3D object.\n")
			break

		# 뷰에 추가된 CGUIView3DObject 객체를 i32ReturnIndex 를 이용해서 얻어 오기
		# Retrieve the CGUIView3DObject object added to the view using i32ReturnIndex.
		objView3DSrc = view3DSrc.GetView3DObject(i32ReturnIndex)
		floDst = objView3DSrc.Get3DObject()

		# 뷰에 추가된 CGUIView3DObject 객체의 내부 CfloDst 에 ply 파일 로드
		# Load the PLY file into the internal CfloDst of the CGUIView3DObject object added to the view.
		floDst.Load("../../ExampleImages/DistanceTransform3D/binary-vertex.ply")

		# CfloDst 에 ply 파일을 로드하였으므로 뷰의 CGUIView3DObject 객체를 업데이트
		# Since the PLY file has been loaded into the CfloDst, update the CGUIView3DObject object in the view.
		view3DSrc.UpdateObject(i32ReturnIndex)
		view3DSrc.ZoomFit()

		# Distance Transform 3D 객체 생성 # Create Distance Transform 3D object
		distanceTransform3D = CDistanceTransform3D()

		tpPosition = TPoint3[Single](0.000000, 0.000000, 0.000000)
		tpDirection = TPoint3[Single](-0.100000, 0.000000, -1.000000)
		tpUpVector = TPoint3[Single](0.000000, 1.000000, 0.000000)

		# Source 객체 설정 # Set the source object
		distanceTransform3D.SetSourceObject(floDst)
		# 카메라 위치 설정 # Set the camera position
		distanceTransform3D.SetPosition(tpPosition)
		# 카메라 방향 설정 # Set the camera direction
		distanceTransform3D.SetDirection(tpDirection)
		# 카메라 업 벡터 설정 # Set the camera up vector
		distanceTransform3D.SetUpVector(tpUpVector)

		# 앞서 설정된 파라미터대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := distanceTransform3D.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute.\n")
			break

		arrResult = List[TPoint3[Single]]()
		# 거리 결과 가져오기 # Get the distance
		res, arrResult = distanceTransform3D.GetResultDistanceAxis(arrResult)

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer3DSrc = view3DSrc.GetLayer(0)
		layer3DDst = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer3DSrc.Clear()
		layer3DDst.Clear()

		# 거리 결과를 그려준다 # Draw distance result
		DrawResult(view3DDst, floDst.GetVertices(), arrResult, "Delta Z")

		# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춰준다. # With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen.
		if (res := view3DDst.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break

		flp = CFLPoint[Double](0, 0)

		if (res := layer3DSrc.DrawTextCanvas(flp, ("Source Object"), EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layer3DDst.DrawTextCanvas(flp, ("Destination Object"), EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		# 이미지 뷰를 갱신 합니다. # Update image view
		view3DSrc.Invalidate(True)
		view3DDst.Invalidate(True)

		# 이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while view3DSrc.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break

def DrawResult(pView3D: CGUIView3D, pFlaPlyData: List[TPoint3[Single]] , arrResult: List[TPoint3[Single]] , strDirection: String):
	arr2F32DataRange = [[math.inf, -math.inf ],[ math.inf, -math.inf],[math.inf, -math.inf]]

	for i in range(arrResult.Count):
		tp = arrResult[i]
		arr2F32DataRange[0][0] = min(arr2F32DataRange[0][0], tp.x)
		arr2F32DataRange[0][1] = max(arr2F32DataRange[0][1], tp.x)
		arr2F32DataRange[1][0] = min(arr2F32DataRange[1][0], tp.y)
		arr2F32DataRange[1][1] = max(arr2F32DataRange[1][1], tp.y)
		arr2F32DataRange[2][0] = min(arr2F32DataRange[2][0], tp.z)
		arr2F32DataRange[2][1] = max(arr2F32DataRange[2][1], tp.z)

	strRangeX = f"X : [{arr2F32DataRange[0][0]}, {arr2F32DataRange[0][1]}]"
	strRangeY = f"Y : [{arr2F32DataRange[1][0]}, {arr2F32DataRange[1][1]}]"
	strRangeZ = f"Z : [{arr2F32DataRange[2][0]}, {arr2F32DataRange[2][1]}]"

	pView3D.GetLayer(0).DrawTextCanvas(CFLPoint[Double](10, 20), "Data Ranges", EColor(8454143, True), EColor.BLACK, 13)
	pView3D.GetLayer(0).DrawTextCanvas(CFLPoint[Double](10, 35), strRangeX, EColor(8454143, True), EColor.BLACK, 13)
	pView3D.GetLayer(0).DrawTextCanvas(CFLPoint[Double](10, 50), strRangeY, EColor(8454016, True), EColor.BLACK, 13)
	pView3D.GetLayer(0).DrawTextCanvas(CFLPoint[Double](10, 65), strRangeZ, EColor(16744576, True), EColor.BLACK, 13)

	i32SelectedAxis = -1

	if strDirection == "Delta X":
		i32SelectedAxis = 0
	elif strDirection == "Delta Y":
		i32SelectedAxis = 1
	else: # dZ
		i32SelectedAxis = 2

	flaColors = List[TPoint3[Byte]]()

	for i in range(arrResult.Count):
		f32Intensity = (arrResult[i].z - arr2F32DataRange[i32SelectedAxis][0]) / (arr2F32DataRange[i32SelectedAxis][1] - arr2F32DataRange[i32SelectedAxis][0])

		if f32Intensity < 0:
			f32Intensity = 0
		if f32Intensity > 1:
			f32Intensity = 1

		f32Segment = 1.0 / 6.0

		arrF32Color = [0, 0, 0]

		for j in range(3):
			f32Value = (f32Intensity - (j * 2 - 1) * f32Segment) / f32Segment
			f32Value = max(0, min(1, f32Value))
			f32Temp = (f32Intensity - (j * 2 + 1) * f32Segment) / f32Segment
			f32Temp  = max(0, min(1, f32Temp ))
			f32Value -= f32Temp
			arrF32Color[j] = int(f32Value * 255)

		tpColor = TPoint3[Byte](arrF32Color[0], arrF32Color[1], arrF32Color[2])

		flaColors.Add(tpColor)

	res, i32ReturnIndex = pView3D.PushObject(CGUIView3DObject(), -1)

	if res.IsOK():
		objView3D = pView3D.GetView3DObject(i32ReturnIndex)
		fl3DO = objView3D.Get3DObject()
		fl3DO.Assign(pFlaPlyData, flaColors)
		pView3D.UpdateObject(i32ReturnIndex)

	
# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

if __name__ == '__main__':
    main()