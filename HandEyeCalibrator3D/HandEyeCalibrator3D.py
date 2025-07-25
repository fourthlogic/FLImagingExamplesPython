# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()
from System.Collections.Generic import List

# 메인 함수 // Main function
def main():
	CLibraryUtilities.Initialize()

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
	
	# 이미지 객체 선언 // Declare the image object
	fliSource = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImage = CGUIViewImage()
	view3D = CGUIView3D()

	while True:
		
		# 이미지 로드 // Load the image
		if(res := fliSource.Load('../../ExampleImages/HandEyeCalibrator3D/ChessBoard.flif')).IsFail() :
			ErrorPrint(res, 'Failed to load the object file.\n')
			break

		# HandEyeCalibrator3D 객체 생성 // Create HandEyeCalibrator3D object
		HandEyeCalibrator3D = CHandEyeCalibrator3D()

		# 엔드 이펙터 포즈 로드 // Load the end effector pose
		if(res := HandEyeCalibrator3D.LoadEndEffectorPose('../../ExampleImages/HandEyeCalibrator3D/EndEffectorPose.csv')).IsFail() :				
			ErrorPrint(res, 'Failed to load the file.\n')
			break			

		# 처리할 이미지 설정
		HandEyeCalibrator3D.SetSourceImage(fliSource)

		# Camera Matrix 설정 // Set the camera matrix
		flpFocalLength = CFLPoint[Double](428.668823242188, 428.268188476563)
		flpPrincipalPoint = CFLPoint[Double](422.934997558594, 240.188659667969)
		 
		HandEyeCalibrator3D.SetCalibrationCameraMatrix(flpFocalLength, flpPrincipalPoint)

		# 셀 간격 설정 // Set the board cell pitch
		HandEyeCalibrator3D.SetCalibrationBoardCellPitch(15, 15)

		# 캘리브레이션 객체 타입 설정 // Set the calibration object type
		HandEyeCalibrator3D.SetCalibrationObjectType(ECalibrationObjectType.ChessBoard)

		# 최적화 방법 설정 // Set the optimization method
		HandEyeCalibrator3D.SetOptimizationMethod(EOptimizationMethod.Nonlinear)

		# 회전 타입 설정 // Set the rotation type
		HandEyeCalibrator3D.SetRotationType(ERotationType.RotationVector)

		# 엔드 이펙터 각 단위 설정 // Set the end effector angle unit
		HandEyeCalibrator3D.SetEndEffectorAngleUnit(EAngleUnit.Radian)

		# 오일러 각 순서 설정 // Set the euler sequence
		HandEyeCalibrator3D.SetEulerSequence(EEulerSequence.Extrinsic_XYZ)

		#왜곡 계수 설정 // Set the distortion coefficient
		listDistortionCoefficient = List[Double]()
		
		listDistortionCoefficient.Add(-0.0538526475429535)
		listDistortionCoefficient.Add(0.0590364411473274)
		listDistortionCoefficient.Add(0.000375126546714455)
		listDistortionCoefficient.Add(0.000785713375080377)
		listDistortionCoefficient.Add(-0.0189481563866138)

		HandEyeCalibrator3D.SetCalibrationDistortionCoefficient(listDistortionCoefficient)

		i32PageCount = fliSource.GetPageCount()

		# 이미지 뷰 생성 // Create image view
		if(res := viewImage.Create(100, 0, 612, 512)).IsFail() :
		
			ErrorPrint(res, 'Failed to create the Source image view.\n')
			break
		

		# 결과 3D 뷰 생성 // Create result 3D view
		if(res := view3D.Create(612, 0, 1124, 512)).IsFail() :			
			ErrorPrint(res, 'Failed to create the Result 3D view.\n')
			break
			

		# 이미지 포인터 설정 // Set image pointer
		viewImage.SetImagePtr(fliSource)

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately		
		layerViewSource = viewImage.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerViewSource.Clear()

		# View 정보를 디스플레이 한다. // Display view information
		# 아래 함수 DrawTextCanvas 는 Screen좌표를 기준으로 하는 String을 Drawing 한다. // The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다. // If the color parameter is added as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by processing it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		if(res := layerViewSource.DrawTextCanvas(CFLPoint[Double](0, 0), 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail() :		
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := HandEyeCalibrator3D.Calibrate()).IsFail() :		
			ErrorPrint(res, 'Failed to execute Hand Eye Calibrator 3D.')
			break
		

		if view3D.IsAvailable() :		
			view3DLayer = view3D.GetLayer(0)
			matResultRotationVector = CMatrix[Double]()
			tp3ResultTranslationVector = TPoint3[Double]()
			listResultEulerAngle = List[Double]()			
			# 캘리브레이션 결과 얻어오기 // Get the calibration result
			HandEyeCalibrator3D.GetResultHandToEyeRotationVector(matResultRotationVector)
			HandEyeCalibrator3D.GetResultHandToEyeTranslationVector(tp3ResultTranslationVector)
			HandEyeCalibrator3D.GetResultHandToEyeEulerAngle(listResultEulerAngle)
			f64RotationError = 0.0
			f64TranslationError = 0.0
			res, f64RotationError = HandEyeCalibrator3D.GetResultRotationError(f64RotationError)
			res, f64TranslationError = HandEyeCalibrator3D.GetResultTranslationError(f64TranslationError)

			# 3D View의 canvas rect 영역 얻어오기 // Get the canvas rect region
			flrCanvasRegion = view3D.GetClientRectCanvasRegion()

			flpImageSize = CFLPoint[Double](flrCanvasRegion.GetWidth(), flrCanvasRegion.GetHeight())
			strTranslate = f'Translation Vector\n{tp3ResultTranslationVector.x:0.6f}\n{tp3ResultTranslationVector.y:0.6f}\n{tp3ResultTranslationVector.z:0.6f}'
			strEuler = f'Euler Angle\n{listResultEulerAngle[0]:0.6f}\n{listResultEulerAngle[1]:0.6f}\n{listResultEulerAngle[2]:0.6f}'
			strRotationVector = f'Rotation Vector\n{matResultRotationVector.GetValue(0, 0):0.6f}\n{matResultRotationVector.GetValue(1, 0):0.6f}\n{matResultRotationVector.GetValue(2, 0):0.6f}'
			strError = f'Rotation Error\n{f64RotationError:0.6f}\nTranslation Error\n{f64TranslationError:0.6f}'

			view3DLayer.DrawTextCanvas(CFLPoint[Double](0, 0), strRotationVector, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.LEFT_TOP)
			view3DLayer.DrawTextCanvas(CFLPoint[Double](0, flpImageSize.y), strEuler, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)
			view3DLayer.DrawTextCanvas(CFLPoint[Double](flpImageSize.x, flpImageSize.y), strTranslate, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.RIGHT_BOTTOM)
			view3DLayer.DrawTextCanvas(CFLPoint[Double](flpImageSize.x, 0), strError, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.RIGHT_TOP)

			fl3DOCalibrationBoard = CFL3DObject() 
			tp3BoardCenter = TPoint3[Double]()

			HandEyeCalibrator3D.GetResultCalibration3DObject(fl3DOCalibrationBoard, tp3BoardCenter)		
			strIdx = f'Calibration Board'

			view3DLayer.DrawText3D(tp3BoardCenter, strIdx, EColor.RED, EColor.BLACK, 9.0)
			view3D.PushObject(fl3DOCalibrationBoard)

			for i in range(0, i32PageCount, 1):
				tp3RobotCenter = TPoint3[Double]()
				tp3CamCenter = TPoint3[Double]()
				fl3DORobot = CFL3DObject()
				fl3DCam = CFL3DObject()
				tp3Cam = TPoint3[Single]()
				tp3Board = TPoint3[Single]()

		 		# 결과 3D 객체 얻어오기 // Get the result 3D object
				res, fl3DCam, tp3CamCenter = HandEyeCalibrator3D.GetResultCamera3DObject(i, fl3DCam, tp3CamCenter)

				if res.IsOK() :
					# 카메라 포즈 추정에 실패할 경우 NOK 출력 // NOK output if camera pose estimation fails
					res, tp3Cam, tp3Board = HandEyeCalibrator3D.GetResultReprojectionPoint(i, tp3Cam, tp3Board)

					if res.IsFail() :
						strIdx = f'Cam {i} (NOK)'
						view3DLayer.DrawText3D(tp3CamCenter, strIdx, EColor.CYAN, EColor.BLACK, 9.0)
					else:
						strIdx = f'Cam {i}'
						view3DLayer.DrawText3D(tp3CamCenter, strIdx, EColor.YELLOW, EColor.BLACK, 9.0)
						view3D.PushObject(fl3DCam)		 			
						
					view3D.PushObject(CGUIView3DObjectLine(tp3Cam, tp3Board, EColor.CYAN))
					
					res, flo3DORobot, tp3RobotCenter = HandEyeCalibrator3D.GetEndEffector3DObject(i, fl3DORobot, tp3RobotCenter)

					if res.IsOK():		 		
						strIdx = f'End Effector {i}'
						view3DLayer.DrawText3D(tp3RobotCenter, strIdx, EColor.BLUE, EColor.BLACK, 9.0)
						view3D.PushObject(fl3DORobot)		 				 	

			view3D.Invalidate()
			view3D.ZoomFit()		 

		 # 이미지 뷰가 종료될 때 까지 기다림
		while viewImage.IsAvailable() and view3D.IsAvailable():
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