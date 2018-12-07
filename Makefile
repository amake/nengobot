SHELL := /bin/bash -O extglob

# Assets

work vendor dist:
	mkdir -p $(@)

BLANK_IMAGE := work/blank.png

$(BLANK_IMAGE): img/after-heisei.svg | work
	inkscape --export-png=$(@) --export-dpi 350 $(<)

FONT_ZIP := UtsukushiMincho-FONT.zip
FONT_OTF := work/UtsukushiMincho-FONT/UtsukushiFONT.otf

$(FONT_OTF): vendor/$(FONT_ZIP) | work
	cd work; unar $(PWD)/$(<)
	touch $(@)

vendor/$(FONT_ZIP): | vendor
	cd $(@D); curl -O http://flop.sakura.ne.jp/font/fontdata/$(FONT_ZIP)

.PHONY: font
font: $(FONT_OTF)

.PHONY: assets
assets: $(BLANK_IMAGE) $(FONT_OTF)

.PHONY: clean
clean:
	rm -rf work dist

# Dev

ENV_DEV := .env_dev

$(ENV_DEV):
	virtualenv $(@)
	$(@)/bin/pip install -e .

ENV_RELEASE := .env_release

.PHONY: test
test: | $(ENV_DEV)
	$(ENV_DEV)/bin/python nengo.py
	$(ENV_DEV)/bin/python announce.py 試験

# Lambda

AWS_ARGS ?=
LAMBDA_NAME := NengoBotTwitterBot
PAYLOAD := dist/lambda-deploy.zip

$(ENV_RELEASE):
	docker run -v $(PWD):/work --rm \
		lambci/lambda:build-python3.6 \
		/bin/sh -c "cd /work; virtualenv $(@); \
		$(@)/bin/pip install -e ."

.PHONY: zip
zip: $(PAYLOAD)

$(PAYLOAD): *.py credentials.json *.tsv $(BLANK_IMAGE) $(FONT_OTF) | $(ENV_RELEASE) dist
	rm -rf $(@)
	zip $(@) $(^) -x \*.pyc
	cd $(ENV_RELEASE)/lib/python3.*/site-packages; \
		zip -r $(PWD)/$(@) ./!(pip*|wheel*|setuptools*|easy_install*) -x \*.pyc

credentials.json:
	$(info Run python ./auth_setup.py to generate credentials)
	$(error $(@) not found)

.PHONY: deploy
deploy: $(PAYLOAD)
	aws $(AWS_ARGS) lambda update-function-code \
		--function-name $(LAMBDA_NAME) \
		--zip-file fileb://$$(pwd)/$(<)

.PHONY: invoke
invoke:
	aws $(AWS_ARGS) lambda invoke \
		--function-name $(LAMBDA_NAME) \
		/dev/null
