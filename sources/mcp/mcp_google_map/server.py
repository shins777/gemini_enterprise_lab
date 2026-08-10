import os
import logging
import httpx
from fastmcp import FastMCP

# 로깅 객체 초기화 및 구성
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google-maps-mcp")

# 환경 변수를 통한 구글 맵 API 키 로드 및 FastMCP 기본 호스트/포트 수립
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
os.environ["FASTMCP_HOST"] = os.getenv("HOST", "0.0.0.0")
os.environ["FASTMCP_PORT"] = os.getenv("PORT", "8080")

# FastMCP 서버 인스턴스 기동
mcp = FastMCP("Google Maps MCP Server")


@mcp.tool()
async def search_location(query: str, location_bias: str = None) -> dict:
    """
    구글 맵스 API를 사용하여 위치, 특정 관심 장소(POI) 또는 주소를 정밀하게 탐색합니다.

    Args:
        query: 장소의 이름, 키워드 또는 명칭 (예: '에펠탑', '서울 강남역')
        location_bias: 가중치(Bias)를 주어 근처 위주로 찾을 위도,경도 문자열 (예: '37.5665,126.9780')

    Returns:
        일치하는 주소, 지도상의 위도/경도 좌표 및 고유 장소 ID(Place ID) 모음.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    if not api_key:
        return {"error": "구글 맵스 API 연동을 위한 GOOGLE_MAPS_API_KEY 환경변수가 설정되지 않았습니다."}

    async with httpx.AsyncClient() as client:
        # 최신 Places API (New) 엔드포인트를 적용합니다.
        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.id,places.rating,places.types"
        }
        payload = {"textQuery": query}
        if location_bias:
            try:
                lat, lng = map(float, location_bias.split(","))
                payload["locationBias"] = {
                    "circle": {
                        "center": {"latitude": lat, "longitude": lng},
                        "radius": 5000.0
                    }
                }
            except Exception:
                pass

        try:
            resp = await client.post(url, json=payload, headers=headers, timeout=10.0)
            data = resp.json()

            if "places" in data and data["places"]:
                results = []
                for place in data["places"][:5]:
                    results.append({
                        "name": place.get("displayName", {}).get("text"),
                        "formatted_address": place.get("formattedAddress"),
                        "location": {
                            "lat": place.get("location", {}).get("latitude"),
                            "lng": place.get("location", {}).get("longitude")
                        },
                        "place_id": place.get("id"),
                        "rating": place.get("rating"),
                        "types": place.get("types")
                    })
                return {"status": "SUCCESS", "query": query, "count": len(results), "results": results}
            
            return {"status": "NO_RESULTS", "message": f"'{query}'에 대한 위치 검색 결과가 존재하지 않습니다."}

        except Exception as e:
            logger.error(f"search_location 수행 도중 오류 발생: {e}")
            return {"status": "ERROR", "message": str(e)}


@mcp.tool()
async def search_restaurants(location: str) -> dict:
    """
    지정 장소, 역 주변 또는 명칭 검색을 기반으로 인기 평점이 우수한 식당(맛집) 상위 5곳을 탐색합니다.

    Args:
        location: 맛집을 찾을 기준 장소 (예: '강남역', '서울역', '판교')

    Returns:
        상위 5개 식당의 이름, 평점, 사용자 평가 개수, 주소, 카테고리 정보가 포함된 딕셔너리.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    if not api_key:
        return {"error": "구글 맵스 API 연동을 위한 GOOGLE_MAPS_API_KEY 환경변수가 설정되지 않았습니다."}

    query = f"{location} 맛집"
    async with httpx.AsyncClient() as client:
        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.id,places.rating,places.userRatingCount,places.priceLevel,places.types"
        }
        payload = {
            "textQuery": query,
            "languageCode": "ko"
        }

        try:
            resp = await client.post(url, json=payload, headers=headers, timeout=10.0)
            data = resp.json()

            if "places" in data and data["places"]:
                places = data["places"]
                
                # 식당 리스트를 평점 기준 내림차순 정렬 후 2차 가중치로 리뷰 갯수 기준 내림차순 정렬
                places.sort(key=lambda x: (x.get("rating", 0.0), x.get("userRatingCount", 0)), reverse=True)
                
                results = []
                for place in places[:5]:
                    price_level_map = {
                        "PRICE_LEVEL_FREE": "Free",
                        "PRICE_LEVEL_INEXPENSIVE": "$",
                        "PRICE_LEVEL_MODERATE": "$$",
                        "PRICE_LEVEL_EXPENSIVE": "$$$",
                        "PRICE_LEVEL_VERY_EXPENSIVE": "$$$$"
                    }
                    price_level = price_level_map.get(place.get("priceLevel"), "Unknown")
                    
                    results.append({
                        "name": place.get("displayName", {}).get("text"),
                        "formatted_address": place.get("formattedAddress"),
                        "rating": place.get("rating"),
                        "reviews_count": place.get("userRatingCount"),
                        "price_level": price_level,
                        "location": {
                            "lat": place.get("location", {}).get("latitude"),
                            "lng": place.get("location", {}).get("longitude")
                        },
                        "place_id": place.get("id"),
                        "types": place.get("types")
                    })
                return {"status": "SUCCESS", "location": location, "count": len(results), "results": results}
            
            return {"status": "NO_RESULTS", "message": f"'{location}' 인근에서 맛집을 발견하지 못했습니다."}

        except Exception as e:
            logger.error(f"search_restaurants 수행 도중 오류 발생: {e}")
            return {"status": "ERROR", "message": str(e)}


