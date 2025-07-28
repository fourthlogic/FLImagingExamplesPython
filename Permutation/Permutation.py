# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

    # 순열 객체 선언 // Declare permutation object
    permutation = CPermutation()

    while True:
        flstrResult = ""

        while True:
            print("Please input n and k as n, k.")
            print("Permutation : k objects are selected from a set of n objects to produce subsets with ordering.")
            print("ex) 6, 2")

            # n, k 문자열을 입력 받는다. // Receive n, k strings.
            strInput = input("Input: ")

            if strInput == "":
                break

            # 입력 받은 문자열을 ',' 으로 구분하여 int 값으로 변환한다. // Separates the input string with ',' and converts it to an int value.
            arrStrInput = strInput.split(',')

            n = -1
            k = -1
            nCount = 0

            for input_str in arrStrInput:
                input_str = input_str.strip()

                if len(input_str) == 0:
                    break

                if input_str == "\n":
                    break

                if nCount == 0:
                    try:
                        n = int(input_str)
                    except ValueError:
                        break 
                elif nCount == 1:
                    try:
                        k = int(input_str)
                    except ValueError:
                        break 
                else:
                    break 

                nCount += 1
            
            if nCount < 2 or n == -1 or k == -1:
                flstrResult = "Please check the input.\n"
                break

            if k <= 0 or n <= 0 or n < k:
                flstrResult = "\nCount : 0"
                break

            # nPk, n 개에서 k 개를 선택하는 순열 // nPk, a permutation of selecting k objects from n objects
            permutation.SetMax(n)
            permutation.SetSelection(k)

            # 순열을 계산 // Calculate the permutation
            permutation.Calculate()
            
            listPermutation = List[List[Int32]]()
            # 순열 결과값 얻기 // Get permutation result
            if (res := permutation.GetResult(listPermutation)[0]).IsFail():
               flstrResult = "Failed to get permutation result.\n"
               break

            flstrPermutation = ""
            i64PermutationCnt = 0
            
            for i in range(listPermutation.Count):
                inner_list = listPermutation[i]

                flstrPermutation += "("

                for j in range(inner_list.Count):
                    flstrPermutation += f" {inner_list[j]} "

                flstrPermutation += ")\n"
                i64PermutationCnt += 1

            flstrCnt = f"\nCount : {i64PermutationCnt}"
            flstrResult = flstrPermutation + flstrCnt
            
            break

        if flstrResult == "":
            flstrResult = "Please check the input.\n"

        flstrResult += "\n\n"
        print(flstrResult)
    
    # End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()