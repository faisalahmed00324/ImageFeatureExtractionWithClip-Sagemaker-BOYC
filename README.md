<img width="215" height="19" alt="image" src="https://github.com/user-attachments/assets/ed83f2c1-c1cf-4b2c-a264-1c52f5862c96" />ImageSearchWithClip-Sagemaker-BOYC
A lightweight Python API for serving Clip model, designed for easy deployment with sagemaker. This project includes a sample endpoint for inference and a Jupyter notebook for deployment automation.

Features
REST API for ML model inference (endpoint.py)
Dockerfile for containerized deployment
Jupyter notebook (deploy.ipynb) for deployment automation
Compatible with SageMaker
Getting Started
Prerequisites
Python 3.12+
Docker
Jupyter Notebook
The Jupyter Notebook was excuted from a sagemaker notebook instace
Installation
Clone the repository:
  'git clone https://github.com/faisalahmed00324/ImageSearchWithClip-Sagemaker-BOYC.git'
  'cd ImageSearchWithClip-Sagemaker-BOYC'

Install dependencies:
  'pip install -r requirements.txt'

Usage
Run Locally
  "python endpoint.py"
Build and Run with Docker
  "docker build -t clip-web-api ."
  "docker run -it clip-web-api serve"
Deploy with Jupyter Notebook on sagemaker
See deploy.ipynb for step-by-step deployment instructions.

Project Structure
License
This project is licensed under the MIT License.

Let me know if you want to customize any section or add more details!
