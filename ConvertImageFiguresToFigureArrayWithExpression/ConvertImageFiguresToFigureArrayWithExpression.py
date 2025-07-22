# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():
	
    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage() for _ in range(4)]

    while True:

        # 이미지 뷰 생성 // Create image view
        if (res := viewImage[0].Create(400, 0, 812, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(812, 0, 1224, 384)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[2].Create(400, 384, 812, 768)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[3].Create(812, 384, 1224, 768)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        fliSource = CFLImage()

        # Source 이미지 로드 // Load the source image
        if (res := fliSource.Load("../../ExampleImages/Figure/ImageWithFigure.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        fliCopy = CFLImage(fliSource, False)
        fliCopy.ClearFigures()

        # 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
        if (res := viewImage[0].SetImagePtr(fliSource)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        for i in range(1, 4):
            # 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
            if (res := viewImage[i].SetImagePtr(fliCopy)[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.")
                break
        
        if (res := viewImage[3].SetImagePtr(fliCopy)[0]).IsFail():
            break

        # SourceView, ResultView 의 0번 레이어 가져오기 // Get Layer 0 of SourceView, ResultView
        layerSource = viewImage[0].GetLayer(0)
        layerResult1 = viewImage[1].GetLayer(0)
        layerResult2 = viewImage[2].GetLayer(0)
        layerResult3 = viewImage[3].GetLayer(0)

        layerSource.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Image", EColor.YELLOW, EColor.BLACK, 15)
        layerResult1.DrawTextCanvas(CFLPoint[Double](0, 0), "Result 1", EColor.YELLOW, EColor.BLACK, 15)
        layerResult2.DrawTextCanvas(CFLPoint[Double](0, 0), "Result 2", EColor.YELLOW, EColor.BLACK, 15)
        layerResult3.DrawTextCanvas(CFLPoint[Double](0, 0), "Result 3", EColor.YELLOW, EColor.BLACK, 15)

        for i in range(1, 4):
            # 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
            if (res := viewImage[0].SynchronizePointOfView(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize view")
                break
        
        if (res := viewImage[0].SynchronizePointOfView(viewImage[3])[0]).IsFail():
            break


        # 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
        for i in range(1, 4):
            if (res := viewImage[0].SynchronizeWindow(viewImage[i])[0]).IsFail():
                ErrorPrint(res, "Failed to synchronize window.")
                break
        
        if (res := viewImage[0].SynchronizeWindow(viewImage[3])[0]).IsFail():
            break

        # 지원되는 연산자 : [, ] , { , }, (, ), +, -, *, / , ^, <, >, <= , =<, >= , =>, != , =!, =, == , &, &&, and, | , || , or
        # 
        # 	연산자 설명
        # 	2 - 1. 괄호 연산자 : [, { , (,] , }, )
        # 	2 - 2. 덧셈 연산자 : +
        # 	2 - 3. 뺄셈 연산자 : -
        # 	2 - 4. 곱셈 연산자 : *
        # 	2 - 5. 나눗셈 연산자 : /
        # 	2 - 6. 거듭제곱 연산자 : ^
        # 	2 - 7. 관계 연산자 : <, >, <= , =<, >= , =>, != , =!, =, ==
        # 	2 - 8. 논리 곱 : &, &&, and
        # 	2 - 9. 논리 합 : | , || , or
        # 
        # 	같은 역할을 하는 연산자
        # 	3 - 1.[, { , (
        # 	3 - 2.], }, )
        # 	3 - 3. <= , = <
        # 	3 - 3. >= , =>
        # 	3 - 4. != , =!
        # 	3 - 5. =, ==
        # 	3 - 6. &, &&, and
        # 	3 - 7. | , || , or
        # 
        # 지원되는 Figure 조건식 
        #   넓이                                  : Area
        # 	둘레                                  : Perimeter
        # 	길이                                  : Length
        # 	폭                                    : Width
        # 	높이                                  : Height
        # 	각도                                  : Angle
        # 	중심의 x 좌표                         : Center.x
        # 	중심의 y 좌표                         : Center.y
        # 	무게중심의 x 좌표                     : CenterOfGravity.x
        # 	무게중심의 y 좌표                     : CenterOfGravity.y
        # 	BoundaryRect의 left                   : BoundaryRect.left 혹은 left
        # 	BoundaryRect의 top                    : BoundaryRect.top 혹은 top
        # 	BoundaryRect의 right                  : BoundaryRect.right 혹은 right
        # 	BoundaryRect의 bottom                 : BoundaryRect.bottom 혹은 bottom
        # 	최소 둘레 직사각형의 넓이             : MinimumEnclosingRectangleArea 혹은 MerArea
        # 	최소 둘레 직사각형의 둘레             : MinimumEnclosingRectanglePerimeter 혹은 MerPerimeter
        # 	최소 둘레 직사각형의 폭               : MinimumEnclosingRectangleWidth 혹은 MerWidth
        # 	최소 둘레 직사각형의 높이             : MinimumEnclosingRectangleHeight 혹은 MerHeight
        # 	최소 둘레 직사각형의 장변             : MinimumEnclosingRectangleLongSideLength 혹은 MerLongSideLength
        # 	최소 둘레 직사각형의 단변             : MinimumEnclosingRectangleShortSideLength 혹은 MerShortSideLength
        # 	최소 둘레 직사각형의 단변/장변 비율   : MinimumEnclosingRectangleShortLongRatio 혹은 MerShortLongRatio
        # 	최소 둘레 직사각형의 각도             : MinimumEnclosingRectangleAngle 혹은 MerAngle
        # 	최소 둘레 직사각형의 중심의 x 좌표    : MinimumEnclosingRectangleCenter.x 혹은 MerCenter.x
        # 	최소 둘레 직사각형의 중심의 y 좌표    : MinimumEnclosingRectangleCenter.y 혹은 MerCenter.y
        # 	최소 둘레 직사각형의 point0의 x 좌표  : MinimumEnclosingRectangle.point0.x 혹은 MER.point0.x
        # 	최소 둘레 직사각형의 point0의 y 좌표  : MinimumEnclosingRectangle.point0.y 혹은 MER.point0.y
        # 	최소 둘레 직사각형의 point1의 x 좌표  : MinimumEnclosingRectangle.point1.x 혹은 MER.point1.x
        # 	최소 둘레 직사각형의 point1의 y 좌표  : MinimumEnclosingRectangle.point1.y 혹은 MER.point1.y
        # 	최소 둘레 직사각형의 point2의 x 좌표  : MinimumEnclosingRectangle.point2.x 혹은 MER.point2.x
        # 	최소 둘레 직사각형의 point2의 y 좌표  : MinimumEnclosingRectangle.point2.y 혹은 MER.point2.y
        # 	최소 둘레 직사각형의 point3의 x 좌표  : MinimumEnclosingRectangle.point3.x 혹은 MER.point3.x
        # 	최소 둘레 직사각형의 point3의 y 좌표  : MinimumEnclosingRectangle.point3.y 혹은 MER.point3.y
        # 	내부의 모든 정점의 개수               : VertexCount
        #   도형 타입                             : Type
        #   이름                                  : Name
        #   인덱스                                : Index
        # 										 
        # 지원되는 함수						 
        #   최대값                                : Max 혹은 Maximum
        # 	최소값                                : Min 혹은 Minimum
        # 	평균값                                : Mean 혹은 Average 혹은 Avg
        # 	중간값                                : Median 혹은 Med
        # 	합                                    : Sum
        # 	제곱합                                : Sqrsum 혹은 Sumsqr
        # 	제곱근합                              : Sqrtsum 혹은 Sumsqrt
        # 	분산                                  : Variance 혹은 Var
        # 	표준편차                              : Stdev 혹은 Stddev

        # Supported Operators : [, ] , { , }, (, ), +, -, *, / , ^, <, >, <= , =<, >= , =>, != , =!, =, == , &, &&, and, | , || , or
        # 
        # 	Operator description
        # 	2 - 1. parenthesis operator : [, { , (,] , }, )
        # 	2 - 2. addition operator : +
        # 	2 - 3. subtraction operator : -
        # 	2 - 4. multiplication operator : *
        # 	2 - 5. division operator : /
        # 	2 - 6. power operator : ^
        # 	2 - 7. relational operator : <, >, <= , =<, >= , =>, != , =!, =, ==
        # 	2 - 8. logical product : &, &&, and
        # 	2 - 9. logical sum : | , || , or
        # 
        # 	Operators that do the same thing
        # 	3 - 1.[, { , (
        # 	3 - 2.], }, )
        # 	3 - 3. <= , = <
        # 	3 - 3. >= , =>
        # 	3 - 4. != , =!
        # 	3 - 5. =, ==
        # 	3 - 6. &, &&, and
        # 	3 - 7. | , || , or
        # 
        #  Supported figure conditional expressions
        #   area                                                   : Area
        # 	perimeter                                              : Perimeter
        # 	length                                                 : Length
        # 	width                                                  : Width
        # 	height                                                 : Height
        # 	angle                                                  : Angle
        # 	x-coordinate of center                                 : Center.x
        # 	y-coordinate of center                                 : Center.y
        # 	x-coordinate of the center of gravity                  : CenterOfGravity.x
        # 	y-coordinate of the center of gravity                  : CenterOfGravity.y
        # 	left of BoundaryRect                                   : BoundaryRect.left or left
        # 	top of BoundaryRect                                    : BoundaryRect.top or top
        # 	right of BoundaryRect                                  : BoundaryRect.right or right
        # 	bottom of BoundaryRect                                 : BoundaryRect.bottom or bottom
        # 	Area of minimum enclosing rectangle                    : MinimumEnclosingRectangleArea or MerArea
        # 	perimeter of minimum enclosing rectangle               : MinimumEnclosingRectanglePerimeter or MerPerimeter
        # 	width of minimum enclosing rectangle                   : MinimumEnclosingRectangleWidth or MerWidth
        # 	height of minimum enclosing rectangle                  : MinimumEnclosingRectangleHeight or MerHeight
        # 	long side length of minimum enclosing rectangle        : MinimumEnclosingRectangleLongSideLength or MerLongSideLength
        # 	short side length of minimum enclosing rectangle       : MinimumEnclosingRectangleShortSideLength or MerShortSideLength
        # 	short/long ratio of minimum enclosing rectangle        : MinimumEnclosingRectangleShortLongRatio or MerShortLongRatio
        # 	angle of minimum enclosing rectangle                   : MinimumEnclosingRectangleAngle or MerAngle
        # 	x-coordinate of center of minimum enclosing rectangle  : MinimumEnclosingRectangleCenter.x or MerCenter.x
        # 	y-coordinate of center of minimum enclosing rectangle  : MinimumEnclosingRectangleCenter.y or MerCenter.y
        # 	x-coordinate of point0 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point0.x or MER.point0.x
        # 	y-coordinate of point0 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point0.y or MER.point0.y
        # 	x-coordinate of point1 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point1.x or MER.point1.x
        # 	y-coordinate of point1 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point1.y or MER.point1.y
        # 	x-coordinate of point2 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point2.x or MER.point2.x
        # 	y-coordinate of point2 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point2.y or MER.point2.y
        # 	x-coordinate of point3 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point3.x or MER.point3.x
        # 	y-coordinate of point3 of minimum enclosing rectangle  : MinimumEnclosingRectangle.point3.y or MER.point3.y
        # 	the number of all vertices in the interior             : VertexCount
        #   type of figure                                         : Type
        #   name                                                   : Name
        #   index                                                  : Index
        # 										 
        #  Supported functions									 
        #   maximum value                                          : Max or Maximum
        # 	minimum value                                          : Min or Minimum
        # 	mean value                                             : Mean or Average or Avg
        # 	median value                                           : Median or Med
        # 	sum                                                    : Sum
        # 	sum of squares                                         : Sqrsum or Sumsqr
        # 	sum of square roots                                    : Sqrtsum or Sumsqrt
        # 	variance                                               : Variance or Var
        # 	standard deviation                                     : Stdev or Stddev

        # 조건식 문자열 // Condition string
        strExpression1 = "Name == '1 Flux'"

        # 조건식을 View에 표기 // Draw the conditional expression in the View
        layerResult1.DrawTextCanvas(CFLPoint[Double](0, 20), strExpression1, EColor.YELLOW, EColor.BLACK, 13)

        flfaResult1 = CFLFigureArray()
        # 조건식을 만족하는 Figure를 flfaResult1에 추출 // Extract the figure that satisfies the conditional expression to flfaResult1
        res, flfaResult1 = CFigureUtilities.ConvertImageFiguresToFigureArrayWithExpression(strExpression1, fliSource, flfaResult1)
        
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 조건식 문자열 // Condition string
        strExpression2 = "Name == '2 Rubber' && Width > 90"

        # 조건식을 View에 표기 // Draw the conditional expression in the View
        layerResult2.DrawTextCanvas(CFLPoint[Double](0, 20), strExpression2, EColor.YELLOW, EColor.BLACK, 13)

        flfaResult2 = CFLFigureArray()
        # 조건식을 만족하는 Figure를 flfaResult2에 추출 // Get the figure that satisfies the conditional expression to flfaResult2
        res, flfaResult2 = CFigureUtilities.ConvertImageFiguresToFigureArrayWithExpression(strExpression2, fliSource, flfaResult2)

        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # 조건식 문자열 // Condition string
        strExpression3 = "Center.x > mean('Center.x')"

        # 조건식을 View에 표기 // Draw the conditional expression in the View
        layerResult3.DrawTextCanvas(CFLPoint[Double](0, 20), strExpression3, EColor.YELLOW, EColor.BLACK, 13)

        flfaResult3 = CFLFigureArray()
        # 조건식을 만족하는 Figure를 flfaResult3에 추출 // Get the figure that satisfies the conditional expression to flfaResult3
        res, flfaResult3 = CFigureUtilities.ConvertImageFiguresToFigureArrayWithExpression(strExpression3, fliSource, flfaResult3)

        # res는 (CResult, 변경된 flfaResult3) 튜플을 반환 // res returns a (CResult, modified flfaResult3) tuple
        if res.IsFail():
            ErrorPrint(res, "Failed to process.")
            break

        # ResultView의 0번 레이어에 Result Figure 그리기 // Draw the Result Figure on Layer 0 of the ResultView
        layerResult1.DrawFigureImage(flfaResult1, EColor.BLACK, 3)
        layerResult1.DrawFigureImage(flfaResult1, EColor.LIME)
        layerResult2.DrawFigureImage(flfaResult2, EColor.BLACK, 3)
        layerResult2.DrawFigureImage(flfaResult2, EColor.LIME)
        layerResult3.DrawFigureImage(flfaResult3, EColor.BLACK, 3)
        layerResult3.DrawFigureImage(flfaResult3, EColor.LIME)

        # Console 출력 // Console output
        print("Result1 Figure that Name == '1 Flux'\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaResult1)}\n\n")

        print("Result2 Figure that Name == '2 Rubber' && Width > 90\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaResult2)}\n\n")

        print("Result3 Figure that Center.x > mean('Center.x')\n")
        print(f"{CFigureUtilities.ConvertFigureObjectToString(flfaResult3)}\n\n")

        # 이미지 뷰를 갱신 합니다. // Update image view
        for i in range(4):
            viewImage[i].Invalidate(True)
            viewImage[i].RedrawWindow()

        # 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
        while all(view.IsAvailable() for view in viewImage):
            CThreadUtilities.Sleep(1)
        
        break
    
    # End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()