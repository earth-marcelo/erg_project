#!/bin/bash
#clear
COR=roma
LIMITES="-60.0/-10.0/-45.0/-15.0"
CAMINHO=/home/marcelo/ERG_DataScience/01-PROCESSAMENTO/outputs

gmt begin mapa_freeair pdf
    gmt set MAP_FRAME_TYPE fancy
        
    gmt grd2cpt $CAMINHO/FREEAIR_ALINHADO.grd -C$COR -L-60/60 -Z -H -I > mydata.cpt
    
    gmt grdgradient $CAMINHO/FREEAIR_ALINHADO.grd  -Es45/60+p -Ggradients.nc -Ne0.5
    
    gmt grdimage $CAMINHO/FREEAIR_ALINHADO.grd -JM16c -Igradients.nc -Cmydata.cpt -Baf -B+t"FREEAIR Alinhada nos Vértices"
    
    # Continente ESCURO (Pintado por cima para fechar o mapa)
    gmt coast -R$LIMITES -JM16c -W0.5p,black -Ggray20 -Df
    
    # Barra de cores
    gmt colorbar -Cmydata.cpt -Bx20f10 -By+lmGal -DJMR+o1c/0c
gmt end

# Abre e limpa#
xdg-open mapa_freeair.pdf > /dev/null 2>&1 &

rm  gradients.nc mydata.cpt