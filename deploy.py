import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")

# Configuration
PROJECT_DIR = os.getenv("PROJECT_DIR", ".") 
DOCKER_USERNAME = os.getenv("DOCKER_USERNAME", "zyetta")  
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")
DOCKER_TAG = os.getenv("DOCKER_TAG", "latest")  
DOCKER_IMAGE = f"{DOCKER_USERNAME}/salt-master:{DOCKER_TAG}"

# Helper to run shell commands
def run(command, cwd=None):
    print(f"\n$ {command}")
    result = subprocess.run(command, shell=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        sys.exit(1)

# Step 1: Pull latest changes and submodules
def update_repo():
    if not os.path.exists(PROJECT_DIR):
        print(f"Error: Project dir {PROJECT_DIR} does not exist")
        sys.exit(1)
    # Pull main repo
    run("git pull", cwd=PROJECT_DIR)
    # Ensure submodules are initialized and at the commit specified in main repo
    run("git submodule update --init --recursive", cwd=PROJECT_DIR)
    
# Step 2: Docker login
def docker_login():
    print("\nLogging into Docker Hub...")
    run(f"echo {DOCKER_PASSWORD} | docker login -u {DOCKER_USERNAME} --password-stdin")

# Step 3: Build Docker image
def build_image():
    print(f"\nBuilding Docker image: {DOCKER_IMAGE}...")
    run(f"docker build -t {DOCKER_IMAGE} .", cwd=PROJECT_DIR)

# Step 4: Push Docker image
def push_image():
    print(f"\nPushing Docker image: {DOCKER_IMAGE}...")
    run(f"docker push {DOCKER_IMAGE}")

# Main pipeline
if __name__ == "__main__":
    update_repo()
    docker_login()
    build_image()
    push_image()
    print("\nDeployment complete!")