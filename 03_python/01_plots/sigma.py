from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# === raiz do projeto ===
BASE_DIR = Path(__file__).resolve().parents[2]

# === arquivos ===
files = {
    "bouguer_267": BASE_DIR / "04_results/01_intermediate/bouguer_267.grd",
    "bouguer_290": BASE_DIR / "04_results/01_intermediate/bouguer_290.grd",
}

topo_path = BASE_DIR / "01_data/topo.grd"

# === saída ===
out_dir = BASE_DIR / "04_results/03_figures"
out_dir.mkdir(parents=True, exist_ok=True)

# === carregar topografia ===
topo = xr.open_dataset(topo_path)["z"]

# === máscaras ===
continente = topo > 0
plataforma = (topo <= 0) & (topo > -200)
oceano = topo <= 0   # ← CORREÇÃO PRINCIPAL

# === função separação ===
def separar(data, sigma=30):
    arr = data.values
    regional = gaussian_filter(arr, sigma=sigma)
    residual = arr - regional
    return xr.DataArray(regional, coords=data.coords), xr.DataArray(residual, coords=data.coords)

# === função plot ===
def plot_mapa(data, title, filename):

    plt.figure(figsize=(10,6))

    # --- dados (sem continente) ---
    im = data.where(oceano).plot(
        cmap="RdBu_r",
        add_colorbar=False,
        yincrease=True
    )

    cbar = plt.colorbar(im)
    cbar.set_label("mGal")

    topo.where(continente).plot(
    cmap="gray",
    vmin=0,
    vmax=1000,   # ← controla o contraste (mais claro)
    add_colorbar=False,
    yincrease=True
)

    # --- plataforma (branco) ---
    topo.where(plataforma).plot(
        cmap="Greys",
        vmin=0, vmax=1,
        add_colorbar=False,
        yincrease=True
    )

    # --- linha de costa ---
    plt.contour(
        topo,
        levels=[0],
        colors="black",
        linewidths=1
    )

    plt.title(title)
    plt.tight_layout()

    # salvar
    plt.savefig(filename, dpi=300)
    plt.close()


# === processamento ===
for nome, path in files.items():

    ds = xr.open_dataset(path)
    z = ds["z"]

    regional, residual = separar(z, sigma=30)

    # nomes bonitos
    label = nome.replace("_", " ").upper()

    # plots
    plot_mapa(z, f"{label} - Total", out_dir / f"{nome}_total.png")
    plot_mapa(regional, f"{label} - Regional", out_dir / f"{nome}_regional.png")
    plot_mapa(residual, f"{label} - Residual", out_dir / f"{nome}_residual.png")