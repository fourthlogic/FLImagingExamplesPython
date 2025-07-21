# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time
import random

def main():
    # Declare the graph view
    viewGraphDark = CGUIViewGraph()
    viewGraphLight = CGUIViewGraph()

    while True:
        res = viewGraphDark.Create(100, 0, 100 + 440, 340)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the graph view.\n")
            break

        res = viewGraphLight.Create(100 + 440 * 1, 0, 100 + 440 * 2, 340)
        if res.IsFail():
            ErrorPrint(res, "Failed to create the graph view.\n")
            break

        res = viewGraphLight.SynchronizeWindow(viewGraphDark)
        if isinstance(res, tuple):  # ref parameter tuple 처리
            res = res[0]
        if res.IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # Set graph themes
        viewGraphDark.SetDarkMode()
        viewGraphLight.SetLightMode()

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

        # Plot the data
        viewGraphDark.Plot(arrF64DataX, arrF64DataY, i32DataCount, EChartType.Scatter, eColor, strName)
        viewGraphLight.Plot(arrF64DataX, arrF64DataY, i32DataCount, EChartType.Scatter, eColor, strName)

        viewGraphDark.ZoomFit()
        viewGraphLight.ZoomFit()

        while viewGraphDark.IsAvailable() and viewGraphLight.IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()