# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():
    # 조합 객체 선언 // Declare a combination object
    C = CCombination()

    while True:
        flstrResult = ""

        while True: # do-while loop in C# is typically a while True with a break
            print("Please input n and k as n, k.")
            print("Combination : k objects are selected from a set of n objects to produce subsets with no ordering.")
            print("ex) 6, 2")
            strInput = input("Input: ")

            if strInput == "":
                break

            # 입력 받은 문자열을 ',' 으로 구분하여 int 값으로 변환한다. // Separates the input string with ',' and converts it to an int value.
            arrStrInput = strInput.split(',')

            n = -1
            k = -1
            nCount = 0

            for input_val in arrStrInput:
                input_val = input_val.strip() # 공백 제거 // Remove whitespace
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
            
            # 입력값 유효성 검사 // Input validation
            if k <= 0 or n <= 0 or n < k or nCount < 2:
                flstrResult = "\nCount : 0"
                break # break from inner while loop

            # nCk, n 개에서 k 개를 선택하는 조합 // nCk, a combination of selecting k objects from n objects
            C.SetMax(n)
            C.SetSelection(k)

            # 조합을 계산 // Calculate combinations
            C.Calculate()
            
            InnerListType = List[Int32]
            OuterListType = List[InnerListType]
            listCombination = OuterListType()
            # 조합 결과값 얻기 // Get combination result
            # Python 바인딩에서는 ref 파라미터가 (CResult, 결과값) 튜플로 반환됨
            # In Python binding, ref parameters are returned as a (CResult, result_value) tuple
            resTuple = C.GetResult(listCombination) 
            res = resTuple[0]

            if res.IsFail():
                flstrResult = f"\nFailed to get combination result: {res.GetString()}"
                break
            
            # GetResult 함수가 채워준 리스트 또는 새로 반환된 리스트를 할당받습니다.
            # Assign the list populated by GetResult or a newly returned list.
            listCombination = resTuple[1] 

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

        # 사용자가 입력 없이 Enter를 누르면 종료 // Exit if user presses Enter without input
        if strInput == "":
            break

    # End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()