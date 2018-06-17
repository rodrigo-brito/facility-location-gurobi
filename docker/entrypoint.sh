#!/bin/sh

set -e

if [ "${1:0:1}" = '-' ]; then
    set -- gurobi "$@"
fi

if [[ "$VERBOSE" = "yes" ]]; then
    set -x
fi

license=/opt/gurobi/gurobi.lic
if [ -f $license ]; then
    echo "Skipping license creation"
    bash
else
    echo "Configure license $GUROBI_LICENSE"
    echo -ne '\n' | grbgetkey $GUROBI_LICENSE
    bash
fi