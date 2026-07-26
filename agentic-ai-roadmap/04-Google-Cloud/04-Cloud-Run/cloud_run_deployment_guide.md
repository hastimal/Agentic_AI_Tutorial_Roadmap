# 🚀 Using Antigravity, Gemini LLM and ADK Social Agent for Agentic AI to Google Cloud Run

This guide outlines step-by-step instructions on how to build the Docker container image and deploy the **FastAPI backend + static UI dashboard** of the `social_agent` to **Google Cloud Run**.

---

## 🏗️ Project Architecture

* **FastAPI Server (`main.py`)**: Exposes API routes (`/api/trends` for emerging tech trends and `/api/generate` for copywriter generation) and hosts static files (`/static/index.html`).
* **Static Dashboard (`static/`)**: A sleek dark glassmorphic user interface allowing users to select trends, configure parameters, and fetch generated copies.
* **Google ADK Agent**: Loaded natively from the `social_agent` package, integrating custom copywriting instructions and tool calling interfaces.

---

## 💻 Step 1: Verify Locally Prior to Deployment

Before pushing to the cloud, run the container locally to ensure there are no configuration errors.

### 1. Build the Docker Image
```bash
docker build -t social-agent-app .
```

### 2. Run the Container locally
Pass your local API key to test:
```bash
docker run -p 8080:8080 \
  -e GEMINI_API_KEY="your_google_ai_studio_api_key" \
  social-agent-app
```

Navigate to `http://localhost:8080/static/index.html` in your web browser. Select a trend, enter keywords, and click **Generate** to verify execution.

---

## 🚀 Step 2: Deploy to Google Cloud Run

Deploy your container serverless-ly using **Google Cloud Build** and **Artifact Registry**.

### 1. Set Environment Variables
```bash
export PROJECT_ID="gcp-10-project"
export REGION="us-central1"
export REPO_NAME="antigravity-repo"
export IMAGE_NAME="social-agent-api"

# Configure defaults for gcloud CLI
gcloud config set project $PROJECT_ID
```

### 2. Create Artifact Registry Repository
Create a Docker registry repository:
```bash
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Antigravity Artifact Repository"
```

### 3. Build & Push Image using Cloud Build
Compile and upload your container image automatically to Artifact Registry:
```bash
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest .
```

---

## 🔒 Step 3: Choose Authentication Mechanism

Choose **one** of the following options to allow your deployed Cloud Run service to authenticate and query Gemini:

### Option A: Use Gemini API Key via Secret Manager (Recommended for AI Studio users)
1. **Store your API Key as a Secret**:
   ```bash
   echo -n "AQ.Ab8RN6JwGF46nAFae5kSJ8upX9RgkZpei0MlNkpxn2dxr7LriQ" | gcloud secrets create GEMINI_API_KEY \
       --data-file=- \
       --replication-policy="automatic"
   ```
2. **Grant Secret Accessor role to the default Compute Engine Service Account**:
   ```bash
   export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
   
   gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
       --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
       --role="roles/secretmanager.secretAccessor"
   ```
3. **Deploy to Cloud Run with Secret**:
   ```bash
    gcloud run deploy social-agent-service \
        --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest \
        --region=$REGION \
        --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest" \
        --memory=1Gi \
        --allow-unauthenticated
    ```

---

### Option B: Use Vertex AI IAM Authentication (Recommended for enterprise / Google Cloud native users)
If you enabled Vertex AI on your project, you can authorize predictions without managing secrets by granting Vertex prediction permissions:

1. **Assign Vertex AI User role to the default Service Account**:
   ```bash
   export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
       --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
       --role="roles/aiplatform.user"
   ```
2. **Deploy to Cloud Run telling the SDK to use Vertex AI**:
   ```bash
    gcloud run deploy social-agent-service \
        --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest \
        --region=$REGION \
        --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
        --memory=1Gi \
        --allow-unauthenticated
    ```

---

## 🌐 Step 4: Verify Your Deployed Application

Once the deployment completes, the CLI outputs your Service URL (e.g., `https://social-agent-service-xxxxxx.a.run.app`).

1. Open your browser and navigate to the root URL (it will automatically redirect you to the dashboard):
   `https://social-agent-service-xxxxxx.a.run.app/`
2. Test by selecting a tech trend and triggering a strategy run!
