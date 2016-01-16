#!/bin/bash -x

#

_progname="$(basename ${0})"
main_help() {

    echo "${_progname} {pip conda notebook plotly [full spyder]}"
    echo "Install pip, conda, notebook, plotly, {'full'}, spyder"
    echo ""
    echo "  ${_progname}             # install pip, conda, notebook"
    echo "  ${_progname} spyder      # install pip, conda, notebook, spyder"
    echo "  ${_progname} spyder full # install pip, conda, notebook, spyder, full"
}


main() {
    set_PYTHON_BIN
    set_GET_PIP__PATH
    set_PIP_BIN
    set_CONDA_BIN

    INSTALL__PIP=1
    INSTALL__CONDA=1
    INSTALL__NOTEBOOK=1
    INSTALL__PLOTLY=1

    INSTALL__FULL=0
    INSTALL__SPYDER=0

    for arg in ${@} ; do
        case "${arg}" in
            pip)
                INSTALL__PIP=1 ;;
            no-pip)
                INSTALL__PIP=0 ;;
            conda)
                INSTALL__CONDA=1 ;;
            no-conda)
                INSTALL__CONDA=0 ;;
            notebook)
                INSTALL__NOTEBOOK=1 ;;
            no-notebook)
                INSTALL__NOTEBOOK=0 ;;
            plotly)
                INSTALL__PLOTLY=1 ;;
            no-plotly)
                INSTALL__PLOTLY=0 ;;
            full)
                INSTALL__FULL=1 ;;
            no-full)
                INSTALL__FULL=0 ;;
            spyder)
                INSTALL__SPYDER=1 ;;
            no-spyder)
                INSTALL__SPYDER=0 ;;
        esac
    done

    (set +x +v;
    echo INSTALL__PIP="${INSTALL__PIP}";
    echo INSTALL__CONDA="${INSTALL__CONDA}";
    echo INSTALL__NOTEBOOK="${INSTALL__NOTEBOOK}";
    echo INSTALL__PLOTLY="${INSTALL__PLOTLY}";
    echo INSTALL__FULL="${INSTALL__FULL}";
    echo INSTALL__SPYDER="${INSTALL__SPYDER}";
    )

    function install_sequence {
        if [ ${INSTALL__PIP} -gt 0 ]; then
            install_pip
            install_pip_requirements
        fi
        if [ ${INSTALL__CONDA} -gt 0 ]; then
            install_conda
        fi
        if [ ${INSTALL__NOTEBOOK} -gt 0 ]; then
            install_conda_pkgs__notebook
            install_mathjax
        fi

        if [ ${INSTALL__PLOTLY} -gt 0 ]; then
            install_pip_pkgs__plotly
            install_pip_pkgs__matplotlylib
        fi
        if [ ${INSTALL__FULL} -gt 0 ]; then
            install_conda_pkgs_full
        fi
        if [ ${INSTALL__SPYDER} -gt 0 ]; then
            install_conda_pkgs__spyder
        fi
    }
    (set -x -e; install_sequence)
}


set_GET_PIP__PATH() {
    GET_PIP__PATH="./downloads"
}

set_PYTHON_BIN() {
    PYTHON_BIN="$(which python)"
}

set_PIP_BIN() {

    #
    #  PIP_OPTS=""  # "--upgrade" "--user" "--user --upgrade"

    PIP_USER=""
    PIP_OPTS__UPGRADE=""
    for arg in ${@} ; do
        case "${arg}" in
            -U|--upgrade)
                PIP_OPTS__UPGRADE=" --upgrade"
                ;;
            --user)
                PIP_OPTS__USER=" --user"
        esac
    done
    PIP_OPTS="${PIP_OPTS:-"${PIP_OPTS__UPGRADE}${PIP_OPTS__USER}"}"

    PIP_BIN="$(which pip)"
    PIP_INSTALL="${PIP_BIN} ${PIP_OPTS} install "
}

set_CONDA_BIN() {
    CONDA_BIN="$(which conda)"
    CONDA_INSTALL="${CONDA_BIN} install --yes "
}

install_pip() {
    GET_PIP="${GET_PIP__PATH}/get-pip.py"
    if [ -z "${PIP_BIN}" ]; then
        mkdir -p "${GET_PIP__PATH}";
        wget "https://bootstrap.pypa.io/get-pip.py" -O "${GET_PIP}";
        python "${GET_PIP}" --user;
        set_PIP_BIN
    fi
}

install_pip_requirements() {
    # install makeindex.py requirements
    ${PIP_INSTALL} -r requirements.txt
}

install_conda() {
    if [ -z "${CONDA_BIN}" ]; then
        ${PIP_INSTALL} --user --upgrade conda
        set_CONDA_BIN
        ${CONDA_BIN} init
    fi
}

install_conda_pkgs_full() {
    ${CONDA_INSTALL} \
        grin \
        curl pycurl ssl_match_hostname \
        pytz dateutil \
        nose pytest pep8 flake8 pyflakes pylint coverage \
        cython numpy numexpr scipy \
        pandas \
        lxml html5lib beautiful-soup \
        pytables hdf5 sqlite sqlalchemy pandasql  \
        gdata \
        quandl \
        xlrd xlwt \
        ipython ipython-notebook runipy \
        matplotlib mpld3  basemap \
        seaborn \
        bokeh \
        mayavi \
        statsmodels patsy \
        scikit-learn \
        networkx \
        nltk \
        flask werkzeug \
        docutils sphinx pygments \
        blaze numba \
        future \
        keyring
}

install_conda_pkgs__notebook() {
    ${CONDA_INSTALL} \
        notebook  # -> IPython
}

install_pip_pkgs__plotly() {
    ${PIP_INSTALL} \
        plotly
}

install_pip_pkgs__matplotlylib() {
    ${PIP_INSTALL} \
        matplotlylib
}

install_pip_pkgs__rest_pandas() {
    ${PIP_INSTALL} \
        rest-pandas
}

install_pip_pkgs__mysql() {
    ${PIP_INSTALL} \
        MySQL-python
}

install_pip_pkgs__pydatalog() {
    ${PIP_INSTALL} \
        pydatalog
}

install_conda_pkgs__spyder() {
    ${CONDA_INSTALL} \
        spyder 
        #theano
}

install_mathjax() {
    ${PYTHON_BIN} -c 'from IPython.external import mathjax; mathjax.install_mathjax()'
}

if [[ "$BASH_SOURCE" == "${0}" ]]; then
  echo "## ${0} ${@}"
  main ${@}
  exit
fi 
