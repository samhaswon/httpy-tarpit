build-and-push:
	docker buildx build --push --platform linux/arm/v6,linux/arm/v7,linux/arm64/v8,linux/amd64,linux/386 --tag samhaswon/httpy-tarpit:latest .
build-only:
	docker buildx build --platform linux/arm/v6,linux/arm/v7,linux/arm64/v8,linux/amd64,linux/386 --tag samhaswon/httpy-tarpit:latest .
builder:
	docker buildx create --name httpy-builder --bootstrap --use