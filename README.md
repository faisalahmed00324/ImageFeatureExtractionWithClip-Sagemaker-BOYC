# CLIP Image & Text Embedding API

A proof of concept demonstrating how to serve **OpenAI CLIP** using a custom Docker inference container and deploy it as an endpoint on **Amazon SageMaker**.

The application exposes a lightweight FastAPI service that generates image and text embeddings using the `openai/clip-vit-base-patch32` model.

## Architecture

```text
                 Client Application
                        |
                        v
                   FastAPI API
                        |
             +----------+----------+
             |                     |
             v                     v
        Image Input             Text Input
        (Base64)                (Text)
             |                     |
             v                     v
          CLIP Model (ViT-B/32)
             |                     |
             v                     v
       Image Embedding       Text Embedding
             |                     |
             +----------+----------+
                        |
                        v
               L2 Normalization
                        |
                        v
                 JSON Response
```

### Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| AI Model | OpenAI CLIP |
| Deep Learning | PyTorch |
| Model Integration | Hugging Face Transformers |
| API Framework | FastAPI |
| Containerization | Docker |
| Cloud Deployment | Amazon SageMaker |
| Deployment Automation | Jupyter Notebook, Boto3, SageMaker SDK |

## Features

- **Image Embeddings:** Generate feature vectors from images using CLIP.
- **Text Embeddings:** Generate feature vectors from text descriptions.
- **Normalized Vectors:** Apply L2 normalization to embedding outputs.
- **REST API:** Expose model inference through FastAPI.
- **Custom Docker Container:** Package the model and inference application into a deployable container.
- **SageMaker Integration:** Deploy the custom inference container to a SageMaker endpoint.
- **Autoscaling:** Configure endpoint scaling using SageMaker Application Auto Scaling.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/ping` | Health check |
| POST | `/invocations` | Generate an image embedding |
| POST | `/text-embedding` | Generate a text embedding |

### Image Embedding

Endpoint: `POST /invocations`

Request:

```json
{
  "image": "<base64-encoded-image>"
}
```

Response:

```json
{
  "embedding": [0.0123, -0.0456, 0.0789]
}
```

### Text Embedding

Endpoint: `POST /text-embedding`

Request:

```json
{
  "text": "A dog running on a beach"
}
```

Response:

```json
{
  "embedding": [0.0123, -0.0456, 0.0789]
}
```

*Embedding values above are illustrative.*

## Project Structure

```text
ImageFeatureExtractionWithClip-Sagemaker-BOYC/
├── endpoint.py       # FastAPI inference application
├── Dockerfile        # Custom inference container
├── requirements.txt  # Python dependencies
├── deploy.ipynb      # SageMaker deployment and autoscaling
├── README.md
└── LICENSE
```

## Running Locally with Docker

### Prerequisites

- Docker
- Access to download the CLIP model during image construction

### 1. Build the Docker image

Run from the repository root:

```bash
docker build -t clip-inference-api .
```

The Dockerfile downloads the CLIP model and stores its files inside the container.

### 2. Start the API

```bash
docker run --rm -p 8080:8080 clip-inference-api serve
```

The API will be available at:

```text
http://localhost:8080
```

FastAPI interactive documentation:

```text
http://localhost:8080/docs
```

Health check:

```text
http://localhost:8080/ping
```

## Deploying to Amazon SageMaker

This project uses a custom inference container (Bring Your Own Container) for SageMaker deployment.

The `deploy.ipynb` notebook demonstrates the deployment workflow:

1. Initialize a SageMaker session.
2. Retrieve the SageMaker execution role.
3. Configure the container image URI from Amazon ECR.
4. Create a SageMaker model using the custom container.
5. Deploy the model to a SageMaker endpoint.
6. Configure endpoint autoscaling.

### Deployment Configuration

The notebook includes an example configuration:

- Initial instance count: 1
- Example instance type: `ml.m5.large`
- Minimum autoscaling capacity: 1
- Maximum autoscaling capacity: 3
- Target tracking metric: SageMaker variant invocations per instance

Before running the notebook, replace the placeholder ECR image URI with your actual image URI and ensure the SageMaker execution role has the necessary permissions.

**Note:** The deployed SageMaker inference interface currently uses `/invocations` for image requests. The separate `/text-embedding` route is available in the FastAPI application, but the SageMaker invocation handler would need to be extended to support text requests through the standard endpoint interface.

## Current Scope and Limitations

This repository is a technical proof of concept.

- Uses the pretrained CLIP ViT-B/32 model.
- Uses a custom Docker inference container.
- Does not include a persistent vector database or similarity-search engine.
- Does not include a frontend application.
- Does not implement authentication or production API security.
- The deployment notebook contains configuration placeholders that must be completed before deployment.

## Potential Improvements

- Integrate FAISS or another vector database for similarity search.
- Support both image and text requests through the SageMaker inference interface.
- Add request validation and improved error handling.
- Add automated tests for inference endpoints.
- Explore GPU-based inference and performance optimization.
- Add monitoring and structured logging.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
