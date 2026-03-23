# Mike Nelson QuPath Extensions

General-purpose QuPath extensions developed by Mike Nelson at [LOCI](https://eliceirilab.org/), University of Wisconsin-Madison.

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

## Available Extensions

### DL Pixel Classifier
Deep learning pixel classification with embedded Python inference via Appose. Train and apply pixel classifiers using PyTorch/ONNX models directly within QuPath.

- **Repository**: https://github.com/uw-loci/qupath-extension-DL-pixel-classifier

### QP-CAT - Cluster Analysis Tools
Python-powered clustering (Leiden, KMeans, HDBSCAN, BANKSY, and more), rule-based phenotyping, dimensionality reduction (UMAP, PCA, t-SNE), and spatial analysis for multiplexed imaging data.

- **Repository**: https://github.com/uw-loci/qupath-extension-pyclustering

### Dialog Position Manager
Remembers and restores dialog window positions across sessions. Automatically recovers windows that become inaccessible (e.g., when a monitor is disconnected).

- **Repository**: https://github.com/uw-loci/qupath-extension-dialog-manager

### OCR for Labels
Optical character recognition for extracting text and barcodes from slide labels. Supports template-based metadata extraction.

- **Repository**: https://github.com/uw-loci/qupath-extension-ocr4labels

### QuIET - Image Export Toolkit
Comprehensive batch export of rendered overlays, label masks, raw pixel data, and ML training tiles with wizard UI, script generation, and publication advice.

- **Repository**: https://github.com/uw-loci/qupath-extension-image-export-toolkit

## Requirements

- QuPath 0.6.0 or later

## For Developers

This catalog follows the [QuPath Extension Catalog Model](https://github.com/qupath/extension-catalog-model).
