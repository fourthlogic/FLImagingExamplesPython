
# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# 에러 출력 함수 // Error printing function
def ErrorPrint(res, string: str = ""):
    if len(string) > 1:
        print(string)

    resTmp = CResult()

    if isinstance(res, tuple):
        resTmp = res[0]
        ref_val = res[1:]
    else:
        resTmp = res
        ref_val = None

    if resTmp.IsFail():
        print(f"Error code : {resTmp.GetResultCode()}\nError name : {resTmp.GetString()}\n")
