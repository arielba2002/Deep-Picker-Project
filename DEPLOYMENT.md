# Deep Picker Project - OpenShift Deployment Guide

This guide explains how to deploy the Deep Picker project to OpenShift with proper service communication and network policies.

## Architecture Overview

The project consists of three main components:

1. **Frontend (React/Vite)**: Serves the user interface and proxies API calls to the backend
2. **Backend (FastAPI)**: Provides REST API endpoints and handles business logic
3. **Database (PostgreSQL)**: Stores application data

## Network Security

The deployment includes network policies that ensure:
- **Frontend**: Externally accessible via LoadBalancer/Route
- **Backend**: Only accessible from frontend and within the namespace (ClusterIP)
- **Database**: Only accessible from backend pods (ClusterIP + NetworkPolicy)

## Prerequisites

1. OpenShift cluster access
2. Docker/Podman for building images
3. `oc` CLI tool installed and configured

## Deployment Steps

### 1. Build and Push Docker Images

First, login to Quay.io registry:

```bash
# Login to Quay.io
docker login -u='rhl193000+hafifa' -p='UHOXMLP8T7X4NGGJER7YIOHY2IBIWNV96ZY6NYIKRTTJ2Z3LDAK0NK2RBXTC5G0Z' quay.io
```

Then build and push the Docker images:

```bash
# Make the build script executable
chmod +x build-and-push.sh

# Build and push images (replace 'latest' with your desired tag)
./build-and-push.sh latest
```

**Note**: The build script is configured to push to Quay.io registry (`quay.io/rhl193000/`). Make sure you're logged in to Quay.io before running the script.

### 2. Deploy to OpenShift

#### Option A: Using the comprehensive deployment file (Recommended)

```bash
# Deploy all components with network policies
oc apply -f openshift-deployment.yaml
```

This creates:
- A dedicated namespace (`deep-picker`)
- Network policies for secure communication
- All application components with proper resource limits
- OpenShift Route for external access

#### Option B: Using the existing all-in-one.yaml

```bash
# Deploy using existing configuration
oc apply -f all-in-one.yaml
```

### 3. Verify Deployment

Check that all pods are running:

```bash
# Check pod status
oc get pods -n deep-picker

# Check services
oc get services -n deep-picker

# Check routes (for external access)
oc get routes -n deep-picker
```

### 4. Access the Application

- **Frontend**: Access via the Route URL or LoadBalancer IP
- **Backend**: Internal access only (http://backend:8888)
- **Database**: Internal access only (db:5432)

## Configuration Changes Made

### Backend Changes

1. **Environment Variables**: Updated to use `os.getenv()` for configuration
2. **Host Binding**: Changed from `localhost` to `0.0.0.0`
3. **CORS Policy**: Updated to allow all origins for container deployment
4. **Health Endpoint**: Added `/health` endpoint for probes

### Frontend Changes

1. **API Calls**: Updated all API calls to use relative URLs (`/api/...`)
2. **Nginx Proxy**: Added nginx configuration to proxy API calls to backend
3. **Build Process**: Multi-stage Docker build with nginx serving

### Network Policies

1. **Namespace Isolation**: All components in dedicated namespace
2. **Frontend Access**: Allows external traffic
3. **Backend Protection**: Only accessible from frontend
4. **Database Security**: Only accessible from backend

## Monitoring and Troubleshooting

### Check Pod Logs

```bash
# Backend logs
oc logs -f deployment/backend -n deep-picker

# Frontend logs
oc logs -f deployment/frontend -n deep-picker

# Database logs
oc logs -f deployment/db -n deep-picker
```

### Check Service Endpoints

```bash
# List all endpoints
oc get endpoints -n deep-picker

# Check network policies
oc get networkpolicies -n deep-picker
```

### Common Issues

1. **Backend can't connect to database**: Check if database pod is ready
2. **Frontend can't reach backend**: Verify nginx proxy configuration
3. **External access issues**: Check Route/LoadBalancer configuration

## Scaling

To scale the application:

```bash
# Scale backend
oc scale deployment/backend --replicas=3 -n deep-picker

# Scale frontend
oc scale deployment/frontend --replicas=3 -n deep-picker
```

## Security Considerations

1. **Database Credentials**: Stored in Kubernetes secrets
2. **Network Isolation**: Enforced via NetworkPolicies
3. **TLS Termination**: Handled at Route level
4. **Resource Limits**: Applied to prevent resource exhaustion

## File Structure

```
.
├── app/
│   ├── backend/
│   │   ├── Dockerfile          # Backend container image
│   │   └── ...                 # Backend source code
│   └── frontend/
│       ├── Dockerfile          # Frontend container image
│       ├── nginx.conf          # Nginx proxy configuration
│       └── ...                 # Frontend source code
├── all-in-one.yaml            # Original deployment file (updated)
├── openshift-deployment.yaml  # Comprehensive deployment with network policies
├── build-and-push.sh          # Build script for Docker images
└── DEPLOYMENT.md              # This file
```

## Next Steps

1. Set up monitoring with Prometheus/Grafana
2. Configure log aggregation
3. Set up automated backups for the database
4. Implement CI/CD pipeline for automated deployments 