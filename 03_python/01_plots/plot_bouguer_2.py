from pathlib import Path
import numpy as np
import xarray as xr

import matplotlib
matplotlib.use("Agg")  # seguro no PyCharm

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]

topo = xr.open_dataset(BASE_DIR / "01_data/topo.grd")
b267 = xr.open_dataset(BASE_DIR / "04_results/01_intermediate/bouguer_267.grd")
b290 = xr.open_dataset(BASE_DIR / "04_results/01_intermediate/bouguer_290.grd")

z_topo = topo["z"]
z267 = b267["z"]
z290 = b290["z"]

lon = topo["lon"]
lat = topo["lat"]

# =========================
# MÁSCARA (única e consistente)
# =========================
mask = z_topo < -200

z267_mask = z267.where(mask)
z290_mask = z290.where(mask)

# =========================
# REGIONAL (suave, sem distorcer borda)
# =========================
def smooth(data, sigma=5):
    from scipy.ndimage import gaussian_filter
    return xr.DataArray(
        gaussian_filter(data.fillna(0), sigma=sigma),
        coords=data.coords,
        dims=data.dims
    )

reg267 = smooth(z267_mask, sigma=10)
res267 = z267_mask - reg267

reg290 = smooth(z290_mask, sigma=10)
res290 = z290_mask - reg290

# =========================
# FUNÇÃO DE PLOT
# =========================
def plot_map(data, title, vmin, vmax, filename):

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    im = ax.pcolormesh(
        lon, lat, data,
        cmap="RdBu_r",
        vmin=vmin,
        vmax=vmax,
        shading="auto"
    )

    # continente cinza (mantido como você queria)
    ax.add_feature(cfeature.LAND, facecolor="0.6", zorder=3)

    # linha de costa
    ax.coastlines(color="black", linewidth=0.8, zorder=4)

    ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()])

    cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("mGal")

    plt.title(title)

    plt.savefig(BASE_DIR / f"04_results/03_figures/{filename}", dpi=300)
    plt.close()

# =========================
# PLOTS
# =========================

# Total (escala ampla)
plot_map(z267_mask, "Bouguer 2.67 - Total", -200, 200, "b267_total.png")
plot_map(reg267,   "Bouguer 2.67 - Regional", -200, 200, "b267_regional.png")

# Residual (escala ajustada como você pediu)
plot_map(res267,   "Bouguer 2.67 - Residual", -20, 20, "b267_residual.png")

plot_map(z290_mask, "Bouguer 2.90 - Total", -200, 200, "b290_total.png")
plot_map(reg290,    "Bouguer 2.90 - Regional", -200, 200, "b290_regional.png")
plot_map(res290,    "Bouguer 2.90 - Residual", -20, 20, "b290_residual.png")

print("✔ Mapas gerados em: 04_results/figures/")