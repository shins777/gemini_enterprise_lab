import os
import csv
import logging
from fastmcp import FastMCP

# 로깅 객체 초기화 및 구성
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-realestate")

# 환경 변수를 통해 FastMCP 호스트 및 포트 번호 바인딩
os.environ["FASTMCP_HOST"] = os.getenv("HOST", "0.0.0.0")
os.environ["FASTMCP_PORT"] = os.getenv("PORT", "8080")

# FastMCP 서버 인스턴스 개시
mcp = FastMCP("Korea Real Estate MCP Server")

# 한국 부동산 20개년 시계열 지표 데이터셋 CSV 경로 설정
CSV_PATH = os.path.join(os.path.dirname(__file__), "korea_real_estate_20yr_factors.csv")

def load_data():
    """
    korea_real_estate_20yr_factors.csv 파일을 읽어서 메모리에 적재하는 헬퍼 함수입니다.
    """
    data = []
    if not os.path.exists(CSV_PATH):
        logger.error(f"지정된 위치에 부동산 CSV 파일이 누락되었습니다: {CSV_PATH}")
        return data
        
    try:
        # UTF-8 BOM 인코딩을 안전하게 해소하며 파일을 로드합니다.
        with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 완벽히 매핑 완료된 영문 표준 컬럼값을 기준으로 레코드를 가공 및 파싱합니다.
                data.append({
                    "year": int(row["year"]),
                    "interest_rate": float(row["interest_rate"]),
                    "kospi": float(row["kospi"]),
                    "seoul_apartment_avg_price": int(row["seoul_apartment_avg_price"]),
                    "regional_apartment_avg_price": int(row["regional_apartment_avg_price"]),
                    "national_apartment_price_index": float(row["national_apartment_price_index"]),
                    "cpi": float(row["cpi"]),
                    "m2_money_supply": int(row["m2_money_supply"]),
                    "unsold_housing": int(row["unsold_housing"])
                })
        logger.info(f"성공적으로 {len(data)}행의 한국 부동산 요인 데이터가 메모리에 로드되었습니다.")
    except Exception as e:
        logger.error(f"CSV 데이터를 로드하는 중 심각한 예외 오류가 발생했습니다: {e}")
    return data

# 서버 기동 시점에 실시간으로 시계열 매트릭스를 로딩합니다.
factors_data = load_data()


@mcp.tool()
async def get_factors_by_year(year: int) -> dict:
    """
    지정된 단일 연도(2006년 ~ 2025년 사이)의 주요 거시경제 지표 및 한국 부동산 가격 요인을 질의합니다.

    Args:
        year: 조회할 대상 연도 (예: 2021, 2023)

    Returns:
        기준금리, KOSPI, 서울/지방 아파트 가격 및 물가지수, M2 통화량, 미분양 누적량 정보를 포함하는 딕셔너리.
    """
    for row in factors_data:
        if row["year"] == year:
            return {"status": "SUCCESS", "data": row}
            
    return {"status": "NOT_FOUND", "message": f"{year}년도에 해당하는 데이터를 수집할 수 없습니다. 가용 연도 범위: 2006-2025년."}


@mcp.tool()
async def get_factors_range(start_year: int, end_year: int) -> dict:
    """
    시작 연도와 종료 연도 간의 다년도 한국 부동산 및 거시경제 지표 시계열 배열을 조회합니다.

    Args:
        start_year: 조회 기간의 시작 연도 (예: 2015)
        end_year: 조회 기간의 종료 연도 (예: 2023)

    Returns:
        지정 기간 범위에 해당되는 연도별 경제 및 부동산 요인 데이터 리스트.
    """
    results = []
    for row in factors_data:
        if start_year <= row["year"] <= end_year:
            results.append(row)
            
    if results:
        return {"status": "SUCCESS", "count": len(results), "data": results}
    return {"status": "NO_RESULTS", "message": f"{start_year}년 ~ {end_year}년 범위 내에 매칭되는 지표 데이터가 존재하지 않습니다."}


@mcp.tool()
async def get_all_factors() -> dict:
    """
    2006년부터 2025년까지의 전체 시계열 한국 부동산 및 주가, 이자율 요인 전체 데이터를 가져옵니다.

    Returns:
        20년치 전체 원천 데이터베이스 레코드 목록.
    """
    return {"status": "SUCCESS", "count": len(factors_data), "data": factors_data}


if __name__ == "__main__":
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", "8080"))
    logger.info(f"실시간 한국 부동산 FastMCP 서버를 {host}:{port} 경로에서 streamable-http 기반으로 시작합니다...")
    mcp.run(transport="streamable-http", host=host, port=port)
