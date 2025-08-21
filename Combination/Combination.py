# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
    # 조합 객체 선언 # Declare a combination object
    combination = CCombination()

    while True:
        flstrResult = ""

        while True:
            print("Please input n and k as n, k.")
            print("Combination : k objects are selected from a set of n objects to produce subsets with no ordering.")
            print("ex) 6, 2")
            strInput = input("Input: ")

            if strInput == "":
                break

            # 입력 받은 문자열을 ',' 으로 구분하여 int 값으로 변환한다. # Separates the input string with ',' and converts it to an int value.
            arrStrInput = strInput.split(',')

            n = -1
            k = -1
            nCount = 0

            for input_val in arrStrInput:
                input_val = input_val.strip() # 공백 제거 # Remove whitespace
                if len(input_val) == 0:
                    break

                if nCount == 0:
                    try:
                        n = int(input_val)
                    except ValueError:
                        break
                elif nCount == 1:
                    try:
                        k = int(input_val)
                    except ValueError:
                        break
                else:
                    break

                nCount += 1
            
            # 입력값 유효성 검사 # Input validation
            if k <= 0 or n <= 0 or n < k or nCount < 2:
                flstrResult = "\nCount : 0"
                break

            # nCk, n 개에서 k 개를 선택하는 조합 # nCk, a combination of selecting k objects from n objects
            combination.SetMax(n)
            combination.SetSelection(k)

            # 조합을 계산 # Calculate combinations
            combination.Calculate()
            
            listCombination = List[List[Int32]]()
            # 조합 결과값 얻기 # Get combination result
            if (res := combination.GetResult(listCombination)[0]).IsFail():
                flstrResult = f"\nFailed to get combination result: {res.GetString()}"
                break

            flstrCombination = ""
            i64CombinationCnt = 0

            for combo in listCombination:
                flstrCombination += "("
                flstrCombination += " ".join(map(str, combo))
                flstrCombination += ")\n"
                i64CombinationCnt += 1

            flstrCnt = f"\nCount : {i64CombinationCnt}"

            flstrResult = flstrCombination + flstrCnt
            break
        
        if flstrResult == "":
            flstrResult = "Please check the input.\n"

        flstrResult += "\n\n"

        print(flstrResult)

        # 사용자가 입력 없이 Enter를 누르면 종료 # Exit if user presses Enter without input
        if strInput == "":
            break

    # End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()