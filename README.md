# Mike Nelson QuPath Extensions

Experimental QuPath extensions developed by Mike Nelson at [LOCI](https://eliceirilab.org/), University of Wisconsin-Madison.

**Note:** These are prototype tools under active development. They have not been peer-reviewed or published. Use at your own discretion -- APIs and behavior may change between versions. Bug reports and feedback are welcome via each extension's GitHub Issues page.

## Adding This Catalog to QuPath

1. Open QuPath (v0.6.0 or later)
2. Go to **Extensions > Manage extensions**
3. Click **Manage extension catalogs**
4. Click **Add** and enter this URL:
   ```
   https://github.com/uw-loci/qupath-catalog-mikenelson
   ```
5. Click **OK** to confirm

The extensions from this catalog will now appear in the extension manager.

## Featured Extensions

The three extensions below are marked as featured in `catalog.json` (`"starred": true`) and surface first in QuPath's extension manager. They are the most mature tools in this catalog.

### QuIET - Image Export Toolkit
Comprehensive batch export of rendered overlays, label masks, raw pixel data, and ML training tiles. Wizard UI, generated reproducible Groovy scripts, and built-in publication-advice for figure preparation.

- **Repository**: https://github.com/uw-loci/qupath-extension-image-export-toolkit

### Dialog Position Manager
Remembers and restores dialog window positions across sessions. Automatically recovers windows that become inaccessible (e.g., when a monitor is disconnected). Useful on multi-monitor setups.

- **Repository**: https://github.com/uw-loci/qupath-extension-dialog-manager

### Wizard Wand
Interactive magic-wand annotation tool with adjustable tolerance for region-growing. Click and drag to expand or contract the selected region in real time.

- **Repository**: https://github.com/uw-loci/qupath-extension-wizard-wand

## Other Extensions

### Deep Learning Pixel Classifier
Deep learning pixel classification with embedded Python inference via Appose. Train and apply pixel classifiers using PyTorch/ONNX models directly within QuPath. Per-tile and project-wide batch inference with context-tile support and FIXED_RANGE normalization.

- **Repository**: https://github.com/uw-loci/qupath-extension-dl-pixel-classifier

### QP-CAT - Cell Analysis Tools
Python-powered clustering (Leiden, KMeans, HDBSCAN, BANKSY, and more), rule-based phenotyping, dimensionality reduction (UMAP, PCA, t-SNE), spatial statistics (Ripley K/L, Geary's C, co-occurrence), multi-figure batch export, optional LLM-driven cluster explanations, and YAML headless batch workflows. Designed for multiplexed imaging data.

- **Repository**: https://github.com/uw-loci/qupath-extension-cell-analysis-tools

### Polyline Wand
Brush- and wand-style editor for line and polyline annotations. Push, smooth, scissors-cut, and erase-from-end modes with two swappable engines (direct vertex push, arc-length displacement field).

- **Repository**: https://github.com/uw-loci/qupath-extension-polyline-wand

### Gated Object Classifier
Apply a saved object classifier to a *gated* subset of objects, defined by class membership, a measurement threshold, the current viewer selection, or any combination. Live preview of how many objects will be classified; each apply records a reusable workflow step that can be replayed across a project.

- **Repository**: https://github.com/uw-loci/qupath-extension-gated-object-classifier

### Project Metadata Browser
Browse, search, and edit metadata across all images in a QuPath project from a single table view. Per-column sort and filter, column-visibility menu, CSV/TSV export.

- **Repository**: https://github.com/uw-loci/qupath-extension-project-metadata-browser

### Channel Names Viewer
Always-visible floating legend listing the currently-selected fluorescence channels, color-coded and live-updating as you toggle channels in Brightness/Contrast. Preserves user channel ordering and offers an outline-contrast assist for dark channels.

- **Repository**: https://github.com/uw-loci/qupath-extension-channel-names-viewer

## Requirements

- QuPath 0.6.0 or later

## For Developers

This catalog follows the [QuPath Extension Catalog Model](https://github.com/qupath/extension-catalog-model).
