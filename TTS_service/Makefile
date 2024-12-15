VERSION=v1
PROJECT_ID=dcsc2024-437804
IMAGE_NAME=gcr.io/$(PROJECT_ID)/tts-service-image

build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f Dockerfile .

push:
	docker push $(IMAGE_NAME):$(VERSION)
	docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):latest