@mcp.tool()
async def calculate_distance(origin: str, destination: str, mode: str = "driving") -> dict:
    """
    출발지점과 도착지점 사이의 대략적인 이동 거리와 예상 요율 소요 시간을 추출합니다.

    Args:
        origin: 출발지 주소, 건물 명칭 또는 '위도,경도' 좌표셋 (예: '서울역')
        destination: 도착지 주소, 건물 명칭 또는 '위도,경도' 좌표셋 (예: '인천국제공항')
        mode: 이동 수단 종류 - 'driving' (자동차), 'walking' (도보), 'bicycling' (자전거), 'transit' (대중교통). 기본값은 'driving'.

    Returns:
        상세 연산된 실 이동 거리(미터) 및 실 요율 연산 시간(초) 정보가 포함된 결과셋.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    if not api_key:
        return {"error": "구글 맵스 API 연동을 위한 GOOGLE_MAPS_API_KEY 환경변수가 설정되지 않았습니다."}

    valid_modes = {
        "driving": "DRIVE",
        "walking": "WALK",
        "bicycling": "BICYCLE",
        "transit": "TRANSIT"
    }
    travel_mode = valid_modes.get(mode.lower(), "DRIVE")

    async with httpx.AsyncClient() as client:
        # 최신 구글 Routes API (New) 엔드포인트를 적용합니다.
        url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "*"
        }
        
        # 주소 문자열 혹은 위도/경도 입력 유무에 따른 웨이포인트(Waypoint) 빌드업
        origin_waypoint = {}
        if "," in origin:
            try:
                lat, lng = map(float, origin.split(","))
                origin_waypoint = {"location": {"latLng": {"latitude": lat, "longitude": lng}}}
            except Exception:
                origin_waypoint = {"address": origin}
        else:
            origin_waypoint = {"address": origin}

        dest_waypoint = {}
        if "," in destination:
            try:
                lat, lng = map(float, destination.split(","))
                dest_waypoint = {"location": {"latLng": {"latitude": lat, "longitude": lng}}}
            except Exception:
                dest_waypoint = {"address": destination}
        else:
            dest_waypoint = {"address": destination}

        payload = {
            "origins": [{"waypoint": origin_waypoint}],
            "destinations": [{"waypoint": dest_waypoint}],
            "travelMode": travel_mode
        }

        try:
            resp = await client.post(url, json=payload, headers=headers, timeout=10.0)
            data = resp.json()

            if isinstance(data, list) and len(data) > 0:
                result = data[0]
                
                # 경로 탐색 불가 시 대중교통으로 자동 롤백 시도
                if result.get("condition") == "ROUTE_NOT_FOUND" and travel_mode != "TRANSIT":
                    logger.info("선택된 이동 수단으로 경로 검색 불가. 대중교통(TRANSIT) 모드로 백업 시도 중...")
                    payload["travelMode"] = "TRANSIT"
                    resp = await client.post(url, json=payload, headers=headers, timeout=10.0)
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 0:
                        result = data[0]
                        mode = "transit"

                if "error" in result:
                    return {"status": "ERROR", "message": result["error"].get("message")}
                
                status_code = result.get("status", {}).get("code")
                if status_code and status_code != 0:
                    return {"status": "ERROR", "message": result.get("status", {}).get("message", "Routes API 내부 통신 장애")}

                if result.get("condition") == "ROUTE_NOT_FOUND":
                    return {"status": "NO_ROUTE", "message": "출발지와 목적지 간의 이동 경로를 탐색할 수 없습니다."}

                distance_meters = result.get("distanceMeters")
                duration_str = result.get("duration")
                duration_seconds = int(duration_str.rstrip("s")) if duration_str else 0
                
                # 현지화 텍스트 반환 처리
                localized = result.get("localizedValues", {})
                distance_text = localized.get("distance", {}).get("text", f"{distance_meters} m")
                duration_text = localized.get("duration", {}).get("text", f"{duration_seconds} s")

                return {
                    "status": "SUCCESS",
                    "origin": origin,
                    "destination": destination,
                    "travel_mode": mode,
                    "distance": distance_text,
                    "distance_meters": distance_meters,
                    "duration": duration_text,
                    "duration_seconds": duration_seconds
                }

            return {"status": "ERROR", "message": "경로 메트릭스 연산 결과가 존재하지 않습니다."}

        except Exception as e:
            logger.error(f"calculate_distance 수행 도중 오류 발생: {e}")
            return {"status": "ERROR", "message": str(e)}


if __name__ == "__main__":
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", "8080"))
    logger.info(f"구글 맵 FastMCP 서버를 {host}:{port}에서 streamable-http 전송 규격으로 가동합니다...")
    mcp.run(transport="streamable-http", host=host, port=port)
