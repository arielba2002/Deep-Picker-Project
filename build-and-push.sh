#!/bin/bash

# Build and Push Script for Deep Picker Project
# This script builds and pushes Docker images for frontend, backend, and database to Quay.io

set -e

# Configuration
REGISTRY="quay.io"
USERNAME="rhl193000"
IMAGE_TAG="${1:-latest}"

echo "🚀 Building Deep Picker Docker Images"
echo "Registry: $REGISTRY"
echo "Username: $USERNAME"
echo "Tag: $IMAGE_TAG"
echo ""

# Login reminder
echo "⚠️  Make sure you're logged in to Quay.io:"
echo "docker login -u='rhl193000+hafifa' -p='UHOXMLP8T7X4NGGJER7YIOHY2IBIWNV96ZY6NYIKRTTJ2Z3LDAK0NK2RBXTC5G0Z' quay.io"
echo ""

# Function to build and push image
build_and_push() {
    local service=$1
    local dockerfile_path=$2
    local context_path=$3
    
    echo "📦 Building $service image..."
    docker build -t $REGISTRY/$USERNAME/$service:$IMAGE_TAG -f $dockerfile_path $context_path
    
    echo "⬆️  Pushing $service image..."
    docker push $REGISTRY/$USERNAME/$service:$IMAGE_TAG
    
    echo "✅ $service image built and pushed successfully!"
    echo ""
}

# Build Backend
echo "🔧 Building Backend Service..."
build_and_push "backend" "app/backend/Dockerfile" "app/backend"

# Build Frontend
echo "🎨 Building Frontend Service..."
build_and_push "frontend" "app/frontend/Dockerfile" "app/frontend"

# Build Database
echo "🗄️  Building Database Service..."
build_and_push "db" "app/database/Dockerfile" "app/database"

echo "🎉 All images built and pushed successfully to Quay.io!"
echo ""
echo "Images available at:"
echo "- $REGISTRY/$USERNAME/backend:$IMAGE_TAG"
echo "- $REGISTRY/$USERNAME/frontend:$IMAGE_TAG"
echo "- $REGISTRY/$USERNAME/db:$IMAGE_TAG"
echo ""
echo "To deploy to OpenShift, run:"
echo "oc apply -f openshift-deployment.yaml"
echo ""
echo "Or to use the simple deployment:"
echo "oc apply -f simple-deployment.yaml" 