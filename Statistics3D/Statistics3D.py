# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():
	# 3D 객체 선언 # Declare 3D object
	floSource = CFL3DObject()

	# 3D 뷰 선언 # Declare 3D view
	view3DSrc = CGUIView3D()

	while True:

		# 수행 결과 객체 선언 # Declare execution result object
		res = CResult(EResult.UnknownError)

		# Source 3D Object 로드 # Load Source 3D Object
		if (res := floSource.Load("../../ExampleImages/Statistics3D/Sphere.ply")).IsFail():
			ErrorPrint(res, "Failed to load the 3D object file.")
			break
		
		# Source 3D 뷰 생성 # Create Source 3D view
		if (res := view3DSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.")
			break
		
		# Statistics 3D 객체 생성 # Create Statistics 3D object
		statistics3D = CStatistics3D()

		# Source 3D Object 설정 # Set Source 3D Object
		if (res := statistics3D.SetSourceObject(floSource)[0]).IsFail():
			ErrorPrint(res, "Failed to set Source 3D Object.")
			break
		
		# 사전 계산 여부 설정 # Set pre calculated value hold flag
		if (res := statistics3D.EnablePreCalculatedHold(True)).IsFail():
			ErrorPrint(res, "Failed to set pre calculated flag.")
			break
		
		# 위치 데이터 불러오기 # Get position data
		tpPositionMin = TPoint3[Double]()
		tpPositionMax = TPoint3[Double]()
		tpPositionSum = TPoint3[Double]()
		tpPositionSumOfSquares = TPoint3[Double]()
		tpPositionMean = TPoint3[Double]()
		tpPositionMedian = TPoint3[Double]()
		tpPositionVariance = TPoint3[Double]()
		tpPositionStandardDeviation = TPoint3[Double]()
		tpPositionCoefficientOfVariance = TPoint3[Double]()
		tpPositionLowerQuartile = TPoint3[Double]()
		tpPositionUpperQuartile = TPoint3[Double]()

		f64PositionCovarianceXY = 0
		f64PositionCovarianceXZ = 0
		f64PositionCovarianceYZ = 0

		f64PositionCorrelationCoefficientXY = 0
		f64PositionCorrelationCoefficientXZ = 0
		f64PositionCorrelationCoefficientYZ = 0
		
		if (res := statistics3D.GetPointPositionMin(tpPositionMin)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's min")
			break
		
		if (res := statistics3D.GetPointPositionMax(tpPositionMax)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's max")
			break
		
		if (res := statistics3D.GetPointPositionSum(tpPositionSum)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's sum")
			break
		
		if (res := statistics3D.GetPointPositionSumOfSquares(tpPositionSumOfSquares)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's sum of squares")
			break
		
		if (res := statistics3D.GetPointPositionMean(tpPositionMean)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's mean")
			break
		
		if (res := statistics3D.GetPointPositionMedian(tpPositionMedian)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's median")
			break
		
		if (res := statistics3D.GetPointPositionVariance(tpPositionVariance)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's variance")
			break
		
		if (res := statistics3D.GetPointPositionStandardDeviation(tpPositionStandardDeviation)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's standard deviation")
			break
		
		if (res := statistics3D.GetPointPositionCoefficientOfVariance(tpPositionCoefficientOfVariance)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's coefficient of variance")
			break
		
		if (res := statistics3D.GetPointPositionLowerQuartile(tpPositionLowerQuartile)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's lower quartile")
			break
		
		if (res := statistics3D.GetPointPositionUpperQuartile(tpPositionUpperQuartile)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's upper quartile")
			break
		
		statistics3D.SetCorrelatedPointPosition(CStatistics3D.EPointPosition.X, CStatistics3D.EPointPosition.Y)

		if (res := statistics3D.GetPointPositionCovariance(f64PositionCovarianceXY)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's covariance")
			break
		
		f64PositionCovarianceXY = statistics3D.GetPointPositionCovariance(f64PositionCovarianceXY)[1]
		
		statistics3D.SetCorrelatedPointPosition(CStatistics3D.EPointPosition.X, CStatistics3D.EPointPosition.Z)

		if (res := statistics3D.GetPointPositionCovariance(f64PositionCovarianceXZ)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's covariance")
			break
		
		f64PositionCovarianceXZ = statistics3D.GetPointPositionCovariance(f64PositionCovarianceXZ)[1]
		
		statistics3D.SetCorrelatedPointPosition(CStatistics3D.EPointPosition.Y, CStatistics3D.EPointPosition.Z)

		if (res := statistics3D.GetPointPositionCovariance(f64PositionCovarianceYZ)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's covariance")
			break
		
		f64PositionCovarianceYZ = statistics3D.GetPointPositionCovariance(f64PositionCovarianceYZ)[1]
		
		statistics3D.SetCorrelatedPointPosition(CStatistics3D.EPointPosition.X, CStatistics3D.EPointPosition.Y)

		if (res := statistics3D.GetPointPositionCorrelationCoefficient(f64PositionCorrelationCoefficientXY)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's correlation coefficient")
			break
		
		f64PositionCorrelationCoefficientXY = statistics3D.GetPointPositionCorrelationCoefficient(f64PositionCorrelationCoefficientXY)[1]
		
		statistics3D.SetCorrelatedPointPosition(CStatistics3D.EPointPosition.X, CStatistics3D.EPointPosition.Z)

		if (res := statistics3D.GetPointPositionCorrelationCoefficient(f64PositionCorrelationCoefficientXZ)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's correlation coefficient")
			break
		
		f64PositionCorrelationCoefficientXZ = statistics3D.GetPointPositionCorrelationCoefficient(f64PositionCorrelationCoefficientXZ)[1]
		
		statistics3D.SetCorrelatedPointPosition(CStatistics3D.EPointPosition.Y, CStatistics3D.EPointPosition.Z)

		if (res := statistics3D.GetPointPositionCorrelationCoefficient(f64PositionCorrelationCoefficientYZ)[0]).IsFail():
			ErrorPrint(res, "Failed to get point position's correlation coefficient")
			break
		
		f64PositionCorrelationCoefficientYZ = statistics3D.GetPointPositionCorrelationCoefficient(f64PositionCorrelationCoefficientYZ)[1]
		
		# 색 데이터 불러오기 # Get color data
		mvColorMin = CMultiVar[Double]()
		mvColorMax = CMultiVar[Double]()
		mvColorSum = CMultiVar[Double]()
		mvColorSumOfSquares = CMultiVar[Double]()
		mvColorMean = CMultiVar[Double]()
		mvColorMedian = CMultiVar[Double]()
		mvColorVariance = CMultiVar[Double]()
		mvColorStandardDeviation = CMultiVar[Double]()
		mvColorCoefficientOfVariance = CMultiVar[Double]()
		mvColorLowerQuartile = CMultiVar[Double]()
		mvColorUpperQuartile = CMultiVar[Double]()

		f64ColorCovarianceBG = 0.0
		f64ColorCovarianceBR = 0.0
		f64ColorCovarianceGR = 0.0

		f64ColorCorrelationCoefficientBG = 0.0
		f64ColorCorrelationCoefficientBR = 0.0
		f64ColorCorrelationCoefficientGR = 0.0

		if (res := statistics3D.GetPointColorMin(mvColorMin)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's min")
			break
		
		if (res := statistics3D.GetPointColorMax(mvColorMax)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's max")
			break
		
		if (res := statistics3D.GetPointColorSum(mvColorSum)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's sum")
			break
		
		if (res := statistics3D.GetPointColorSumOfSquares(mvColorSumOfSquares)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's sum of squares")
			break
		
		if (res := statistics3D.GetPointColorMean(mvColorMean)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's mean")
			break
		
		if (res := statistics3D.GetPointColorMedian(mvColorMedian)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's median")
			break
		
		if (res := statistics3D.GetPointColorVariance(mvColorVariance)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's variance")
			break
		
		if (res := statistics3D.GetPointColorStandardDeviation(mvColorStandardDeviation)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's standard deviation")
			break
		
		if (res := statistics3D.GetPointColorCoefficientOfVariance(mvColorCoefficientOfVariance)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's coefficient of variance")
			break
		
		if (res := statistics3D.GetPointColorLowerQuartile(mvColorLowerQuartile)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's lower quartile")
			break
		
		if (res := statistics3D.GetPointColorUpperQuartile(mvColorUpperQuartile)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's upper quartile")
			break
		
		statistics3D.SetCorrelatedPointColor(CStatistics3D.EPointColor.B, CStatistics3D.EPointColor.G)

		if (res := statistics3D.GetPointColorCovariance(f64ColorCovarianceBG)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's covariance")
			break
		
		f64ColorCovarianceBG = statistics3D.GetPointColorCovariance(f64ColorCovarianceBG)[1]
		
		statistics3D.SetCorrelatedPointColor(CStatistics3D.EPointColor.B, CStatistics3D.EPointColor.R)

		if (res := statistics3D.GetPointColorCovariance(f64ColorCovarianceBR)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's covariance")
			break
		
		f64ColorCovarianceBR = statistics3D.GetPointColorCovariance(f64ColorCovarianceBR)[1]
		
		statistics3D.SetCorrelatedPointColor(CStatistics3D.EPointColor.G, CStatistics3D.EPointColor.R)

		if (res := statistics3D.GetPointColorCovariance(f64ColorCovarianceGR)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's covariance")
			break
		
		f64ColorCovarianceGR = statistics3D.GetPointColorCovariance(f64ColorCovarianceGR)[1]
		
		statistics3D.SetCorrelatedPointColor(CStatistics3D.EPointColor.B, CStatistics3D.EPointColor.G)

		if (res := statistics3D.GetPointColorCorrelationCoefficient(f64ColorCorrelationCoefficientBG)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's correlation coefficient")
			break
		
		f64ColorCorrelationCoefficientBG = statistics3D.GetPointColorCorrelationCoefficient(f64ColorCorrelationCoefficientBG)[1]
		
		statistics3D.SetCorrelatedPointColor(CStatistics3D.EPointColor.B, CStatistics3D.EPointColor.R)

		if (res := statistics3D.GetPointColorCorrelationCoefficient(f64ColorCorrelationCoefficientBR)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's correlation coefficient")
			break
		
		f64ColorCorrelationCoefficientBR = statistics3D.GetPointColorCorrelationCoefficient(f64ColorCorrelationCoefficientBR)[1]
		
		statistics3D.SetCorrelatedPointColor(CStatistics3D.EPointColor.G, CStatistics3D.EPointColor.R)

		if (res := statistics3D.GetPointColorCorrelationCoefficient(f64ColorCorrelationCoefficientGR)[0]).IsFail():
			ErrorPrint(res, "Failed to get point color's correlation coefficient")
			break
		
		f64ColorCorrelationCoefficientGR = statistics3D.GetPointColorCorrelationCoefficient(f64ColorCorrelationCoefficientGR)[1]
		
		# 면 데이터 불러오기 # Get face data
		f64SurfaceArea = 0.0
		
		if (res := statistics3D.GetSurfaceArea(f64SurfaceArea)[0]).IsFail():
			ErrorPrint(res, "Failed to get face's surface area")
			break
		
		f64SurfaceArea = statistics3D.GetSurfaceArea(f64SurfaceArea)[1]
		
		# 콘솔에 데이터 출력 # Print data to console
		print(" < Point Position Data >")

		print(f"Min ->\tX: {tpPositionMin.x:.7}\tY: {tpPositionMin.y:.7}\tZ: {tpPositionMin.z:.7}")
		print(f"Max ->\tX: {tpPositionMax.x:.7}\tY: {tpPositionMax.y:.7}\tZ: {tpPositionMax.z:.7}")
		print(f"Sum ->\tX: {tpPositionSum.x:.7}\tY: {tpPositionSum.y:.7}\tZ: {tpPositionSum.z:.7}")
		print(f"Sum Of Squares ->\tX: {tpPositionSumOfSquares.x:.7}\tY: {tpPositionSumOfSquares.y:.7}\tZ: {tpPositionSumOfSquares.z:.7}")
		print(f"Mean ->\tX: {tpPositionMean.x:.7}\tY: {tpPositionMean.y:.7}\tZ: {tpPositionMean.z:.7}")
		print(f"Median ->\tX: {tpPositionMedian.x:.7}\tY: {tpPositionMedian.y:.7}\tZ: {tpPositionMedian.z:.7}")
		print(f"Variance ->\tX: {tpPositionVariance.x:.7}\tY: {tpPositionVariance.y:.7}\tZ: {tpPositionVariance.z:.7}")
		print(f"Standard Deviation ->\tX: {tpPositionStandardDeviation.x:.7}\tY: {tpPositionStandardDeviation.y:.7}\tZ: {tpPositionStandardDeviation.z:.7}")
		print(f"Coefficient Of Variance ->\tX: {tpPositionCoefficientOfVariance.x:.7}\tY: {tpPositionCoefficientOfVariance.y:.7}\tZ: {tpPositionCoefficientOfVariance.z:.7}")
		print(f"Lower Quartile ->\tX: {tpPositionLowerQuartile.x:.7}\tY: {tpPositionLowerQuartile.y:.7}\tZ: {tpPositionLowerQuartile.z:.7}")
		print(f"Upper Quartile ->\tX: {tpPositionUpperQuartile.x:.7}\tY: {tpPositionUpperQuartile.y:.7}\tZ: {tpPositionUpperQuartile.z:.7}")

		print(f"Covariance ->\tXY: {f64PositionCovarianceXY:.7}\tXZ: {f64PositionCovarianceXZ:.7}\tYZ: {f64PositionCovarianceYZ:.7}")
		print(f"Correlation Coefficient ->\tXY: {f64PositionCorrelationCoefficientXY:.7}\tXZ: {f64PositionCorrelationCoefficientXZ:.7}\tYZ: {f64PositionCorrelationCoefficientYZ:.7}")

		print("")

		print(" < Point Color Data >")

		print(f"Min ->\tB: {mvColorMin.GetAt(0):.7}\tG: {mvColorMin.GetAt(1):.7}\tR: {mvColorMin.GetAt(2):.7}")
		print(f"Max ->\tB: {mvColorMax.GetAt(0):.7}\tG: {mvColorMax.GetAt(1):.7}\tR: {mvColorMax.GetAt(2):.7}")
		print(f"Sum ->\tB: {mvColorSum.GetAt(0):.7}\tG: {mvColorSum.GetAt(1):.7}\tR: {mvColorSum.GetAt(2):.7}")
		print(f"Sum Of Squares ->\tB: {mvColorSumOfSquares.GetAt(0):.7}\tG: {mvColorSumOfSquares.GetAt(1):.7}\tR: {mvColorSumOfSquares.GetAt(2):.7}")
		print(f"Mean ->\tB: {mvColorMean.GetAt(0):.7}\tG: {mvColorMean.GetAt(1):.7}\tR: {mvColorMean.GetAt(2):.7}")
		print(f"Median ->\tB: {mvColorMedian.GetAt(0):.7}\tG: {mvColorMedian.GetAt(1):.7}\tR: {mvColorMedian.GetAt(2):.7}")
		print(f"Variance ->\tB: {mvColorVariance.GetAt(0):.7}\tG: {mvColorVariance.GetAt(1):.7}\tR: {mvColorVariance.GetAt(2):.7}")
		print(f"Standard Deviation ->\tB: {mvColorStandardDeviation.GetAt(0):.7}\tG: {mvColorStandardDeviation.GetAt(1):.7}\tR: {mvColorStandardDeviation.GetAt(2):.7}")
		print(f"Coefficient Of Variance ->\tB: {mvColorCoefficientOfVariance.GetAt(0):.7}\tG: {mvColorCoefficientOfVariance.GetAt(1):.7}\tR: {mvColorCoefficientOfVariance.GetAt(2):.7}")
		print(f"Lower Quartile ->\tB: {mvColorLowerQuartile.GetAt(0):.7}\tG: {mvColorLowerQuartile.GetAt(1):.7}\tR: {mvColorLowerQuartile.GetAt(2):.7}")
		print(f"Upper Quartile ->\tB: {mvColorUpperQuartile.GetAt(0):.7}\tG: {mvColorUpperQuartile.GetAt(1):.7}\tR: {mvColorUpperQuartile.GetAt(2):.7}")

		print(f"Covariance ->\tBG: {f64ColorCovarianceBG:.7}\tBR: {f64ColorCovarianceBR:.7}\tGR: {f64ColorCovarianceGR:.7}")
		print(f"Correlation Coefficient ->\tBG: {f64ColorCorrelationCoefficientBG:.7}\tBR: {f64ColorCorrelationCoefficientBR:.7}\tGR: {f64ColorCorrelationCoefficientGR:.7}")

		print("")

		print(" < Face Data >")

		print(f"Surface Area: {f64SurfaceArea:.7}")

		print("")


		# 화면에 출력하기 위해 3D 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from 3D view for display
		# 이 객체는 3D 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an 3D view and does not need to be released
		layer3DSource = view3DSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear figures drawn on existing layer
		layer3DSource.Clear()

		# 3D 뷰 정보 표시 # Display 3D view information
		if (res := layer3DSource.DrawTextCanvas(CFLPoint[Double](0, 0), "Source 3D Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.")
			break
		
		# 입력 3D 객체 출력 # Print input 3D Object
		if (res := view3DSrc.PushObject(floSource)).IsFail():
			ErrorPrint(res, "Failed to display the 3D Object.")
			break
		
		# 새로 생성한 3D Object를 가지는 뷰 Zoom Fit 실행 # Activate Zoom Fit for view with newly created 3D object
		if (res := view3DSrc.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit 3D view.")
			break
		
		# 3D 뷰를 갱신 # Update 3D view
		view3DSrc.Invalidate(True)

		# 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until a view is closed before exiting
		while view3DSrc.IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
    main()
