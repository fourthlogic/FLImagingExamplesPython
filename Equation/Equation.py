# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

from System.Numerics import Complex

# 메인 함수 // Main function
def main():
    arrStrEquation = [
        "Linear equation",
        "Quadratic equation",
        "Cubic equation",
        "Quartic equation",
        "Quintic equation"
    ]

    while True: # 메인 루프 시작 // Start main loop
        strResult = ""

        while True: 
            print("Please input equation coefficient.")
            print("ex) 7.2, 3.8, 10, 2.4")
            print("    7.2*x^3 + 3.8*x^2 + 10*x + 2.4\n")
            strInput = input("Input: ")

            if not strInput: # 입력이 없으면 내부 루프 종료 // If no input, break inner loop
                break

            # 계수 값을 담기위해 list 생성 // Create list to hold coefficient values
            listCoef = List[Complex]()

            # 입력 받은 문자열을 ',' 으로 구분하여 double 값으로 변환한다. // Separate the input string with ',' and convert it to a double value.
            arrStrInput = strInput.split(',')

            for input_val in arrStrInput:
                input_val = input_val.strip()
                if not input_val: # 공백이거나 비어있는 문자열은 건너뜀 // Skip empty or whitespace-only strings
                    continue

                try:
                    f64Input = float(input_val)
                    listCoef.Add(Complex(f64Input, 0.0))
                except ValueError:
                    # 파싱 실패 시 해당 입력은 건너뛰고 계속 진행 // If parsing fails, skip this input and continue
                    continue

            # 최상위 계수가 0 이면 제거해준다. // If the top coefficient is 0, remove it.
            while listCoef and listCoef[0].Real == 0.0:
                listCoef.pop(0)

            i32Count = len(listCoef)

            if i32Count < 2: # 최소한 선형 방정식 (계수 2개: ax + b) 이상이어야 함 // Must be at least a linear equation (2 coefficients: ax + b)
                break

            print("\n")

            # 입력 받은 계수로 수식을 만들어서 표시한다. // Create and display a formula with the entered coefficients.
            strDegree = ""
            if i32Count < 7:
                strDegree = arrStrEquation[i32Count - 2]
            else:
                strDegree = f"{i32Count - 1}th degree equation"

            print(strDegree)

            strEquation = ""

            for i in range(i32Count):
                f64Coef = listCoef[i].Real

                if f64Coef == 0.0:
                    continue

                if strEquation and f64Coef > 0.0:
                    strEquation += " + "

                strFormat = ""
                if i == i32Count - 2: # x^1 항 // x^1 term
                    strFormat = f"{f64Coef}*x"
                elif i == i32Count - 1: # 상수항 // Constant term
                    strFormat = f"{f64Coef}"
                else: # x^n 항 // x^n term
                    strFormat = f"{f64Coef}*x^{i32Count - 1 - i}"

                strEquation += strFormat

            print(strEquation)
            print("\n")

            # 방정식의 해를 얻기위해 list 생성 // Create list to get solution of equation
            listEquationResult = List[Complex]()

            # 방정식의 해를 얻어온다. // Get the solution of the equation.
            if (resTuple := CEquation.Solve(listCoef, listEquationResult))[0].IsFail():
                strResult = f"Failed to solve equation: {resTuple[0].GetString()}"
                break

            listEquationResult = resTuple[1] # 해결된 값을 listEquationResult에 할당 // Assign solved values to listEquationResult

            if not listEquationResult: # 결과 리스트가 비어있으면 // If result list is empty
                break

            # 방정식의 해를 표시한다. // Display the solution of the equation.
            strResult = "Result \n"

            for cpxResult in listEquationResult:
                strCpx = ""
                if cpxResult.Imaginary == 0.0: # 허수부가 0인 경우 // If imaginary part is 0
                    strCpx = f"{cpxResult.Real}"
                elif cpxResult.Imaginary > 0.0: # 허수부가 양수인 경우 // If imaginary part is positive
                    strCpx = f"{cpxResult.Real}+{cpxResult.Imaginary}i"
                else: # 허수부가 음수인 경우 // If imaginary part is negative
                    strCpx = f"{cpxResult.Real}{cpxResult.Imaginary}i"

                strResult += strCpx + "\n"
            
            break

        if not strResult:
            strResult = "Please check the input.\n"

        print(strResult)
        
        if not strInput:
            break
    
    # End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()