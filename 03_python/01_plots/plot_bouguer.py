from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# === raiz do projeto ===
BASE_DIR = Path(__file__).resolve().parents[2]

# === arquivos ===
topo = xr.open_dataset(BASE_DIR / "01_data/topo.grd")
b267 = xr.open_dataset(BASE_DIR / "04_results/01_intermediate/bouguer_267.grd")
b290 = xr.open_dataset(BASE_DIR / "04_results/01_intermediate/bouguer_290.grd")

z_topo = topo["z"]
z267 = b267["z"]
z290 = b290["z"]

lon = topo["lon"]
lat = topo["lat"]

# === máscara plataforma (>-200 m) ===
mask_oceano_profundo = z_topo < -200

z267 = z267.where(mask_oceano_profundo)
z290 = z290.where(mask_oceano_profundo)

# === função de plot ===
def plot_map(data, title):

    fig = plt.figure(figsize=(8,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # dados
    im = ax.pcolormesh(
        lon, lat, data,
        cmap="RdBu_r",
        vmin=-200, vmax=200,
        shading="auto"
    )

    # continente cinza
    ax.add_feature(cfeature.LAND, facecolor="0.6", zorder=3)

    # linha de costa preta
    ax.coastlines(color="black", linewidth=0.8, zorder=4)

    # limites
    ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()])

    # colorbar CONTROLADA (sem ficar gigante)
    cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("mGal")

    plt.title(title)
    plt.show()


# === plots ===
plot_map(z267, "Bouguer 2.67 g/cm³")
plot_map(z290, "Bouguer 2.90 g/cm³")