#!/usr/bin/env bash
set -e

SERVICE_NAME="${SERVICE_NAME:-korea-realestate-mcp}"
REGION="${REGION:-us-central1}"
if [ -z "$CLOUDSDK_AUTH_ACCESS_TOKEN" ]; then
  export CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || echo "")"
fi

if [ -z "$PROJECT_ID" ]; then
  echo "Error: GCP Project ID is not set. Run 'gcloud config set project YOUR_PROJECT_ID' or set PROJECT_ID environment variable."
  exit 1
fi

echo "============================================================"
echo " Deploying $SERVICE_NAME to GCP Cloud Run"
echo " Project ID : $PROJECT_ID"
echo " Region     : $REGION"
echo "============================================================"

# Deploy to Cloud Run using source build
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080

# Retrieve deployed Service URL
SERVICE_URL="$(gcloud run services describe "$SERVICE_NAME" --project "$PROJECT_ID" --region "$REGION" --format 'value(status.url)')"
HTTP_URL="${SERVICE_URL}/mcp"

echo "============================================================"
echo " Deployment Complete!"
echo " Service URL : $SERVICE_URL"
echo " HTTP Endpoint: $HTTP_URL"
echo "============================================================"
echo "Use $HTTP_URL in your Agent Platform / MCP Client config."
