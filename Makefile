
# Makefile for IPython notebooks

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir = $(shell dirname $(mkfile_path))

default:
	@echo "IPython notebooks"

install:
	# pip install virtualenvwrapper
	# mkvirtualenv <name>
	bash ./install.sh

nb:
	ipython notebook --secure --ip=127.0.0.1 --notebook-dir=.

test: test_all

test-all:
	find $(mkfile_dir) -name '*.ipynb' -exec runipy {} \;

run-all:
	find $(mkfile_dir) -name '*.ipynb' -exec runipy -o {} \;

html-index:
	python ./makeindex.py \
		--base-url=/github/westurner/notebooks/blob/gh-pages/ > ./index.html

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



clean-html:
	rm index.html
	find $(mkfile_dir) -name '*.html' -print0 | xargs -0 rm -fv

clean: clean-html


