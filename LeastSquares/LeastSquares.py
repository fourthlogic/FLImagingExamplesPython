# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


from System.Numerics import Complex
import random


# 메인 함수 // Main function
def main():
    arrStrEquation = [
        "Linear equation",
        "Quadratic equation",
        "Cubic equation",
        "Quartic equation",
        "Quintic equation"
    ]

    while True:
        strInput = input("Please input generate sample data count: ")
    
        if len(strInput) == 0:
            print("Please check the input.\n")
            break
    
        try:
            i32DataCount = int(strInput)
        except ValueError:
            print("Please check the input.\n")
            break
    
        if i32DataCount <= 0:
            print("Please check the input.\n")
            break
    
        # 입력 받은 개수만큼 데이터를 생성한다. // Generates data according to the number of inputs
        arrF64DataX = [0.0] * i32DataCount
        arrF64DataY = [0.0] * i32DataCount
    
        strSampleData = ""
        f64PrevX = 0.0
        f64PrevY = 0.0
        
        for i in range(i32DataCount):
            if len(strSampleData) != 0:
                strSampleData += ", "
    
            arrF64DataX[i] = f64PrevX + (random.randint(0, i32DataCount - 1) / 10.0)
    
            if random.randint(0, 1) % 2 != 0:
                arrF64DataY[i] = f64PrevY + (random.randint(0, i32DataCount - 1) / 10.0)
            else:
                arrF64DataY[i] = f64PrevY - (random.randint(0, i32DataCount - 1) / 10.0)
    
            f64PrevX = arrF64DataX[i]
            f64PrevY = arrF64DataY[i]
    
            strFormat = f"({arrF64DataX[i]}, {arrF64DataY[i]})"
            strSampleData += strFormat
    
        print("Sample Data")
        print(strSampleData)
        print("\n")
    
        # LeastSquares 객체 생성 // Create LeastSquares object
        leastSqaures = CLeastSquares[Double]()
    
        # 데이터를 할당 // Assign data
        leastSqaures.Assign(arrF64DataX, arrF64DataY, i32DataCount)
    
        for i in range(1, 6):
            # 계수 값을 받기 위해 List 생성 // Create List to receive coefficient values
            # R square 값을 받기 위해 double 선언 // Declare double for R square value
    
            # 다항식 계수를 얻는다. // Get polynomial coefficients
            res, listF64Output, f64TRSqr = leastSqaures.GetPoly(i, List[Double](), 0.0)
    
            if res.IsFail():
                print(f"Failed to get polynomial for degree {i}.\n")
                continue
    
            strEquation = ""
            i32Count = len(listF64Output)
    
            if i32Count == 0:
                continue
            
            listCoef = List[Complex]() 
    
            # 얻어온 계수로 다항식을 만든다. // Create polynomial with obtained coefficients
            for j in range(i32Count):
                f64Coef = listF64Output[j]
    
                listCoef.Add(Complex(f64Coef, 0.0))
    
                if f64Coef == 0.0:
                    continue
    
                if len(strEquation) != 0 and f64Coef > 0.0:
                    strEquation += " + "
    
                power = i32Count - 1 - j
    
                if power == 0:
                    strFormat = f"{f64Coef}"
                elif power == 1:
                    strFormat = f"{f64Coef}*x"
                else:
                    strFormat = f"{f64Coef}*x^{power}"
    
                strEquation += strFormat
            
            if len(strEquation) == 0:
                continue
    
            strDegree = arrStrEquation[i - 1]
            strR = f"R square value: {f64TRSqr}"
    
            print(strDegree)
            print(strR)
            print(strEquation)
    
            # 방정식의 해를 얻기위해 List<Complex> 생성 // Create List<Complex> to get solution of equation
            listEquationResult = List[Complex]()
    
            # 방정식의 해를 얻어온다. // Get the solution of the equation.
            res, listEquationResult = CEquation.Solve(listCoef, listEquationResult)
    
            if res.IsFail():
                print(f"Failed to solve equation for degree {i}.\n")
                continue
    
            # 방정식의 해를 표시한다. // Display the solution of the equation.
            strResult = "Result \n"
            
            for j in range(listEquationResult.Count):
                cpxResult = listEquationResult[j]
            
                if cpxResult.Imaginary == 0.0:
                    strCpx = f"{cpxResult.Real}"
                elif cpxResult.Imaginary > 0.0:
                    strCpx = f"{cpxResult.Real}+{cpxResult.Imaginary}i"
                else:
                    strCpx = f"{cpxResult.Real}{cpxResult.Imaginary}i"
            
                strResult += strCpx + "\n"
            
            strResult += "\n"
            print(strResult)
        
        break 
    
    # End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()