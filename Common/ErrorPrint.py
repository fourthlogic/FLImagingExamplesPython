
# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str = ""):
    if len(string) > 1:
        print(string)

    if res.IsFail():
        print(f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n")
