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

.PHONY: help setup Makefile

setup:
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install --upgrade wheel
	.venv/bin/pip install -r requirements.txt

serve:
	sphinx-autobuild -b html $(SOURCEDIR) $(BUILDDIR)/html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
