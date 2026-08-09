import os
import csv
import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-realestate")

# Read environment variables and set FastMCP host/port
os.environ["FASTMCP_HOST"] = os.getenv("HOST", "0.0.0.0")
os.environ["FASTMCP_PORT"] = os.getenv("PORT", "8080")

# Initialize FastMCP Server
mcp = FastMCP("Korea Real Estate MCP Server")

# CSV File path
CSV_PATH = os.path.join(os.path.dirname(__file__), "korea_real_estate_20yr_factors.csv")

def load_data():
    data = []
    if not os.path.exists(CSV_PATH):
        logger.error(f"CSV file not found at {CSV_PATH}")
        return data
        
    try:
        with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "year": int(row["연도"]),
                    "interest_rate": float(row["한국은행 기준금리(%)"]),
                    "kospi": float(row["KOSPI 지수(기말)"]),
                    "seoul_apartment_avg_price": int(row["서울 아파트 평균매매가(만원)"]),
                    "regional_apartment_avg_price": int(row["지방 5대광역시 평균매매가(만원)"]),
                    "national_apartment_price_index": float(row["전국 아파트 매매가격지수(2021.01=100)"]),
                    "cpi": float(row["소비자물가지수(CPI, 2020=100)"]),
                    "m2_money_supply": int(row["M2 통화량(조원, 기말)"]),
                    "unsold_housing": int(row["전국 미분양주택(호)"])
                })
        logger.info(f"Loaded {len(data)} rows of real estate factors.")
    except Exception as e:
        logger.error(f"Error loading CSV data: {e}")
    return data

# Load data on startup
factors_data = load_data()


@mcp.tool()
async def get_factors_by_year(year: int) -> dict:
    """
    Retrieve economic indicators and real estate factors for a specific year (between 2006 and 2025).

    Args:
        year: The year to search for (e.g. 2021, 2023)

    Returns:
        Dictionary containing interest rate, KOSPI, apartment prices, CPI, M2 supply, and unsold housing.
    """
    for row in factors_data:
        if row["year"] == year:
            return {"status": "SUCCESS", "data": row}
            
    return {"status": "NOT_FOUND", "message": f"Data for year {year} not found. Available range: 2006-2025."}


@mcp.tool()
async def get_factors_range(start_year: int, end_year: int) -> dict:
    """
    Retrieve economic indicators and real estate factors for a range of years.

    Args:
        start_year: The beginning year (e.g. 2015)
        end_year: The ending year (e.g. 2023)

    Returns:
        List of indicators for each year in the range.
    """
    results = []
    for row in factors_data:
        if start_year <= row["year"] <= end_year:
            results.append(row)
            
    if results:
        return {"status": "SUCCESS", "count": len(results), "data": results}
    return {"status": "NO_RESULTS", "message": f"No data found in range {start_year} - {end_year}."}


@mcp.tool()
async def get_all_factors() -> dict:
    """
    Retrieve the entire 20-year history of Korean economic indicators and real estate factors.

    Returns:
        List of all data records from 2006 to 2025.
    """
    return {"status": "SUCCESS", "count": len(factors_data), "data": factors_data}


if __name__ == "__main__":
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", "8080"))
    logger.info(f"Starting Real Estate FastMCP Server on {host}:{port} with SSE transport...")
    mcp.run(transport="sse", host=host, port=port)
