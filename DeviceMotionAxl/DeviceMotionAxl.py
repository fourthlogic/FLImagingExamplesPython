# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from enum import Enum

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

# 모션 기능 enum # motion feature enum
class EMotionFeature(Enum):
	SearchOriginPosition = 0
	MoveAbsolutePosition = 1
	MoveIncrementalPosition = 2


# 메인 함수 # Main function
def main():

	# Axl Motion 장치를 선언 # Declare Axl Motion device
	devMotion = CDeviceMotionAxl()

	while True:
		# 모션 파일의 전체 경로를 입력합니다. # Enter the full path of the motion file.
		strInput = input("Enter motion file full path (e.g. C:/Motion/Any.mot): ")

		strMotionPath = strInput
		strMotionPath = strMotionPath.replace("\r", "")
		strMotionPath = strMotionPath.replace("\n", "")

		# 모션 파일의 경로를 설정합니다. # Sets the path to the motion file.
		if((res := devMotion.SetMotionFilePath(strMotionPath)).IsFail()):
			ErrorPrint(res, "Failed to set motion file path.")
			break

		# 연결할 축 개수를 설정합니다. # Sets the number of axes to connect to.
		if((res := devMotion.SetAxisCount(1)).IsFail()):
			ErrorPrint(res, "Failed to set axis count.")
			break

		# 모션 장치를 초기화 합니다. # Initialize the motion device.
		if((res := devMotion.Initialize()).IsFail()):
			ErrorPrint(res, "Failed to initialize the device.")
			break

		# 모션 축 객체를 얻어옵니다. # Obtain motion axis objects.
		motionAxis : CDeviceMotionAxlAxis = devMotion.GetMotionAxis(0)

		if motionAxis == None:
			print("Failed to get motion axis.")
			break

		# 서보를 켭니다. # Turn on the servo.
		if((res := motionAxis.SetServoOn(True)).IsFail()):
			ErrorPrint(res, "Failed to servo on.")
			break

		while motionAxis.IsServoOn() == False:
			CThreadUtilities.Sleep(100)

		while True:
			eMotionFeature = EMotionFeature.MoveAbsolutePosition
			bExit = False

			while True:
				# 사용할 모션 기능을 선택합니다. # Select the motion feature you want to use.
				print("")
				print("1. Search Origin Position")
				print("2. Move Absolute Position")
				print("3. Move Incremental Position")
				print("0. Exit")
				strInput = input("Select: ")
				i32Select = int(strInput)

				if i32Select == 0:
					bExit = True
					break
				elif i32Select == 1:
					eMotionFeature = EMotionFeature.SearchOriginPosition
					break
				elif i32Select == 2:
					eMotionFeature = EMotionFeature.MoveAbsolutePosition
					break
				elif i32Select == 3:
					eMotionFeature = EMotionFeature.MoveIncrementalPosition
					break

				print("Incorrect input. Please select again.\n")

			if bExit == True:
				break

			if eMotionFeature == EMotionFeature.SearchOriginPosition:
				# 원점 복귀 동작을 진행합니다. # Proceed with the return-to-origin action.
				if((res := motionAxis.SearchOriginPosition()).IsFail()):
					ErrorPrint(res, "Failed to search origin position.")
					break

				# 원점 복귀 동작이 완료 될때까지 대기합니다. # Wait until the return to origin action is complete.
				CThreadUtilities.Sleep(100)

				while motionAxis.GetSearchOriginStatus() == CDeviceMotionAxlAxis.ESearchOriginStatus.Searching:
					CThreadUtilities.Sleep(100)

				if motionAxis.GetSearchOriginStatus() == CDeviceMotionAxlAxis.ESearchOriginStatus.Error:
					print("Failed to search origin position.")
				else:
					print("Successed to search origin position.")
			else:
				f64MoveVelocity = 0
				f64MoveAccelAndDecel = 0
				f64MovePosition = 0

				# 이동 속도를 입력합니다. # Enter the velocity of movement.
				strInput = input("Enter Axis Velocity(mm/s): ")
				f64MoveVelocity = float(strInput)

				# 가감속을 입력합니다. # Enter acceleration and deceleration.
				strInput = input("Enter Axis Acceleration(mm/s^2): ")
				f64MoveAccelAndDecel = float(strInput)

				# 이동거리나 절대위치를 입력합니다. # Enter the distance or absolute position.
				strInput = input("Enter Axis Position(mm): ")
				f64MovePosition = float(strInput)

				if eMotionFeature == EMotionFeature.MoveAbsolutePosition:
					# 절대 좌표로 이동합니다. # Move to absolute coordinates.
					if((res := motionAxis.MovePosition(f64MovePosition, f64MoveVelocity, f64MoveAccelAndDecel, f64MoveAccelAndDecel, False)).IsFail()):
						ErrorPrint(res, "Failed to move position.")
						break

					# 모션이 정지 될때까지 대기합니다. # Wait until motion stops.
					CThreadUtilities.Sleep(100)

					while motionAxis.IsMotionDone() == False:
						CThreadUtilities.Sleep(100)
				elif eMotionFeature == EMotionFeature.MoveIncrementalPosition:
					# 상대 좌표로 이동합니다. # Move to relative coordinates.
					if((res := motionAxis.MoveDistance(f64MovePosition, f64MoveVelocity, f64MoveAccelAndDecel, f64MoveAccelAndDecel, False)).IsFail()):
						ErrorPrint(res, "Failed to move distance.")
						break

					# 모션이 정지 될때까지 대기합니다. # Wait until motion stops.
					CThreadUtilities.Sleep(100)

					while motionAxis.IsMotionDone() == False:
						CThreadUtilities.Sleep(100)

		break

	# Motion 장치의 초기화를 해제합니다. # Terminate the Motion device.
	devMotion.Terminate()

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()