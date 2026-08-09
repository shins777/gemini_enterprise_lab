import asyncio
import subprocess
import sys
from mcp import ClientSession
from mcp.client.sse import sse_client

SERVICE_URL = "https://korea-realestate-mcp-yn77fvmwva-uc.a.run.app"

def get_gcloud_access_token() -> str:
    """
    Retrieves Google OAuth2 Access Token from local application-default credentials.
    """
    print("Retrieving GCP OAuth2 Access Token via gcloud ADC...")
    try:
        result = subprocess.run(
            ["gcloud", "auth", "application-default", "print-access-token"],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()
        if not token:
            raise ValueError("Token output is empty.")
        return token
    except Exception as e:
        print(f"Error fetching access token: {e}")
        print("Please run: gcloud auth application-default login")
        sys.exit(1)

async def run_mcp_test(year: int):
    # Fetch OAuth2 Access Token
    token = get_gcloud_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Connecting to Cloud Run SSE endpoint: {SERVICE_URL}/sse...")
    try:
        async with sse_client(f"{SERVICE_URL}/sse", headers=headers) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                print("Initializing session...")
                await session.initialize()
                
                print(f"Calling tool 'get_factors_by_year' for year {year}...")
                result = await session.call_tool("get_factors_by_year", {"year": year})
                
                print("\n--- Deployed Cloud Run Response ---")
                if result.isError:
                    print(f"Error executing tool: {result.content}")
                else:
                    print(result.content[0].text)
                print("-----------------------------------")
                
    except Exception as e:
        print(f"Connection or execution error: {e}")

if __name__ == "__main__":
    target_year = 2021
    if len(sys.argv) > 1:
        try:
            target_year = int(sys.argv[1])
        except ValueError:
            print("Usage: python test.py [year_integer]")
            sys.exit(1)
            
    asyncio.run(run_mcp_test(target_year))
