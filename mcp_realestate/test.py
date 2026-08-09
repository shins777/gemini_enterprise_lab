import asyncio
import sys
import os
from mcp import ClientSession
from mcp.client.sse import sse_client

# Default to local server for local verification, can override with argument
DEFAULT_URL = "http://localhost:8080"

async def run_mcp_test(url: str, year: int):
    # If using cloud run, warn about auth requirements
    headers = {}
    if "a.run.app" in url:
        print("[Note] Testing on Cloud Run. Make sure you have authorized access.")
        # If they have a token available in environment, use it
        token = os.getenv("GCP_ID_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        else:
            print("To authenticate CLI requests on domain-restricted Cloud Run endpoints,")
            print("please export your OIDC identity token as GCP_ID_TOKEN:")
            print("  $ export GCP_ID_TOKEN=$(gcloud auth print-identity-token)")
            print("Running request without auth header...")

    sse_endpoint = f"{url.rstrip('/')}/sse"
    print(f"Connecting to SSE endpoint: {sse_endpoint}...")
    try:
        async with sse_client(sse_endpoint, headers=headers) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                print("Initializing session...")
                await session.initialize()
                
                print(f"Calling tool 'get_factors_by_year' for year {year}...")
                result = await session.call_tool("get_factors_by_year", {"year": year})
                
                print("\n--- Tool Response ---")
                if result.isError:
                    print(f"Error: {result.content}")
                else:
                    print(result.content[0].text)
                print("---------------------")
                
    except Exception as e:
        print(f"Connection or execution error: {e}")
        if "403" in str(e) or "Forbidden" in str(e):
            print("\n[Auth Warning] Received 403 Forbidden.")
            print("Because the Cloud Run service is restricted to the workspace domain,")
            print("please verify the service by linking it to your Gemini Enterprise App")
            print("and testing it directly in the Assistant Chat Preview panel!")

if __name__ == "__main__":
    target_year = 2021
    target_url = DEFAULT_URL
    
    if len(sys.argv) > 1:
        # Check if first arg is URL or year
        arg = sys.argv[1]
        if arg.startswith("http"):
            target_url = arg
            if len(sys.argv) > 2:
                try:
                    target_year = int(sys.argv[2])
                except ValueError:
                    pass
        else:
            try:
                target_year = int(arg)
            except ValueError:
                print("Usage: python test.py [url] [year]")
                sys.exit(1)
                
    asyncio.run(run_mcp_test(target_url, target_year))
