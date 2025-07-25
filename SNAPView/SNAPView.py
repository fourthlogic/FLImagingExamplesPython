# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 스냅 뷰 객체 선언 // Declare the SNAP View
	viewSNAP = CGUIViewSNAP()

	while True:
		
		# 스냅 뷰 생성 // Create SNAP view
		if (res := viewSNAP.Create(0, 0, 600, 600)).IsFail():
			ErrorPrint(res, 'Failed to create the SNAP view.')
			break

		# 스냅 파일 로드 // Load SNAP file
		if (res := viewSNAP.Load('C:/Users/Public/Documents/FLImaging/FLImagingExamplesSNAP/Advanced Functions/Object/Blob.flsf')).IsFail():
			ErrorPrint(res, 'Failed to load the file.')
			break

		# 스냅 실행 // Run SNAP
		if (res := viewSNAP.Run()).IsFail():
			ErrorPrint(res, 'Failed to run the SNAP.')
			break

		# 스냅이 종료될 때 까지 기다림 // Wait for the SNAP to close
		while viewSNAP.IsAvailable():
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