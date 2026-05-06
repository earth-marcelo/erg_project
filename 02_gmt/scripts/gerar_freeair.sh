#!/bin/bash

LIMITES="-60.0/-10.0/-45.0/-15.0"

BASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CAMINHO="$BASE_DIR/outputs/grids"

mkdir -p "$CAMINHO"

echo "Gerando freeair..."

# 1. Recorta free-air
gmt grdcut @earth_faa_01m -R$LIMITES -G$CAMINHO/freeair_tmp.grd

# 2. Verifica topo
if [ ! -f "$CAMINHO/topo.grd" ]; then
    echo "Erro: topo.grd não encontrado"
    exit 1
fi

# 3. Alinha free-air ao topo (CORRETO)
gmt grdsample $CAMINHO/freeair_tmp.grd \
  -R$CAMINHO/topo.grd \
  -G$CAMINHO/freeair.grd

# 4. Limpa
rm $CAMINHO/freeair_tmp.grd

echo "Free-air alinhado ao topo"