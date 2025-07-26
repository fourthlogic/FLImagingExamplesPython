# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import time
import random

def main():
	# 그래프 뷰 선언
    # Declare the graph view
    viewGraphDark = CGUIViewGraph()
    viewGraphLight = CGUIViewGraph()

    while True:        
		# Graph 뷰 생성 # Create graph view
        if (res := viewGraphDark.Create(100, 0, 100 + 440, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.")
            break

        if (res := viewGraphLight.Create(100 + 440 * 1, 0, 100 + 440 * 2, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.")
            break
        
		# Graph 뷰의 위치 동기화 # Synchronize the positions of windows
        if (res := viewGraphLight.SynchronizeWindow(viewGraphDark)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

		# 랜덤으로 100개의 데이터를 생성한다.
        # Generate 100 random data points
        i32DataCount = 100
        arrF64DataX = [0.0] * i32DataCount
        arrF64DataY = [0.0] * i32DataCount

        f64PrevX = 0.0
        f64PrevY = 0.0

        for i in range(i32DataCount):
            arrF64DataX[i] = f64PrevX + (random.randint(0, 99) / 10.0)
            if random.randint(0, 1) != 0:
                arrF64DataY[i] = f64PrevY + (random.randint(0, 99) / 10.0)
            else:
                arrF64DataY[i] = f64PrevY - (random.randint(0, 99) / 10.0)
            f64PrevX = arrF64DataX[i]
            f64PrevY = arrF64DataY[i]

        # Generate random color (equivalent to RGB from 3 bytes)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colorValue = (b << 16) | (g << 8) | r
        eColor = EColor(colorValue, True)

        strName = "Chart"
        
		# 그래프에 생성한 데이터를 추가한다. 
        # Plot the data
        if viewGraphDark.Plot(arrF64DataX, arrF64DataY, i32DataCount, EChartType.Scatter, eColor, strName) == -1:
            print("Failed to plot data.")
            break

        if viewGraphLight.Plot(arrF64DataX, arrF64DataY, i32DataCount, EChartType.Scatter, eColor, strName) == -1:
            print("Failed to plot data.")
            break
        
		# Graph 뷰의 스케일을 조정 # Sets the scales of the graph view.
        viewGraphDark.ZoomFit()
        viewGraphLight.ZoomFit()
        
		# Graph 뷰 테마를 다크모드로 설정 # Sets the theme of the graph view to dark mode.
        viewGraphDark.SetDarkMode()

		# Graph 뷰 테마를 라이트모드로 설정 # Sets the theme of the graph view to light mode.
        viewGraphLight.SetLightMode()
        
		# 그래프 뷰가 종료될 때 까지 기다림
        # Wait until the Graph views are closed
        while viewGraphDark.IsAvailable() and viewGraphLight.IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()