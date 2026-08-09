# Google Maps MCP Server

An Model Context Protocol (MCP) server providing Google Maps search and distance calculation tools, designed for deployment on Google Cloud Run and registration in Agent Platform / Agent Registry.

## Included Tools

1. `search_location`: Search for places, addresses, or points of interest using Google Maps Places API and Geocoding API.
2. `calculate_distance`: Calculate travel distance (meters) and travel time (seconds) between origin and destination using Google Maps Distance Matrix API.

---

## Files

- `server.py`: Python MCP server implementation using FastMCP with SSE transport.
- `requirements.txt`: Required Python dependencies.
- `Dockerfile`: Container image specification for Cloud Run deployment.
- `deploy.sh`: One-command build & deployment script for Cloud Run.
- `mcp_config.json`: Connection and tool configuration file for MCP clients and Agent Platform.

---

## Local Setup & Testing

1. Set your Google Maps API Key:
   ```bash
   export GOOGLE_MAPS_API_KEY="your_api_key_here"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run locally:
   ```bash
   python server.py
   ```
   The server will start on `http://0.0.0.0:8080/sse`.

---

## Deployment to Cloud Run

Run the automated deployment script:

```bash
export GOOGLE_MAPS_API_KEY="your_api_key_here"
export REGION="asia-northeast1" # or your target region
./deploy.sh
```

Or deploy manually via `gcloud`:

```bash
gcloud run deploy google-maps-mcp \
  --source . \
  --region us-central1 \
  --no-allow-unauthenticated \
  --set-env-vars GOOGLE_MAPS_API_KEY="your_api_key_here" \
  --port 8080
```

After deployment, Cloud Run will output your SSE Endpoint URL:
`https://<service-name>-<hash>-<region>.a.run.app/sse`

---

## Agent Platform / Agent Registry Registration

To register this MCP server in Agent Platform Agent Registry:

1. Copy your deployed Cloud Run SSE Endpoint URL (`https://<service-name>-<hash>-<region>.a.run.app/sse`).
2. Update `mcp_config.json` with your Cloud Run SSE URL.
3. In Agent Platform Console / Gemini Enterprise Admin:
   - Navigate to **Agent Registry** -> **MCP Server Registration**.
   - Click **Add Custom MCP Server**.
   - Select **Transport**: `SSE (Server-Sent Events)`.
   - Set **Server URL**: `https://<service-name>-<hash>-<region>.a.run.app/sse`.
   - Set **Authentication**: Select Unauthenticated or GCP IAM OIDC token depending on your security policy.
