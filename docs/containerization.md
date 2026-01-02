# Containerization

## Purpose and Scope
This document describes how to containerize the server and run it in docker <br>
It explains how the backend application is packaged into Docker image.

The goals of the containerization are:
- Consistent runtime environments across development and deployment
- Efficient image builds and reproducibility
- Seamless integration with the CI/CD pipeline and Kubernetes

## Repository Structure
The repository is organized as follows:
```
.
├─ client/
│  └─ ...
├─ docs/
│  └─ containerization.md
└─ server/
   └─ DockerFile
```
## Create Docker Image

### Dockerfile
>Docker is a software platform designed to build, test, and deploy applications quickly by packaging software into standardized units called containers. These containers include everything an application needs to run, such as libraries, system tools, and code, ensuring consistent performance across any environment.

Dockerfile is used to describe how a container will be build. The one inside the server folder will:
1. Get the latest Ubuntu image from Docker Hub.
2. Set the working directory to /app
3. Install python3 and pip
4. Copy the server folder to app/server
5. Install the required libraries
6. Expose the port 8080
7. Set the environment variables that the server needs to run
8. Start command

### Create image command
To create the docker image run the following command in the terminal:
```
docker build -t server:develop -f server/DockerFile .
```
List all images to ensure that the image was created
```
docker image ls
```
Running the image happens with the command:
```
docker run -p 8080:8080 server:develop
```
