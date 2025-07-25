# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 스냅 빌드 객체 선언 // Declare SNAP Build
	buildSNAP = CSNAPBuild()

	while True:

		# 스냅 파일 로드 // Load SNAP file
		if (res := buildSNAP.Load('C:/Users/Public/Documents/FLImaging/FLImagingExamplesSNAP/Advanced Functions/Object/Blob.flsf')).IsFail():
			ErrorPrint(res, 'Failed to load the file.')
			break

		# 스냅 실행 // Run SNAP
		if (res := buildSNAP.Run()).IsFail():
			ErrorPrint(res, 'Failed to run the SNAP.')
			break

		# 스냅이 종료될 때 까지 기다림 // Wait for the SNAP to close
		while buildSNAP.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()