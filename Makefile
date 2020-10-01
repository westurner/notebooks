
# Makefile for IPython notebooks

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir = $(shell dirname $(mkfile_path))

CONDA_ENV_NAME:=notebooks
PYTHON_OPTS:=PYTHONNOUSERSITE=1
CONDA_OPTS=${PYTHON_OPTS}
conda=${CONDA_OPTS} conda

.PHONY: default install \
	conda-env-create conda-env-update conda-env-export \
	conda-env-stripversions \
	nb \
	test test-all \
	run-all \
	html-index readme-index \
	html-all py-all \
	clean-html \
	clean


default:
	@echo "Jupyter notebooks"

install:
	# pip install virtualenvwrapper
	# mkvirtualenv <name>
	bash ./install.sh
	# conda env cre

conda-env-create:
	${conda} env create -n "${CONDA_ENV_NAME}" -f='./environment.yml'

conda-env-update:
	${conda} env update -n "${CONDA_ENV_NAME}" -f='./environment.yml'

environment.yml: conda-env-export

conda-env-export:
	${conda} env export -n "${CONDA_ENV_NAME}" | \
		grep -Ev '^(name|prefix): ' | \
		tee './environment.versions.yml' | \
		tee './environment.yml'

conda-env-export-from-history:
	${conda} env export -n "${CONDA_ENV_NAME}" --from-history | \
		grep -Ev '^(name|prefix): ' | \
		tee './environment.fromhistory.yml'
	echo "# Note that pip packages and all conda channels (?) are not listed in this file" | \
		tee -a './environment.fromhistory.yml'


environment.noversions.yml: conda-env-stripversions

conda-env-stripversions:  # conda-env-export
	pyline -f environment.versions.yml "line.split('=', -1)[0]" | \
	sed "s/- python$$/- python=3.7/g" | \
	tee environment.noversions.yml

conda-env-export-all: conda-env-export conda-env-stripversions \
	conda-env-export-from-history

nb:
	jupyter notebook --ip=127.0.0.1 --notebook-dir=.


jupyterlab:
	jupyter-lab --ip=127.0.0.1 --notebook-dir=.

lab: jupyterlab

FIND_NOTEBOOKS=find $(mkfile_dir) -name '*.ipynb' ! -wholename '*.ipynb_checkpoints/*' ! -name '*.nbconvert.ipynb'

test: test-all

test-all:
	${PYTHON_OPTS} \
	${FIND_NOTEBOOKS} -exec echo \; -exec echo "## {}" \; -exec jupyter-nbconvert --execute --to notebook {} \;

run-all:
	${PYTHON_OPTS} \
	${FIND_NOTEBOOKS} -exec echo \; -exec echo "## {}" \; -exec jupyter-nbconvert --execute --to notebook --inplace {} \;

header-footer-templates:
	@#pip install markdown-it-py
	markdown-it README.md.header.md > index.html.header.html
	markdown-it README.md.footer.md > index.html.footer.html

html-index:
	python ./makeindex.py \
		--html \
		--title="westurner/notebooks - Jupyter notebooks" \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./index.html

readme-index:
	python ./makeindex.py \
		--readme \
		--title="westurner/notebooks - Jupyter notebooks" \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./README.md

index: html-index readme-index

index-html: html-index

index-readme: readme-index

index-test:
	python ./makeindex.py \
		-v \
		--html \
		--title="westurner/notebooks - Jupyter notebooks" \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./index.html
	python ./makeindex.py \
		-v \
		--readme \
		--title="westurner/notebooks - Jupyter notebooks" \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./README.md


html-all:
	${PYTHON_OPTS} \
	${FIND_NOTEBOOKS} -print0 \
	| while read -d $$'\0' file; do \
		cd "$$(dirname "$$file")"; \
		jupyter nbconvert "`basename $$file`" --to html; \
		htmlfile=`echo "$$file" | sed 's/.ipynb$$/.html/g'` ; \
	done;
	$(MAKE) html-index
	$(MAKE) readme-index


py-all:
	${PYTHON_OPTS} \
	${FIND_NOTEBOOKS} -print0 \
	| while read -d $$'\0' file; do \
		cd "$$(dirname "$$file")"; \
		jupyter nbconvert "`basename $$file`" --to python; \
	done;

clean-html:
	rm index.html
	find $(mkfile_dir) -name '*.html' -print0 | xargs -0 rm -fv

clean: clean-html


