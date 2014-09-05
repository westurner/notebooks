#!/bin/bash -x

# Install python (2.7+)

INSTALLDIR="./downloads"

PIP_BIN=$(which pip)
PIP_USER=""

CONDA_BIN=$(which conda)

install_pip() {
    GET_PIP="${INSTALLDIR}/get-pip.py"
    if [ -z "${PIP_BIN}" ]; then
        mkdir -p "${INSTALLDIR}";
        wget "https://bootstrap.pypa.io/get-pip.py" -O "${GET_PIP}";
        python "${GET_PIP}" --user;
        PIP_BIN=$(which pip)
    fi
}

install_conda() {
    ${PIP_BIN} install ${PIP_USER} --upgrade conda
    CONDA_BIN=$(which conda)
}

install_notebook_pkgs() {
    ${CONDA_BIN} install --yes \
        grin \
        curl pycurl ssl_match_hostname \
        pytz dateutil \
        nose pytest pep8 flake8 pyflakes pylint coverage \
        cython numpy numexpr scipy \
        pandas \
        pytables hdf5 sqlite sqlalchemy pandasql  \
        gdata \
        xlrd xlwt \
        ipython ipython-notebook runipy \
        matplotlib basemap \
        bokeh \
        mayavi \
        statsmodels patsy \
        scikit-learn \
        networkx \
        nltk \
        flask werkzeug \
        docutils sphinx pygments \
        blaze numba \
        keyring \
        lxml html5lib beautiful-soup \
        spyder 
        #theano
    ${PIP_BIN} install \
        mpld3 \
        plotly matplotlylib \
        rest-pandas \
        quandl
    # ${PIP_BIN} install MySQL-python
}

main() {
    install_pip && \
    install_conda && \
    install_notebook_pkgs
}

if [[ "$BASH_SOURCE" == "$0" ]]; then
  main
fi 
