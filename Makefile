
# Makefile for IPython notebooks

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir = $(shell dirname $(mkfile_path))

CONDA_ENV_NAME=notebooks

default:
	@echo "Jupyter notebooks"

install:
	# pip install virtualenvwrapper
	# mkvirtualenv <name>
	bash ./install.sh
	# conda env cre

conda-env-create:
	conda env create -n "${CONDA_ENV_NAME}" -f='./environment.yml'

conda-env-update:
	conda env update -n "${CONDA_ENV_NAME}" -f='./environment.yml'

nb:
	jupyter notebook --secure --ip=127.0.0.1 --notebook-dir=.

test: test-all

test-all:
	find $(mkfile_dir) -name '*.ipynb' -exec runipy {} \;

run-all:
	find $(mkfile_dir) -name '*.ipynb' -exec runipy -o {} \;

html-index:
	python ./makeindex.py \
		--html \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./index.html

readme-index:
	python ./makeindex.py \
		--readme \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./README.md

index: html-index readme-index

html-all:
	find . -name '*.ipynb' -print0 | while read -d $$'\0' file; \
	do \
		if [ ! -z `echo $$file | grep -v '.ipynb_checkpoints/'` ]; \
			cd $(mkfile_dir)/`dirname "$$file"`; \
			ipython nbconvert "`basename $$file`" --to html; \
			htmlfile=`echo "$$file" | sed 's/.ipynb$$/.html/g'` ; \
		fi \
	done;
	$(MAKE) html-index
	$(MAKE) readme-index



clean-html:
	rm index.html
	find $(mkfile_dir) -name '*.html' -print0 | xargs -0 rm -fv

clean: clean-html


