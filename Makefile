# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Uberspace7lab
SOURCEDIR     = source
BUILDDIR      = build

PYTHON_VERSION = $(shell cat runtime.txt)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help setup setup-venv setup-pre-commit lint check-guides Makefile

setup: setup-venv setup-pre-commit

setup-venv:
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install --upgrade wheel
	.venv/bin/pip install -r requirements.txt

setup-pre-commit:
	.venv/bin/pre-commit install --overwrite --install-hooks

lint:
	.venv/bin/pre-commit run --all-files

check-guides:
	.venv/bin/python check-guides.py --check --warn source/guide_*.rst

get-new-words: clean spelling
	.venv/bin/python spelling_tools.py

add-new-words:
	.venv/bin/python spelling_tools.py --merge

serve:
	sphinx-autobuild -b html $(SOURCEDIR) $(BUILDDIR)/html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
