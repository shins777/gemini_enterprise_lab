import os
import logging
import httpx
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google-maps-mcp")

# Read environment variables and set FastMCP host/port
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
os.environ["FASTMCP_HOST"] = os.getenv("HOST", "0.0.0.0")
os.environ["FASTMCP_PORT"] = os.getenv("PORT", "8080")

# Initialize FastMCP Server
mcp = FastMCP("Google Maps MCP Server")


@mcp.tool()
async def search_location(query: str, location_bias: str = None) -> dict:
    """
    Search for locations, places, or addresses using Google Maps API.

    Args:
        query: Name, address, or keyword of the location (e.g., 'Eiffel Tower', 'Gangnam Station, Seoul')
        location_bias: Optional 'latitude,longitude' string to bias results (e.g., '37.5665,126.9780')

    Returns:
        Dictionary containing matching places, formatted addresses, coordinates, and place IDs.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY environment variable is missing."}

    async with httpx.AsyncClient() as client:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {"query": query, "key": api_key}
        if location_bias:
            params["location"] = location_bias

        try:
            resp = await client.get(url, params=params, timeout=10.0)
            data = resp.json()

            if data.get("status") == "OK" and data.get("results"):
                results = []
                for place in data["results"][:5]:
                    results.append({
                        "name": place.get("name"),
                        "formatted_address": place.get("formatted_address"),
                        "location": place.get("geometry", {}).get("location"),
                        "place_id": place.get("place_id"),
                        "rating": place.get("rating"),
                        "types": place.get("types")
                    })
                return {"status": "SUCCESS", "query": query, "count": len(results), "results": results}
            
            # Fallback to Geocoding API if Place Search yields no results
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
            geo_resp = await client.get(geocode_url, params={"address": query, "key": api_key}, timeout=10.0)
            geo_data = geo_resp.json()

            if geo_data.get("status") == "OK" and geo_data.get("results"):
                results = []
                for place in geo_data["results"][:5]:
                    results.append({
                        "name": place.get("formatted_address"),
                        "formatted_address": place.get("formatted_address"),
                        "location": place.get("geometry", {}).get("location"),
                        "place_id": place.get("place_id"),
                        "types": place.get("types")
                    })
                return {"status": "SUCCESS", "query": query, "count": len(results), "results": results}

            return {"status": "NO_RESULTS", "message": f"No locations found for '{query}'.", "raw_status": data.get("status")}

        except Exception as e:
            logger.error(f"Error in search_location: {e}")
            return {"status": "ERROR", "message": str(e)}


@mcp.tool()
async def calculate_distance(origin: str, destination: str, mode: str = "driving") -> dict:
    """
    Calculate travel distance and estimated duration between origin and destination.

    Args:
        origin: Starting address, place name, or 'lat,lng' coordinates (e.g., 'Seoul Station')
        destination: Destination address, place name, or 'lat,lng' coordinates (e.g., 'Incheon Airport')
        mode: Travel mode - 'driving', 'walking', 'bicycling', or 'transit'. Default is 'driving'.

    Returns:
        Dictionary containing distance text/value (meters), duration text/value (seconds), origin/destination addresses.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY environment variable is missing."}

    valid_modes = ["driving", "walking", "bicycling", "transit"]
    if mode.lower() not in valid_modes:
        mode = "driving"

    async with httpx.AsyncClient() as client:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "mode": mode.lower(),
            "key": api_key
        }

        try:
            resp = await client.get(url, params=params, timeout=10.0)
            data = resp.json()

            if data.get("status") == "OK" and data.get("rows"):
                element = data["rows"][0]["elements"][0]
                if element.get("status") == "OK":
                    return {
                        "status": "SUCCESS",
                        "origin": data.get("origin_addresses", [origin])[0],
                        "destination": data.get("destination_addresses", [destination])[0],
                        "travel_mode": mode,
                        "distance": element.get("distance", {}).get("text"),
                        "distance_meters": element.get("distance", {}).get("value"),
                        "duration": element.get("duration", {}).get("text"),
                        "duration_seconds": element.get("duration", {}).get("value")
                    }
                else:
                    return {"status": "ELEMENT_ERROR", "message": element.get("status")}

            return {"status": "ERROR", "message": data.get("error_message", data.get("status"))}

        except Exception as e:
            logger.error(f"Error in calculate_distance: {e}")
            return {"status": "ERROR", "message": str(e)}


if __name__ == "__main__":
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = os.getenv("FASTMCP_PORT", "8080")
    logger.info(f"Starting Google Maps FastMCP Server on {host}:{port} with SSE transport...")
    mcp.run(transport="sse")
