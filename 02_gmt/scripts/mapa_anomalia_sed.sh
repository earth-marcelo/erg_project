#!/bin/bash
# Script Final - Versao Resiliente

AREA="-60/-10/-45/-15"
PROJ="-JM20c"
DADO="../01-PROCESSAMENTO/outputs/anomalia_sedimentos.xyz"
OUT="mapa_anomalia_sedimentos.pdf"

echo "🎯 GMT processando... Quase lá, Marcelo!"

gmt begin $OUT pdf
    gmt set MAP_FRAME_TYPE fancy
    
    # 1. Cores
    gmt makecpt -Cmagma -T-150/0/10 -Z
    
    # 2. XYZ para Grid (com -r para evitar erro de incompatibilidade)
    gmt xyz2grd $DADO -R$AREA -I1m -Gtemp_anomalia.grd -i0,1,2 -sh -r
    
    # 3. Imagem
    gmt grdimage temp_anomalia.grd $PROJ -Baf -B+t"Anomalia Gravimetrica de Sedimentos"
    
    # 4. Costa
    gmt coast $PROJ -R$AREA -W0.5p,black -Ggray -Df
    
    # 5. Legenda
    gmt colorbar -DjMR+w10c/0.5c+o1.2c/0c -Baf+l"mGal"
gmt end

rm -f temp_anomalia.grd
echo "✅ SUCESSO! O mapa $OUT foi criado."