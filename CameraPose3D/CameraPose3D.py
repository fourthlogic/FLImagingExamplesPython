# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

from System.Collections.Generic import List


# 메인 함수 // Main function
def main():

	dictEulerString = {
		EEulerSequence.Extrinsic_XYZ : 'Ext_XYZ',
		EEulerSequence.Extrinsic_XZY : 'Ext_XZY',
		EEulerSequence.Extrinsic_YZX : 'Ext_YZX',
		EEulerSequence.Extrinsic_YXZ : 'Ext_YXZ',
		EEulerSequence.Extrinsic_ZXY : 'Ext_ZXY',
		EEulerSequence.Extrinsic_ZYX : 'Ext_ZYX',
		EEulerSequence.Extrinsic_XYX : 'Ext_XYX',
		EEulerSequence.Extrinsic_XZX : 'Ext_XZX',
		EEulerSequence.Extrinsic_YZY : 'Ext_YZY',
		EEulerSequence.Extrinsic_YXY : 'Ext_YXY',
		EEulerSequence.Extrinsic_ZYZ : 'Ext_ZYZ',
		EEulerSequence.Extrinsic_ZXZ : 'Ext_ZXZ',
		EEulerSequence.Intrinsic_XYZ : 'Int_XYZ',
		EEulerSequence.Intrinsic_XZY : 'Int_XZY',
		EEulerSequence.Intrinsic_YZX : 'Int_YZX',
		EEulerSequence.Intrinsic_YXZ : 'Int_YXZ',
		EEulerSequence.Intrinsic_ZXY : 'Int_ZXY',
		EEulerSequence.Intrinsic_ZYX : 'Int_ZYX',
		EEulerSequence.Intrinsic_XYX : 'Int_XYX',
		EEulerSequence.Intrinsic_XZX : 'Int_XZX',
		EEulerSequence.Intrinsic_YZY : 'Int_YZY',
		EEulerSequence.Intrinsic_YXY : 'Int_YXY',
		EEulerSequence.Intrinsic_ZYZ : 'Int_ZYZ',
		EEulerSequence.Intrinsic_ZXZ : 'Int_ZXZ'
				}
	
	# 이미지 뷰 선언 // Declare the image view	
	view3D = CGUIView3D()

	# 이미지 선언 // Declare the image
	fliSource = CFLImage()

	while True:
		
		# 이미지 로드 // Load the image
		if(res := fliSource.Load("../../ExampleImages/CameraPose3D/ChessBoard(9).flif")).IsFail() :				
			ErrorPrint(res, "Failed to load the object file.\n")
			break
		
		# CameraPose3D 객체 생성 // Create CameraPose3D object
		cameraPose3D = CCameraPose3D()

		# Camera Matrix 설정 // Set the camera matrix
		flpFocalLength = CFLPoint[Double](617.8218, 618.2815)
		flpPrincipalPoint = CFLPoint[Double](319.05237, 243.0472)
		cameraPose3D.SetCameraMatrix(flpFocalLength, flpPrincipalPoint)

		# 셀 간격 설정 // Set the board cell pitch
		cameraPose3D.SetBoardCellPitch(5, 5)

		# 캘리브레이션 객체 타입 설정 // Set the calibration object type
		cameraPose3D.SetCalibrationObjectType(ECalibrationObjectType.ChessBoard)

		# 이미지 전처리 타입 설정 // Set the image preprocessing method
		cameraPose3D.SetPreprocessingMethod(ECalibrationPreprocessingMethod.ShadingCorrection)

		i32PageCount = fliSource.GetPageCount()

		flpOrigin = CFLPoint[Double](0, 0)

		arrViewWrap = list() 
		i32WindowWidth = 300
		i32WindowHeight = 300

		for i in range(0, i32PageCount // 3) :		
			i32Height = i32WindowHeight * i

			for j in range(0, i32PageCount // 3) :			
				i32Width = i32WindowWidth * j
				i32Index = i * 3 + j

				arrViewWrap.append(CGUIViewImage())
				arrViewWrap[i32Index].Create(10 + i32Height, i32Width, 10 + i32Height + i32WindowHeight, i32Width + i32WindowWidth)					

		for i in range(1, i32PageCount) :
			arrViewWrap[0].SynchronizeWindow(arrViewWrap[i])

		pagePtr = list()

		# 페이지 선택
		for i in range(0, i32PageCount) : 							
			pagePtr.append(CFLImage(fliSource.GetPage(i)))

			# 처리할 이미지 설정
			cameraPose3D.SetSourceImage(pagePtr[i])

			# 이미지 포인터 설정 // Set image pointer
			arrViewWrap[i].SetImagePtr(pagePtr[i])

			# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
			if(res := cameraPose3D.Execute()).IsFail() :			
				ErrorPrint(res, "Failed to execute Camera Pose 3D.")
				break			

			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately		
			layerViewSource = arrViewWrap[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
			layerViewSource.Clear()

			# View 정보를 디스플레이 한다. // Display view information
			# 아래 함수 DrawTextCanvas 는 Screen좌표를 기준으로 하는 String을 Drawing 한다. // The function DrawTextCanvas below draws a String based on the screen coordinates.
			# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다. // If the color parameter is added as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by processing it as a background color.
			# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
			#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
			# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
			#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
			if(res := layerViewSource.DrawTextCanvas(flpOrigin, "Source Image", EColor.YELLOW, EColor.BLACK, 15)).IsFail() :			
				ErrorPrint(res, "Failed to draw text.\n")
				break			

			# 결과 객체 영역 가져오기 // Get the result board region
			flqBoardRegion = CFLQuad[Double]()
			cameraPose3D.GetResultBoardRegion(flqBoardRegion)

			# 결과 코너점 가져오기 // Get the result corner points
			flfaCornerPoints = CFLFigureArray()
			cameraPose3D.GetResultCornerPoints(flfaCornerPoints)

			# 결과 객체 영역 그리기 // Draw the result board region
			layerViewSource.DrawFigureImage(flqBoardRegion, EColor.BLUE, 3)

			# 결과 코너점 그리기 // Draw the result corner points
			flfaCornerPoints.Flatten()

			for k in range(0, flfaCornerPoints.GetCount()) :
				layerViewSource.DrawFigureImage(flfaCornerPoints.GetAt(k).GetCenter().MakeCrossHair(5, True), EColor.ORANGE, 1)

			# 오일러 각 순서 설정 // Set the euler sequence
			eEulerSequence = EEulerSequence.Extrinsic_XYZ

			# 결과 가져오기 // Get the results
			listResultRotationVector = List[Double]()
			listResultTranslationVector = List[Double]()
			listResultEulerAngle = List[Double]()
			matResultRotationMatrix = CMatrix[Double]()

			res, listResultRotationVector = cameraPose3D.GetResultRotationVector(listResultRotationVector)
			res, matResultRotationMatrix = cameraPose3D.GetResultRotationMatrix(matResultRotationMatrix)
			res, listResultTranslationVector = cameraPose3D.GetResultTranslationVector(listResultTranslationVector)
			res, listResultEulerAngle = cameraPose3D.GetResultEulerAngle(eEulerSequence, listResultEulerAngle)

			flpImageSize = CFLPoint[Double](fliSource)
			flpImageSize.x *= 2
			flpImageSize.y *= 2

			strTranslate = String.Format("Translation Vector\n[{0,11:0.000000}]\n[{1,11:0.000000}]\n[{2,11:0.000000}]", listResultTranslationVector[0], listResultTranslationVector[1], listResultTranslationVector[2])
			strEuler = String.Format("Euler Angle({0})\n[{1,11:0.000000}]\n[{2,11:0.000000}]\n[{3,11:0.000000}]", dictEulerString[eEulerSequence], listResultEulerAngle[0], listResultEulerAngle[1], listResultEulerAngle[2])
			strRotationMatrix = String.Format("Rotation Matrix\n[{0,9:0.000000}, {1,9:0.000000}, {2,9:0.000000}]\n[{3,9:0.000000}, {4,9:0.000000}, {5,9:0.000000}]\n[{6,9:0.000000}, {7,9:0.000000}, {8,9:0.000000}]", matResultRotationMatrix.GetValue(0, 0), matResultRotationMatrix.GetValue(0, 1), matResultRotationMatrix.GetValue(0, 2), matResultRotationMatrix.GetValue(1, 0), matResultRotationMatrix.GetValue(1, 1), matResultRotationMatrix.GetValue(1, 2), matResultRotationMatrix.GetValue(2, 0), matResultRotationMatrix.GetValue(2, 1), matResultRotationMatrix.GetValue(2, 2))
			strRotationVector = String.Format("Rotation Vector\n[{0,11:0.000000}]\n[{1,11:0.000000}]\n[{2,11:0.000000}]", listResultRotationVector[0], listResultRotationVector[1], listResultRotationVector[2])
			
			layerViewSource.DrawTextImage(TPoint[Double](flpImageSize.x, 0), strTranslate, EColor.YELLOW, EColor.BLACK, 11, False, 0, EGUIViewImageTextAlignment.RIGHT_TOP, "Courier New")
			layerViewSource.DrawTextImage(TPoint[Double](0, flpImageSize.y), strEuler, EColor.YELLOW, EColor.BLACK, 11, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM, "Courier New")
			layerViewSource.DrawTextImage(TPoint[Double](0, 0), strRotationVector, EColor.YELLOW, EColor.BLACK, 11, False, 0, EGUIViewImageTextAlignment.LEFT_TOP, "Courier New")
			layerViewSource.DrawTextImage(TPoint[Double](flpImageSize.x, flpImageSize.y), strRotationMatrix, EColor.YELLOW, EColor.BLACK, 11, False, 0, EGUIViewImageTextAlignment.RIGHT_BOTTOM, "Courier New")		
			arrViewWrap[i].Invalidate()

		# 이미지 뷰가 종료될 때 까지 기다림
		while arrViewWrap[0].IsAvailable() :
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()