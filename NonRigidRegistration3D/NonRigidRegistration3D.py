# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# FLImaging(R) 라이브러리의 기능을 사용하기 전에 아래 함수를 반드시 한 번 호출해야 합니다.
# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	# 3D 객체 선언 # Declare 3D object
	floDestinationObject = CFL3DObject()
	floLearnObject = CFL3DObject()
	floSourceObject = CFL3DObject()

	# 3D 뷰 선언 # Declare 3D view
	view3DDst = CGUIView3D()
	view3DLearn = CGUIView3D()
	view3DSource = CGUIView3D()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:
		# Learn Object 로드 # Load the Learn object
		if(res := floLearnObject.Load("../../ExampleImages/NonRigidRegistration3D/hand0Sample.fl3do")).IsFail() :
			ErrorPrint(res, "Failed to load the object file.\n")
			break

		# Source Object 로드 # Load the Source object
		if(res := floSourceObject.Load("../../ExampleImages/NonRigidRegistration3D/hand1Sample.fl3do")).IsFail() :
			ErrorPrint(res, "Failed to load the object file.\n")
			break

		# Learn 3D 뷰 생성 # Create the Learn 3D view
		if(res := view3DLearn.Create(0, 0, 500, 500)).IsFail() :
			ErrorPrint(res, "Failed to create the Learn 3D view.\n")
			break

		# Source 3D 뷰 생성 # Create the Source 3D view
		if(res := view3DSource.Create(500, 0, 1000, 512)).IsFail() :
			ErrorPrint(res, "Failed to create the Source 3D view.\n")
			break

		# Destination 3D 뷰 생성 # Create the Destination 3D view
		if(res := view3DDst.Create(0, 500, 500, 1000)).IsFail() :
			ErrorPrint(res, "Failed to create the Destination 3D view.\n")
			break

		# Learn 3D 뷰에 Learn Object 디스플레이 # Display the Learn object in the Learn 3D view
		if(res := view3DLearn.PushObject(floLearnObject)).IsFail() :
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break

		# Source 3D 뷰에 Source Object 디스플레이 # Display the Source object in the Source 3D view
		if(res := view3DSource.PushObject(floSourceObject)).IsFail() :
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break

		# CNonRigidRegistration3D 객체 생성 # Create CNonRigidRegistration3D object
		nonRigidRegistration3D = CNonRigidRegistration3D()

		# Learn object 설정 # Set the learn object
		nonRigidRegistration3D.SetLearnObject(floLearnObject)

		# Source object 설정 # Set the source object
		nonRigidRegistration3D.SetSourceObject(floSourceObject)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if(res := nonRigidRegistration3D.Execute()).IsFail() :
			ErrorPrint(res, "Failed to execute Non-Rigid Registration 3D.\n")
			break

		# 3D 뷰의 시점을 객체에 맞춤 # Fit the 3D views to the objects
		view3DLearn.ZoomFit()
		view3DSource.ZoomFit()
		view3DDst.ZoomFit()

		# 화면에 출력하기 위해 3D 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 from the 3D view for display
		# 이 객체는 3D 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to a 3D view and does not need to be released separately
		layer3DDst = view3DDst.GetLayer(0)
		layer3DLearn = view3DLearn.GetLayer(0)
		layer3DSource = view3DSource.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer3DDst.Clear()
		layer3DLearn.Clear()
		layer3DSource.Clear()

		# View 정보를 디스플레이 한다. # Display view information
		# 아래 함수 DrawTextCanvas 는 Screen좌표를 기준으로 하는 String을 Drawing 한다. # The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Area Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()

		if(res := layer3DLearn.DrawTextCanvas(flp, "Learn Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if(res := layer3DSource.DrawTextCanvas(flp, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if(res := layer3DDst.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
			ErrorPrint(res, "Failed to draw text.\n")
			break

		# 정합 결과 3D 객체 얻기 # Get the registration result 3D object
		floResult = CFL3DObject()

		res, floResult = nonRigidRegistration3D.GetResult3DObject(floResult)

		# 결과 객체를 3D 뷰에 표시하기 위한 객체 생성 # Create an object to display the result object in the 3D view
		view3DObject = CGUIView3DObject(floResult)

		i32ResultObjectIndex = 0

		# Destination 3D 뷰에 결과 객체와 Source 객체 디스플레이 # Display the result object and the Source object in the Destination 3D view
		res, i32ResultObjectIndex = view3DDst.PushObject(view3DObject, i32ResultObjectIndex)

		if res.IsFail() or (res := view3DDst.PushObject(floSourceObject)).IsFail() :
			ErrorPrint(res, "Failed to set object on the 3d view.\n")
			break

		# Learn 객체와 결과 객체의 정점 얻기 # Get the vertices of the Learn object and the result object
		listVertices = floLearnObject.GetVertices()
		listResultVertices = floResult.GetVertices()

		# 기준 점으로 Learn 객체의 첫 번째 정점 선택 # Select the first vertex of the Learn object as the reference point
		tp3Point = listVertices[0]
		tp3ResultTranslationVector = TPoint3[Single]()
		tp3ResultEulerAngle = TPoint3[Single]()

		# 정합 전 원본 Learn 객체 기준으로 기준 점과 가장 가까운 결과 노드의 인덱스 얻기
		# Get the index of the result node nearest to the reference point, searched on the original Learn object before registration
		i32ResultNodeIndex = nonRigidRegistration3D.GetNearestResultNodeIndex(tp3Point)

		# 결과 객체에서 동일한 인덱스의 정점이 기준 점의 정합 결과 위치 # The vertex with the same index in the result object is the registered position of the reference point
		tp3ResultPoint = listResultVertices[i32ResultNodeIndex]

		# 해당 노드의 결과 이동 벡터와 오일러 각 얻기 # Get the result translation vector and euler angle of the node
		res, tp3ResultTranslationVector = nonRigidRegistration3D.GetResultTranslationVector(i32ResultNodeIndex, tp3ResultTranslationVector)
		res, tp3ResultEulerAngle = nonRigidRegistration3D.GetResultEulerAngle(i32ResultNodeIndex, EEulerSequence.Extrinsic_XYZ, tp3ResultEulerAngle)

		# Learn 3D 뷰에 기준 점 위치 표시 # Display the reference point position in the Learn 3D view
		strLearnPosition = "Source Point"
		tp3LearnPosition = TPoint3[Double](float(tp3Point.x), float(tp3Point.y), float(tp3Point.z))

		layer3DLearn.DrawText3D(tp3LearnPosition, strLearnPosition, EColor.YELLOW, EColor.BLACK, 15)

		# Destination 3D 뷰의 결과 위치에 해당 노드의 결과 포즈 표시 # Display the result pose of the node at the result position in the Destination 3D view
		tp3ResultPosition = TPoint3[Double](float(tp3ResultPoint.x), float(tp3ResultPoint.y), float(tp3ResultPoint.z))

		strResultPose = "Source -> Target\nT({:.3f}, {:.3f}, {:.3f})\nR({:.3f}, {:.3f}, {:.3f})".format(
			tp3ResultTranslationVector.x, tp3ResultTranslationVector.y, tp3ResultTranslationVector.z,
			tp3ResultEulerAngle.x, tp3ResultEulerAngle.y, tp3ResultEulerAngle.z)

		layer3DDst.DrawText3D(tp3ResultPosition, strResultPose, EColor.YELLOW, EColor.BLACK, 15)

		# 결과 객체를 빨간색으로 강조 표시 # Highlight the result object in red
		view3DDst.GetView3DObject(i32ResultObjectIndex).HighlightObject(int(EColor.RED))

		# 3D 뷰의 시점을 객체에 맞춤 # Fit the 3D views to the objects
		view3DLearn.ZoomFit()
		view3DSource.ZoomFit()
		view3DDst.ZoomFit()

		# 3D 뷰들의 시점을 동기화 # Synchronize the point of view of the 3D views
		view3DDst.SynchronizePointOfView(view3DLearn)
		view3DDst.SynchronizePointOfView(view3DSource)

		# 3D 뷰를 갱신 합니다. # Update 3d view
		view3DSource.Invalidate(True)
		view3DLearn.Invalidate(True)
		view3DDst.Invalidate(True)
		view3DDst.UpdateObject(i32ResultObjectIndex)

		# 3D 뷰가 종료될 때 까지 기다림 # Wait for the 3D views to close
		while view3DLearn.IsAvailable() and view3DSource.IsAvailable() and view3DDst.IsAvailable() :
			CThreadUtilities.Sleep(1)
			
		view3DSource.Destroy()
		view3DLearn.Destroy()
		view3DDst.Destroy()

		break

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
	main()