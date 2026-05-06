#!/usr/bin/env bash

OPEN=/home/marcelo/erg_project/01_data
SAVE=/home/marcelo/erg_project/04_results/01_intermediate

LIMITES=-60/-10/-45/-15
PROJ=-JM16c
COR=turbo


gmt grdmath $OPEN/topo.grd -200 GE $SAVE/bouguer_267.grd NaN IFELSE = $SAVE/bouguer_mask_temp.grd
gmt grdinfo $SAVE/bouguer_mask_temp.grd

#gmt begin mapa_bouguer_final pdf
#gmt set MAP_FRAME_TYPE fancy


# máscara
#gmt grdmath $CAMINHO/topo.grd -200 LT $CAMINHO/bouguer.grd NaN IFELSE = bouguer_mask.grd

#gmt grd2cpt $CAMINHO/bouguer_mask.grd -C$COR -L-160/140 -Z -H  > mydata.cpt
#gmt makecpt -Cturbo -T-200/125 -H > mydata.cpt

#gmt grdimage $CAMINHO/bouguer_mask.grd -JM16c  -Cmydata.cpt -Ei600  -f0x,1y 

#gmt grdgradient $CAMINHO/bouguer_mask.grd $REGIAO -Ep45/60+p  -Ggradients.grd -Ne0.6 -f0x,1y
#gmt grdimage $CAMINHO/bouguer_mask.grd -JM16c  -Cmydata.cpt -Ei600  -f0x,1y -Igradients.grd

#gmt grdimage bouguer_mask.grd $REGIAO $PROJ -C -B -Q 

#gmt coast $REGIAO $PROJ -Ggray -W0.5p

#gmt colorbar -DjBR+o-1c/2.5c+w7.0c/0.32c+mc -Bx50f25 -By+lmGal -I -Cmydata.cpt

#gmt end show

#gmt grd2cpt $CAMINHO/bouguer_mask.grd -E100 -V > /dev/null

#rm bouguer_mask.grd