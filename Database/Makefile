VERSION=v1
PROJECT_ID=dcsc2024-437804
IMAGE_NAME=metadata-service-image


build:
	docker build --no-cache -f Dockerfile -t gcr.io/$(PROJECT_ID)/$(IMAGE_NAME):$(VERSION) .

push:
	docker push gcr.io/$(PROJECT_ID)/$(IMAGE_NAME):$(VERSION)
	docker tag gcr.io/$(PROJECT_ID)/$(IMAGE_NAME):$(VERSION) gcr.io/$(PROJECT_ID)/$(IMAGE_NAME):latest
	docker push gcr.io/$(PROJECT_ID)/$(IMAGE_NAME):latest

