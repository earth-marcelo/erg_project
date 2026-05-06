import os
import shutil

def mover(origem, destino):
    if os.path.exists(origem):
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        print(f"Movendo: {origem} -> {destino}")
        shutil.move(origem, destino)
    else:
        print(f"Não encontrado: {origem}")

# =========================
# 📦 GRIDS (intermediate)
# =========================
mover("outputs/grids/bouguer_267.grd", "results/intermediate/bouguer_267.grd")
mover("outputs/grids/bouguer_290.grd", "results/intermediate/bouguer_290.grd")

# =========================
# 🖼 FIGURAS
# =========================
mover("results/maps/topografia.png", "results/figures/topografia.png")
mover("results/maps/freeair.png", "results/figures/freeair.png")
mover("results/maps/bouguer_267.png", "results/figures/bouguer_267.png")
mover("results/maps/bouguer_290.png", "results/figures/bouguer_290.png")

# =========================
# 🧠 PYTHON (src organizado)
# =========================
mover("outputs/grids/mapas_python.py", "src/make_maps.py")

# =========================
# 🧹 LIMPEZA OPCIONAL
# =========================
# (descomenta só quando tiver certeza)

# if os.path.exists("outputs"):
#     print("Removendo pasta outputs/")
#     shutil.rmtree("outputs")

print("\n✔ Organização concluída.")