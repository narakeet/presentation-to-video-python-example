DOCKER_IMAGE := python:3.7
run:
	@[[ ! -z "$(NARAKEET_API_KEY)" ]] || (echo "NARAKEET_API_KEY not set" && exit 1)
	@[[ ! -z "$(PPTX_FILE)" ]] || (echo "PPTX_FILE not set" && exit 1)
	docker run -it --rm -eNARAKEET_API_KEY=$(NARAKEET_API_KEY) -ePPTX_FILE=$(PPTX_FILE) -v $(shell pwd):/data -v /tmp:/tmp -w /data --entrypoint /bin/bash $(DOCKER_IMAGE) -c "pip install -r requirements.txt && python main.py"
