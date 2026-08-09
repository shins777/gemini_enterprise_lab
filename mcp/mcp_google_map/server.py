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
        # Use Places API (New)
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
            
            return {"status": "NO_RESULTS", "message": f"No locations found for '{query}'."}

        except Exception as e:
            logger.error(f"Error in search_location: {e}")
            return {"status": "ERROR", "message": str(e)}


@mcp.tool()
async def search_restaurants(location: str) -> dict:
    """
    Search for top 5 highly-rated and popular restaurants or eateries in a specific location or area.

    Args:
        location: Name of the station, area, neighborhood, or city to find restaurants in (e.g. '강남역', 'Seoul Station').

    Returns:
        Dictionary containing top 5 restaurant details: name, rating, reviews count, formatted address, types, and price level.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY environment variable is missing."}

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
                
                # Sort by rating descending, then by userRatingCount descending
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
            
            return {"status": "NO_RESULTS", "message": f"No restaurants found for '{location}'."}

        except Exception as e:
            logger.error(f"Error in search_restaurants: {e}")
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

    valid_modes = {
        "driving": "DRIVE",
        "walking": "WALK",
        "bicycling": "BICYCLE",
        "transit": "TRANSIT"
    }
    travel_mode = valid_modes.get(mode.lower(), "DRIVE")

    async with httpx.AsyncClient() as client:
        # Use Routes API (New)
        url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "*"
        }
        
        # Build waypoint payloads
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
                
                # Check for routing success, fallback to TRANSIT if ROUTE_NOT_FOUND
                if result.get("condition") == "ROUTE_NOT_FOUND" and travel_mode != "TRANSIT":
                    logger.info("Route not found. Retrying with TRANSIT travel mode as fallback...")
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
                    return {"status": "ERROR", "message": result.get("status", {}).get("message", "Routes API error")}

                if result.get("condition") == "ROUTE_NOT_FOUND":
                    return {"status": "NO_ROUTE", "message": "No route could be found between origin and destination."}

                distance_meters = result.get("distanceMeters")
                duration_str = result.get("duration")
                duration_seconds = int(duration_str.rstrip("s")) if duration_str else 0
                
                # Fetch localized text values if available
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

            return {"status": "ERROR", "message": "No route matrix results found."}

        except Exception as e:
            logger.error(f"Error in calculate_distance: {e}")
            return {"status": "ERROR", "message": str(e)}


if __name__ == "__main__":
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", "8080"))
    logger.info(f"Starting Google Maps FastMCP Server on {host}:{port} with streamable-http transport...")
    mcp.run(transport="streamable-http", host=host, port=port)
