# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


import time

def main():
    
	# 3D 뷰 선언
	# Declare 3D views.
    view3D = Array[CGUIView3D]([CGUIView3D(), CGUIView3D()])

    while True:
		# 3D 뷰 생성
		# Create 3D views.
        if (res := view3D[0].Create(100, 0, 612, 512)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.")
            break

        if (res := view3D[1].Create(612, 0, 1124, 512)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.")
            break

        view3D[0].SynchronizeWindow(view3D[1])

        view3D[0].SetTopologyType(ETopologyType3D.Wireframe)
        view3D[1].SetTopologyType(ETopologyType3D.Wireframe)

		# 곡선의 접선에서 코드(Chord, 곡선의 두 점을 직선으로 연결한 선분)가 벗어날 수 있는 최대 거리를 나타냅니다. 
		# 이 값이 클수록 분할된 삼각형의 수가 적어지며, 
		# 반대로 값이 작을수록 더 많은 삼각형이 형성되어 곡선을 더 정밀하게 근사합니다. 
		# 기본값 0을 입력하면 step 모델에서 적절한 chordal deviation 값을 자동으로 계산합니다.
		# It represents the maximum distance that a chord (a straight line segment connecting two points on the curve) can deviate from the tangent of the curve. 
		# A larger value results in fewer triangles being formed, 
		# while a smaller value results in more triangles, providing a more precise approximation of the curve. 
		# The default value of 0 automatically calculates the appropriate chordal deviation value based on the imported step model.
        f64ChordalDeviation = 0.0
        
		# 방법 1. CFL3DObject 에서 STEP 파일 로드
		# Method 1. Load the STEP file directly into a CFL3DObject
        # 3D 뷰에 빈 CGUIView3DObject 객체 추가
        # Add an empty CGUIView3DObject to the 3D view
        res, i32ReturnIndex = view3D[0].PushObject(CGUIView3DObject(), -1)
        if res.IsFail():
            ErrorPrint(res, "Failed to display 3D object.")
            break
        
        # 3D 뷰에 추가한 CGUIView3DObject 객체 얻어 오기
        # Get the CGUIView3DObject that was added to the 3D view
        objView3D = view3D[0].GetView3DObject(i32ReturnIndex)
        if objView3D is None:
            res = CResult(EResult.NullPointer)
            ErrorPrint(res, "Failed to get View3D object.")
            break

        # CGUIView3DObject 내부의 CFL3DObject 객체(fl3DObject) 얻어 오기
        # Get the CFL3DObject instance from inside the CGUIView3DObject
        fl3DObject = objView3D.Get3DObject()
        if fl3DObject is None:
            res = CResult(EResult.NullPointer)
            ErrorPrint(res, "Failed to get 3D object.")
            break

        # CGUIView3DObject 객체(fl3DObject)에 STEP 파일 로드. 이 때 STEP 파일 경로와 f64ChordalDeviation 값을 전달        
        # Load the STEP file into the CFL3DObject (provide path and chordal deviation)
        if (res := fl3DObject.LoadSTEP("../../ExampleImages/StepReaderConvertTo3DObject/Cylinder.step", f64ChordalDeviation)).IsFail():
            ErrorPrint(res, "Failed to load step file.")
            break

        # CFL3DObject에 STEP 파일이 로드되었으므로 뷰어에서 이를 업데이트
        # Update the 3D viewer after loading the STEP file into CFL3DObject
        view3D[0].UpdateObject(i32ReturnIndex)
        view3D[0].ZoomFit()
        
		# 방법 2. CStepReader 에서 STEP 파일 로드 후 GetResult3DObject() 로 CFL3DObject 에 할당
        # Method 2. Load the STEP file using CStepReader, then assign it to a CFL3DObject using GetResult3DObject()
        # STEP 파일을 읽는 객체 CStepReader 선언
        # Declare a CStepReader object for reading STEP files
        stepReader = CStepReader()

        # Chordal Deviation을 0.00001로 설정
        # Set chordal deviation value
        f64ChordalDeviation = 0.00001

        # 3D 뷰에 빈 CGUIView3DObject 객체 추가
        # Add an empty CGUIView3DObject to the 3D view
        res, i32ReturnIndex = view3D[1].PushObject(CGUIView3DObject(), -1)

        if res.IsFail():
            ErrorPrint(res, "Failed to display 3D object.")
            break
        
        # 3D 뷰에 추가한 CGUIView3DObject 객체 얻어 오기
        # Get the CGUIView3DObject that was added to the 3D view
        objView3D2 = view3D[1].GetView3DObject(i32ReturnIndex)
        if objView3D2 is None:
            ErrorPrint(res, "Failed to get View3D object.")
            break

        # CGUIView3DObject 내부의 CFL3DObject 객체(fl3DObject) 얻어 오기
        # Get the CFL3DObject instance from inside the CGUIView3DObject
        fl3DObject2 = objView3D2.Get3DObject()
        if fl3DObject2 is None:
            res = CResult(EResult.NullPointer)
            ErrorPrint(res, "Failed to get 3D object.")
            break

        # CStepReader 객체(stepReader)에 STEP 파일을 로드
        # Load the STEP file into the CStepReader
        if (res := stepReader.Load("../../ExampleImages/StepReaderConvertTo3DObject/Cylinder.step")).IsFail():
            ErrorPrint(res, "Failed to load step file.")
            break

        # CStepReader 객체(stepReader)에 로드된 STEP 파일을 CFL3DObject 객체(fl3DObject)로 얻어 오기. 이 때 f64ChordalDeviation를 전달
        # Retrieve the CFL3DObject from the loaded CStepReader result, passing in the chordal deviation
        if (res := stepReader.GetResult3DObject(fl3DObject2, f64ChordalDeviation)[0]).IsFail():
            ErrorPrint(res, "Failed to get 3D object from the StepReader.")
            break
        
        # CFL3DObject 객체가 업데이트 되었으므로 뷰어에서 이를 업데이트
        # Update the 3D viewer after the CFL3DObject has been populated
        view3D[1].UpdateObject(i32ReturnIndex)
        view3D[1].ZoomFit()

        # 형태를 확인 및 비교하기 좋은 위치로 카메라 설정
        # Set the camera to a good angle for visual comparison of the two shapes
        camera = CGUIView3DCamera()
        camera.SetDirection(CFLPoint3[Single](-0.2, 0.8, -0.6))
        camera.SetDirectionUp(CFLPoint3[Single](-0.2, 1.0, 0.1))
        camera.SetPosition(CFLPoint3[Single](56.2, -276.5, 324.0))
        camera.SetTarget(CFLPoint3[Single](9.6, -34.5, 151.4))

        view3D[0].SetCamera(camera)
        view3D[1].SetCamera(camera)

        flp = CFLPoint[Double](0, 0)
        
		# 아래 함수 DrawTextCanvas는 스크린 좌표를 기준으로 문자열을 뷰어에 출력한다.
        # The function DrawTextCanvas displays a string on the viewer using screen coordinates.
		# 파라미터 순서 : 기준 좌표 Figure 객체 -> 문자열 -> 텍스트 색 -> 텍스트 테두리 색 -> 폰트 크기 -> 실제 크기로 출력 유무 -> 각도 -> 정렬 -> 폰트 이름 -> 텍스트 알파값(불투명도) -> 텍스트 테두리 알파값 (불투명도) -> 폰트 두께 -> 폰트 이탤릭 여부
		# Parameter order: reference coordinate (Figure object) -> text string -> text color -> text outline color -> font size -> render in real-world size (bool) -> angle -> alignment -> font name -> text alpha (opacity) -> text outline alpha (opacity) -> font thickness -> italic font (bool)
        if (res := view3D[0].GetLayer(2).DrawTextCanvas(flp, "Chordal Deviation = 0.0", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        if (res := view3D[1].GetLayer(2).DrawTextCanvas(flp, "Chordal Deviation = 0.00001", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text")
            break

        # 3D 객체 형태를 보기 좋게 3D 뷰 캔바스 색상을 흰색으로 지정
        # Set the 3D view canvas background color to white for better object visibility
        view3D[0].SetCanvasColor(EColor.WHITE)
        view3D[1].SetCanvasColor(EColor.WHITE)

        # 3D 뷰 화면 갱신
        # Refresh the 3D view screens
        view3D[0].UpdateScreen()
        view3D[1].UpdateScreen()

        # 3D 뷰가 닫히기 전까지 종료하지 않고 대기
        # Wait until the 3D views are closed before exiting
        while view3D[0].IsAvailable() and view3D[1].IsAvailable():
            CThreadUtilities.Sleep(1)

        break
	# End of main function


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()