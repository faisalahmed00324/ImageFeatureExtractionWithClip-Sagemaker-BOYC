FROM python:3.9-slim

# Install system deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /opt/program/requirements.txt
RUN pip install --no-cache-dir -r /opt/program/requirements.txt

# Pre-download CLIP model into image
RUN python -c "from transformers import CLIPProcessor, CLIPModel; \
    CLIPModel.from_pretrained('openai/clip-vit-base-patch32').save_pretrained('/opt/program/model'); \
    CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32').save_pretrained('/opt/program/model')"

# Copy app
WORKDIR /opt/program
COPY endpoint.py /opt/program

# SageMaker expects inference server on port 8080
ENV PORT=8080
ENV HOST=0.0.0.0

# Start server
#CMD ["uvicorn", "endpoint:app", "--host", "0.0.0.0", "--port", "8080"]
# SageMaker expects `docker run <image> serve`
ENTRYPOINT ["python", "endpoint.py"]
CMD ["serve"]
