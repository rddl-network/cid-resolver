#################################################
### Docker Build for Develop & Release ##########
#################################################
# We create release and Develop based on Major
# and Minor version Numbers
# example: Major Version 1.0,1.1,1.2...
# example: Minor Version 1.0.1,1.1.0,1.2.0......
#################################################

K8S_TAG ?= latest
K8S_DOCKER_IMAGE_REGISTRY ?= index.docker.io
BUILD_DOCKER_IMAGE ?= $(K8S_DOCKER_IMAGE_REGISTRY)/riddleandcode/cid-resolver:$(K8S_TAG)

.PHONY: docker-rel-k8s
docker-rel-k8s:
	docker build --no-cache -t $(BUILD_DOCKER_IMAGE) \
		-f ./../../Dockerfile ./../../
