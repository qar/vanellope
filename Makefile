include ./Makefile.variable

build:
	docker build . -t $(IMAGE):$(VERSION)

push:
	docker push $(IMAGE):$(VERSION)

build_dev:
	docker build . -t $(DEV_IMAGE) -f ./DockerfileDev

run_dev: build_dev
	mkdir -p $(DEV_DATA_DIR)
	docker run --rm -v $(DEV_DATA_DIR):/vanellope_content -v $(shell pwd):/src -p $(DEV_PORT):80 --name $(DEV_IMAGE) $(DEV_IMAGE)
