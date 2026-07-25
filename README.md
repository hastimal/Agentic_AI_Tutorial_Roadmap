# Antigravity Agentic API: Cloud Run Deployment Guide

This project is a containerized FastAPI application implementing an AI Agent using the **Google Antigravity SDK (ADK)** and Gemini LLMs. It is designed to be easily run locally and deployed to **Google Cloud Run** for high-availability, auto-scaling, and serverless hosting.

---

## 🏗️ Project Architecture

- **FastAPI Web Server (`main.py`)**: Exposes REST endpoints (`/chat` for agent turns and `/health` for status/liveness probes).
- **Google Antigravity Agent**: Integrates system instructions and executes custom Python tools.
- **Custom Tools (`tools.py`)**: System actions (`get_current_time` and `fetch_mock_system_status`) accessible by the agent.
- **Dockerized Container (`Dockerfile`)**: Packages dependencies, vendored Antigravity SDK, and source files into a lightweight, non-root execution environment.

---

## ⚡ Local Development

### 1. Setup Environment
First, ensure you are using Python 3.11+ and create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Credentials
Create a `.env` file in the root of `Jangid-project`:
```env
GEMINI_API_KEY="your_google_ai_studio_api_key"
MODEL="gemini-3.5-flash"
PORT=8080
```
> Obtain a Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/api-keys).

### 3. Run FastAPI Locally
```bash
python3 main.py
```
Or run with live reload:
```bash
python3 -m uvicorn main:app --reload --port 8080
```

### 4. Test the API Endpoints
Verify health check:
```bash
curl http://127.0.0.1:8080/health
```

Query the agent requesting a tool usage:
```bash
curl -X POST "http://127.0.0.1:8080/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Check the mock system status for the database service"}'
```

---

## 🐳 Docker Containerization

To verify that the application containerizes successfully prior to cloud deployment:

### 1. Build the Docker Image
```bash
docker build -t antigravity-agent-app .
```

### 2. Run the Container Locally
Pass your local environment variables into the container:
```bash
docker run -p 8080:8080 \
  -e GEMINI_API_KEY="your_google_ai_studio_api_key" \
  antigravity-agent-app
```
Test using the same `curl` commands shown above.

---

## 🚀 Deploying to Google Cloud Run

To host the API on Google Cloud Run, follow these steps.

### Prerequisites
- Install the [Google Cloud SDK (gcloud CLI)](https://cloud.google.com/sdk/docs/install).
- Initialize your configuration:
  ```bash
  gcloud init
  ```
- Authenticate Docker to push images to Google Cloud:
  ```bash
  gcloud auth configure-docker
  ```

---

### Step 1: Configure GCP Environment
Define environment variables to streamline the commands:
```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export REPO_NAME="antigravity-repo"
export IMAGE_NAME="agent-api"

# Set default project
gcloud config set project $PROJECT_ID
```

### Step 2: Enable Google Cloud Services
Enable Artifact Registry, Cloud Build, and Cloud Run APIs:
```bash
gcloud services enable \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    secretmanager.googleapis.com
```

### Step 3: Create Artifact Registry Repository
Create a Docker repository in Artifact Registry to store your container image:
```bash
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Antigravity Agent Docker Repository"
```

### Step 4: Build and Push Using Cloud Build
You can build and push the container to Artifact Registry in a single step using Google Cloud Build:
```bash
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest .
```

---

### Step 5: Cloud Run Authentication Setup
To query Gemini from Cloud Run, choose **one** of the two authentication methodologies:

#### Option A: Use Gemini API Key via Secret Manager (Recommended for AI Studio users)
1. **Create the Secret**:
   ```bash
   echo -n "your-gemini-api-key" | gcloud secrets create GEMINI_API_KEY \
       --data-file=- \
       --replication-policy="automatic"
   ```
2. **Grant Secret Access to default compute service account**:
   Get the project number:
   ```bash
   export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
   ```
   Grant Secret Manager Secret Accessor role:
   ```bash
   gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
       --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
       --role="roles/secretmanager.secretAccessor"
   ```

#### Option B: Use Vertex AI (Recommended for enterprise / Google Cloud Native users)
Assign the Vertex AI User role directly to your Cloud Run service account, allowing the SDK to authenticate automatically without managing API key secrets.
```bash
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

---

### Step 6: Deploy to Cloud Run

#### Deployment command for Option A (using Secret Manager):
```bash
gcloud run deploy agent-service \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest \
    --region=$REGION \
    --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest" \
    --allow-unauthenticated
```

#### Deployment command for Option B (using Vertex AI service-to-service auth):
```bash
gcloud run deploy agent-service \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest \
    --region=$REGION \
    --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
    --allow-unauthenticated
```

Once deployment completes, the CLI outputs a service URL (e.g., `https://agent-service-xxxxxx.a.run.app`).

---

### Step 7: Verify Cloud Run Deployment
Query the deployed Cloud Run service URL:
```bash
# Verify health
curl https://agent-service-xxxxxx.a.run.app/health

# Run an agentic chat turn
curl -X POST "https://agent-service-xxxxxx.a.run.app/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the current time and check the status of our cache database service?"}'
```
