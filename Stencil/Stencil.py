# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

clr.AddReference("System")
from System.Text import StringBuilder

def main():
    viewImage = CGUIViewImage()
    res = CResult()

    while True:        
        # 이미지 뷰어 생성
        # Create the image viewer        
        if (res := viewImage.Create(200, 0, 800, 500)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 이미지 뷰어에서 0번째 레이어를 얻어 오기
        # Get the 0-th layer from the image viewer
        layer = viewImage.GetLayer(0)

        # 스텐실 클래스 인스턴스 생성
        # Create an instance of the stencil class
        stencil = CStencil()

        # 스텐실 클래스에 줄 간격을 0.2로 설정
        # Set the line spacing to 0.2 in the stencil
        if (res := stencil.SetLineSpacing(0.2)).IsFail():
            ErrorPrint(res, "Failed to set line spacing.")
            break

        # 스텐실 클래스에 자간을 0.3으로 설정
        # Set the letter spacing to 0.3 in the stencil
        if (res := stencil.SetLetterSpacing(0.3)).IsFail():
            ErrorPrint(res, "Failed to set letter spacing.")
            break

        # 스텐실 클래스에 폰트 사이즈를 24로 설정
        # Set the font size to 24 in the stencil
        if (res := stencil.SetFontSize(24)).IsFail():
            ErrorPrint(res, "Failed to set font size.")
            break

        # 스텐실 클래스에 Arial 폰트 페이스를 로드
        # Load the Arial font face into the stencil
        if (res := stencil.LoadFont("Arial")).IsFail():
            ErrorPrint(res, "Failed to load font : Arial.")
            break

        # 스텐실 클래스에 Cambria 폰트 페이스를 로드
        # Load the Cambria font face into the stencil
        if (res := stencil.LoadFont("Cambria")).IsFail():
            ErrorPrint(res, "Failed to load font : Cambria.")
            break

        # 로드한 폰트들 중 Arial을 선택
        # Select the Arial font among the loaded fonts
        if (res := stencil.SelectFont("Arial")).IsFail():
            ErrorPrint(res, "Failed to select font : Arial.")
            break

        # 선택한 폰트 이름을 얻어 오는 방법(참고)
        # Example: retrieve the currently selected font name
        sb = StringBuilder(1024)        
        if (res := stencil.GetSelectedFontName(sb)[0]).IsFail():
            ErrorPrint(res, "Failed to get selected font name.")
            break

        strFontName = sb.ToString()

        ## 선택한 폰트로 작성한 문자열을 도형으로 얻어 오기
        ## Convert a string to a figure using the selected font
        # 결과를 얻어 올 도형 생성
        # Create a figure array to store the result
        flfaRes = CFLFigureArray()
        
        # 문자열 설정
        # Define the string to render
        strText = "[Arial]\nFourthLogic CStencil class..."

        # 문자열을 도형으로 변환
        # Convert the string to a figure
        if (res := stencil.ConvertStringToFigure(strText, flfaRes)[0]).IsFail():
            ErrorPrint(res, "Failed to convert string to figure.")
            break

        # 도형을 레이어에 그려서 눈으로 확인할 수 있도록 합니다.
        # Draw the figure on the layer so it is visible
        layer.DrawFigureImage(flfaRes, EColor.BLACK, 1, EColor.YELLOW)

        # 로드된 폰트들 중 또다른 폰트인 Cambria를 선택
        # Select another font (Cambria) from the loaded fonts
        if (res := stencil.SelectFont("Cambria")).IsFail():
            ErrorPrint(res, "Failed to select font : Cambria.")
            break

        # 줄 간격을 1.0으로 설정
        # Set the line spacing to 1.0
        if (res := stencil.SetLineSpacing(1.0)).IsFail():
            ErrorPrint(res, "Failed to set line spacing.")
            break

        # 자간을 0으로 설정
        # Set the letter spacing to 0
        if (res := stencil.SetLetterSpacing(0)).IsFail():
            ErrorPrint(res, "Failed to set letter spacing.")
            break

        # 문자열 설정
        # Define a new string to render
        strText = "[Cambria]\nFourthLogic CStencil class..."
        
        # 문자열을 도형으로 변환
        # Convert the string to a figure
        if (res := stencil.ConvertStringToFigure(strText, flfaRes)[0]).IsFail():
            ErrorPrint(res, "Failed to convert string to figure.")
            break

        # 도형을 y방향으로 내리기
        # Offset the figure downward in the Y direction
        flfaRes.Offset(0.0, stencil.GetFontSize() * 5)

        # 도형을 레이어에 그려서 눈으로 확인할 수 있도록 합니다.
        # Draw the figure on the layer so it is visible
        layer.DrawFigureImage(flfaRes, EColor.BLACK, 1, EColor.CYAN)

        # 이미지 뷰어 갱신
        # Refresh the image viewer
        viewImage.Invalidate(True)

        # 이미지 뷰어가 닫히기 전까지 뷰어를 열려 있는 상태로 유지
        # Keep the viewer open until it is manually closed
        while viewImage.IsAvailable():
            CThreadUtilities.Sleep(1)

        break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()