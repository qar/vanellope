include ./Makefile.variable

build:
	docker build . -t $(IMAGE):$(VERSION) -f ./Dockerfile

push:
	docker push $(IMAGE):$(VERSION)

build_dev:
	docker build . -t $(DEV_IMAGE) -f ./DockerfileDev

preview: build
	mkdir -p $(DEV_DATA_DIR)
	docker run \
		--rm\
		-v $(DEV_DATA_DIR):/vanellope_content\
		-p $(DEV_PORT):80\
		--name $(DEV_IMAGE)\
		$(IMAGE):$(VERSION)
	sleep 2
	$(shell open http://localhost:$(DEV_PORT))

run_dev: build_dev
	mkdir -p $(DEV_DATA_DIR)
	docker run\
		--rm\
		-v $(DEV_DATA_DIR):/vanellope_content\
		-v $(shell pwd):/src\
		-p $(DEV_PORT):80\
		--name $(DEV_IMAGE)\
		$(DEV_IMAGE)
	sleep 2
	$(shell open http://localhost:$(DEV_PORT))
