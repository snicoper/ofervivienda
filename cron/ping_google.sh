#!/bin/bash

source $HOME/.bashrc

workon "ofervivienda.com"

source _variables.sh

$PROJECT_ROOT/prod_manage.py ping_google /sitemap.xml

echo "Ping Google realizado con exito"
