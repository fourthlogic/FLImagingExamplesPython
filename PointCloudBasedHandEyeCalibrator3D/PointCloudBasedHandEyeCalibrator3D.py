# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *
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
	
	# 3D 객체 선언 // Declare the 3d object
	floLearn = CFL3DObject()

	# 이미지 뷰 선언 // Declare the image view	
	view3D = CGUIView3D()

	while True:
		
		match = CSurfaceMatch3D()

		# 오일러 각 순서 설정 // Set the euler sequence
		match.SetEulerSequence(EEulerSequence.Extrinsic_XYZ)

		# Learn Object 로드 // Load learn object

		if(res :=floLearn.Load("../../ExampleImages/PointCloudBasedHandEyeCalibrator3D/Learn.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the object.\n")
			break
		

		match.SetLearnObject(floLearn)

		# 피벗 설정 // Set the pivot point.
		flpPivot = CFLPoint3[Double](-7.880958, -43.990047, 546.119202)
		match.SetLearnPivot(flpPivot)

		if(res :=match.Learn()).IsFail() :	
			ErrorPrint(res, "Failed to learn.\n")
			break		

		# PointCloudBasedHandEyeCalibrator3D 객체 생성 // Create PointCloudBasedHandEyeCalibrator3D object
		PointCloudBasedHandEyeCalibrator3D = CPointCloudBasedHandEyeCalibrator3D()

		# 엔드 이펙터 포즈 로드 // Load the end effector pose
		if(res :=PointCloudBasedHandEyeCalibrator3D.LoadEndEffectorPose("../../ExampleImages/PointCloudBasedHandEyeCalibrator3D/EndEffectorPose.csv")).IsFail() :		
			ErrorPrint(res, "Failed to load the file.\n")
			break		

		PointCloudBasedHandEyeCalibrator3D.Set3DMatchModel(match)

		# Source object 로드 // load the source object			
		i32SourceCount = 9

		for i in range(0, i32SourceCount) :		
			floSource = CFL3DObject()
			flsFileName = f's{i + 1}.ply'

			if(res :=floSource.Load("../../ExampleImages/PointCloudBasedHandEyeCalibrator3D/" + flsFileName)).IsFail() :		
				ErrorPrint(res, "Failed to load the object.\n")
				break
		
			PointCloudBasedHandEyeCalibrator3D.AddSourceObject(floSource)		

		# 캘리브레이션 모드 설정 // Set the calibration mode
		PointCloudBasedHandEyeCalibrator3D.SetCalibrationMode(CHandEyeCalibrator3D.ECalibrationMode.EyeInHand)

		# 최적화 방법 설정 // Set the optimization method
		PointCloudBasedHandEyeCalibrator3D.SetOptimizationMethod(EOptimizationMethod.Nonlinear)

		# 회전 타입 설정 // Set the rotation type
		PointCloudBasedHandEyeCalibrator3D.SetRotationType(ERotationType.EulerAngle)

		# 엔드 이펙터 각 단위 설정 // Set the end effector angle unit
		PointCloudBasedHandEyeCalibrator3D.SetEndEffectorAngleUnit(EAngleUnit.Degree)

		# 오일러 각 순서 설정 // Set the euler sequence
		PointCloudBasedHandEyeCalibrator3D.SetEulerSequence(EEulerSequence.Extrinsic_XYZ)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res :=PointCloudBasedHandEyeCalibrator3D.Calibrate()).IsFail() :		
			ErrorPrint(res, "Failed to execute Point Cloud Based Hand Eye Calibrator 3D.")
			break		

		# 결과 3D 뷰 생성 // Create result 3D view
		if(res :=view3D.Create(612, 0, 1124, 512)).IsFail() :		
			ErrorPrint(res, "Failed to create the Result 3D view.\n")
			break		

		if view3D.IsAvailable() :		
			view3DLayer = view3D.GetLayer(0)

			matResultRotationVector = CMatrix[Double]()
			tp3ResultTranslationVector = TPoint3[Double]()
			listResultEulerAngle = List[Double]()
			f64RotationError = 0
			f64TranslationError = 0
			# 캘리브레이션 결과 얻어오기 // Get the calibration result
			PointCloudBasedHandEyeCalibrator3D.GetResultHandToEyeRotationVector(matResultRotationVector)
			PointCloudBasedHandEyeCalibrator3D.GetResultHandToEyeTranslationVector(tp3ResultTranslationVector)
			PointCloudBasedHandEyeCalibrator3D.GetResultHandToEyeEulerAngle(listResultEulerAngle)
			res, f64RotationError = PointCloudBasedHandEyeCalibrator3D.GetResultRotationError(f64RotationError)
			res, f64TranslationError = PointCloudBasedHandEyeCalibrator3D.GetResultTranslationError(f64TranslationError)

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

			PointCloudBasedHandEyeCalibrator3D.GetResultCalibration3DObject(fl3DOCalibrationBoard, tp3BoardCenter)			
			strIdx = 'Calibration Board'
			view3DLayer.DrawText3D(tp3BoardCenter, strIdx, EColor.RED, EColor.BLACK, 9.0)
			view3D.PushObject(fl3DOCalibrationBoard)

			for i in range(0, PointCloudBasedHandEyeCalibrator3D.GetSourceObjectCount()):			
				tp3RobotCenter = TPoint3[Double]()
				tp3CamCenter = TPoint3[Double]()
				fl3DORobot = CFL3DObject()
				fl3DCam = CFL3DObject()
				tp3Cam = TPoint3[Single]()
				tp3Board = TPoint3[Single]()

		 		# 결과 3D 객체 얻어오기 // Get the result 3D object
				res, fl3DCam, tp3CamCenter = PointCloudBasedHandEyeCalibrator3D.GetResultCamera3DObject(i, fl3DCam, tp3CamCenter)

				if res.IsOK() :
					# 카메라 포즈 추정에 실패할 경우 NOK 출력 // NOK output if camera pose estimation fails
					res, tp3Cam, tp3Board = PointCloudBasedHandEyeCalibrator3D.GetResultReprojectionPoint(i, tp3Cam, tp3Board)

					if res.IsFail() :
						strIdx = f'Cam {i} (NOK)'
						view3DLayer.DrawText3D(tp3CamCenter, strIdx, EColor.CYAN, EColor.BLACK, 9.0)
					else:
						strIdx = f'Cam {i}'
						view3DLayer.DrawText3D(tp3CamCenter, strIdx, EColor.YELLOW, EColor.BLACK, 9.0)
						view3D.PushObject(fl3DCam)		 			
						
					view3D.PushObject(CGUIView3DObjectLine(tp3Cam, tp3Board, EColor.CYAN))
					
					res, flo3DORobot, tp3RobotCenter = PointCloudBasedHandEyeCalibrator3D.GetEndEffector3DObject(i, fl3DORobot, tp3RobotCenter)

					if res.IsOK():		 		
						strIdx = f'End Effector {i}'
						view3DLayer.DrawText3D(tp3RobotCenter, strIdx, EColor.BLUE, EColor.BLACK, 9.0)
						view3D.PushObject(fl3DORobot)		 				

			view3D.Invalidate()
			view3D.ZoomFit()

			# 이미지 뷰가 종료될 때 까지 기다림
			while view3D.IsAvailable():
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