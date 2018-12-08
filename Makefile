SHELL := /bin/bash -O extglob

# Assets

work vendor dist:
	mkdir -p $(@)

BLANK_IMAGE := work/blank.png

$(BLANK_IMAGE): img/after-heisei.svg | work
	inkscape --export-png=$(@) --export-dpi 350 $(<)

FONT_ZIP := vendor/UtsukushiMincho-FONT.zip
FONT_OTF := work/UtsukushiMincho-FONT/UtsukushiFONT.otf

$(FONT_OTF): $(FONT_ZIP) | work
	cd work; unar $(PWD)/$(<)
	touch $(@)

$(FONT_ZIP): | vendor
	cd $(@D); curl -O http://flop.sakura.ne.jp/font/fontdata/$(@F)

.PHONY: font
font: $(FONT_OTF)

EMOJI_DIR := work/images/160x160
EMOJI_EXTRACTOR := vendor/emoji_extractor.rb

$(EMOJI_DIR): $(EMOJI_EXTRACTOR) | work
	cd work; ruby $(PWD)/$(<)

$(EMOJI_EXTRACTOR): | vendor
	cd $(@D); curl -O https://raw.githubusercontent.com/tmm1/emoji-extractor/2ceed50ccc65e1da29511314cbf0535bd60a7552/$(@F)

ASSETS := $(BLANK_IMAGE) $(FONT_OTF) $(EMOJI_DIR)

.PHONY: assets
assets: $(ASSETS)

.PHONY: clean
clean:
	rm -rf work dist

# Dev

ENV_DEV := .env_dev

$(ENV_DEV):
	virtualenv $(@)
	$(@)/bin/pip install -e .
	$(@)/bin/pip install boto3

ENV_RELEASE := .env_release

.PHONY: test
test: | $(ENV_DEV) $(ASSETS)
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

DRY_RUN := --dryrun

.PHONY: deploy-emoji
deploy-emoji: $(EMOJI_DIR)
	aws $(AWS_ARGS) s3 sync $(DRY_RUN) $(<) s3://nengobot/$(<F)
