---
name: build-mcp-server
description: >-
    Gemini Enterprise MCP 서버를 Cloud run 환경에서 구축해서 Streamable HTTP MCP 서버를 실행하게 하는것이 최종 목적입니다. 
version: 1.0.0
--

# MCP 서버 구축 및 커스텀 배포/인프라 관리 도구 실행 Hands-on Lab 가이드

최종목표는 .env 파일에 제시된 프로젝트에 대한 MCP 서버를 구축하고, 해당 정보를 Gemini Enterprise MCP 서버에 등록하여, Gemini Enterprise에서 도구를 통해서 실행하는 것입니다.
MCP 서버는 Cloud run 환경에서 구동됩니다. 

1. Configuration 정보.
  - 참고하는 환경파일 : `src/.env` 
  
2. 실제 실행하는 shell 은 아래 디렉토리의 deploy.sh 를 실행합니다.
  - `src/mcp/mcp_realestate/deploy.sh`