# DayTrader City Visualization

This repository contains a minimal **CesiumJS** web app that visualises a 3‑D city populated with AI day‑traders.

## What's inside
- **generate_city.py** – Blender Python script that builds a simple grid‑city (blocks + random‑height buildings) and exports it as `city.glb`.
- **index.html**, **style.css**, **trader.js** – CesiumJS front‑end (same as the guide but ready to run).
- **README.md** – instructions on how to generate the city, export to 3D Tiles/GLTF, host the files, and push to GitHub.
- **.gitignore** – ignores Blender cache files and large assets.

## Quick start (local)
```bash
# 1️⃣ Install Blender (2.93+ recommended) and Python dependencies
# 2️⃣ Run the city generator (creates city.glb)
blender --background --python generate_city.py

# 3️⃣ Serve the folder (Python http server)
python -m http.server 8000
# Open http://localhost:8000 in a modern browser.
```

## Publishing
1. Create a new repository on GitHub (e.g. `youruser/daytrader-city`).
2. Add the remote and push:
```bash
git init
git add .
git commit -m "Initial commit – Cesium city visualisation"
git branch -M main
git remote add origin https://github.com/youruser/daytrader-city.git
git push -u origin main
```
3. Enable **GitHub Pages** on the `main` branch (Settings → Pages → Source: `gh‑pages` or `main`).
4. Your site will be live at `https://youruser.github.io/daytrader-city/`.

> **NOTE** – The city model (`city.glb`) must be reachable by the page. If you prefer **3D Tiles**, upload `city.glb` to Cesium ion, enable the *public* token, and replace the `city_tileset.json` URL in `index.html` with the generated 3D Tiles endpoint.

---

If you need further customisation (e.g., realistic building footprints, terrain, or a point‑cloud of traders), let me know and I can extend the Blender script or the Cesium front‑end.
