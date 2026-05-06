from pathlib import Path
import xarray as xr
import numpy as np
import matplotlib
matplotlib.use("Agg")  # sem GUI
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter

# ===============================
# raiz do projeto
# ===============================
BASE_DIR = Path(__file__).resolve().parents[2]

# ===============================
# leitura
# ===============================
topo = xr.open_dataset(BASE_DIR / "01_data/topo.grd")
b267 = xr.open_dataset(BASE_DIR / "04_results/01_intermediate/bouguer_267.grd")
b290 = xr.open_dataset(BASE_DIR / "04_results/01_intermediate/bouguer_290.grd")

z_topo = topo["z"].values
z267 = b267["z"].values
z290 = b290["z"].values

lon = topo["lon"].values
lat = topo["lat"].values

# ===============================
# máscara (apenas para visual)
# ===============================
mask_oceano_profundo = z_topo < -200  # True onde queremos mostrar

# ===============================
# filtro correto (ignora NaN)
# ===============================
def gaussian_filter_nan(data, sigma):
    """
    Aplica gaussian_filter ignorando NaNs usando normalização por pesos.
    """
    valid = np.isfinite(data)
    data_filled = np.where(valid, data, 0.0)
    weights = valid.astype(float)

    smooth_data = gaussian_filter(data_filled, sigma=sigma)
    smooth_weights = gaussian_filter(weights, sigma=sigma)

    # evita divisão por zero
    result = smooth_data / np.maximum(smooth_weights, 1e-8)
    return result

def separar_regional_residual(data, sigma=20):
    regional = gaussian_filter_nan(data, sigma)
    residual = data - regional
    return regional, residual

# ===============================
# cálculo
# ===============================
reg267, res267 = separar_regional_residual(z267, sigma=20)
reg290, res290 = separar_regional_residual(z290, sigma=20)

# ===============================
# função de plot (máscara só aqui)
# ===============================
def plot_map(data, title, vmin, vmax, filename):
    # aplica máscara apenas para visualização
    plot_data = np.where(mask_oceano_profundo, data, np.nan)

    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    im = ax.pcolormesh(
        lon, lat, plot_data,
        cmap="RdBu_r",
        vmin=vmin, vmax=vmax,
        shading="auto"
    )

    # continente cinza
    ax.add_feature(cfeature.LAND, facecolor="0.6", zorder=3)

    # costa preta
    ax.coastlines(color="black", linewidth=0.8, zorder=4)

    ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()])

    cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("mGal")

    plt.title(title)
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

# ===============================
# saída
# ===============================
OUT = BASE_DIR / "04_results/02_plots"
OUT.mkdir(parents=True, exist_ok=True)

# ===============================
# plots
# ===============================
# TOTAL
plot_map(z267, "Bouguer 2.67 g/cm³ - Total", -200, 200, OUT / "bouguer_267_total.png")
plot_map(z290, "Bouguer 2.90 g/cm³ - Total", -200, 200, OUT / "bouguer_290_total.png")

# REGIONAL
plot_map(reg267, "Bouguer 2.67 g/cm³ - Regional", -200, 200, OUT / "bouguer_267_regional.png")
plot_map(reg290, "Bouguer 2.90 g/cm³ - Regional", -200, 200, OUT / "bouguer_290_regional.png")

# RESIDUAL (contraste que você pediu)
plot_map(res267, "Bouguer 2.67 g/cm³ - Residual", -20, 20, OUT / "bouguer_267_residual.png")
plot_map(res290, "Bouguer 2.90 g/cm³ - Residual", -20, 20, OUT / "bouguer_290_residual.png")

print("✓ Mapas gerados em:", OUT)