#!/bin/bash
#clear
COR=tempo
LIMITES="-60.0/-10.0/-45.0/-15.0"
CAMINHO=/home/marcelo/ERG_DataScience/01-PROCESSAMENTO/outputs

gmt begin mapa_topo pdf
    gmt set MAP_FRAME_TYPE fancy
        
    gmt grd2cpt $CAMINHO/TOPO_ALINHADO.grd -C$COR -L-6000/0 -Z -H -I > mydata.cpt
    
    gmt grdgradient $CAMINHO/TOPO_ALINHADO.grd -A45 -Ggradients.nc -Ne0.5
    
    gmt grdimage $CAMINHO/TOPO_ALINHADO.grd -JM16c -Igradients.nc -Cmydata.cpt -Baf -B+t"Batimetria Alinhada nos Vértices"
    
    # Continente ESCURO (Pintado por cima para fechar o mapa)
    gmt coast -R$LIMITES -JM16c -W0.5p,black -Ggray20 -Df
    
    # Barra de cores
    gmt colorbar -Cmydata.cpt -Bx1000f500 -By+lm -DJMR+o1c/0c
gmt end

# Abre e limpa#
xdg-open mapa_topo.pdf > /dev/null 2>&1 &

rm  gradients.nc mydata.cpt