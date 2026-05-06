#!/bin/bash
set -euo pipefail

LIMITES="-60.0/-10.0/-45.0/-15.0"

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CAMINHO="${BASE_DIR}/outputs/grids"

mkdir -p "${CAMINHO}"

echo "Gerando topo..."

# 1. Recorta topografia do GEBCO
gmt grdcut @earth_gebco_01m -R${LIMITES} -G${CAMINHO}/topo_tmp.grd

# 2. Reamostragem
gmt grdsample ${CAMINHO}/topo_tmp.grd -r -G${CAMINHO}/topo.grd

# 3. Limpeza
rm -f ${CAMINHO}/topo_tmp.grd

echo "Topo final gerado em: ${CAMINHO}/topo.grd"