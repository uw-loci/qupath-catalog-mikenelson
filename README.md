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

## Available Extensions

### Deep Learning Pixel Classifier
Deep learning pixel classification with embedded Python inference via Appose. Train and apply pixel classifiers using PyTorch/ONNX models directly within QuPath.

- **Repository**: https://github.com/uw-loci/qupath-extension-dl-pixel-classifier

### QP-CAT - Cell Analysis Tools
Python-powered clustering (Leiden, KMeans, HDBSCAN, BANKSY, and more), rule-based phenotyping, dimensionality reduction (UMAP, PCA, t-SNE), and spatial analysis for multiplexed imaging data.

- **Repository**: https://github.com/uw-loci/qupath-extension-cell-analysis-tools

### Dialog Position Manager
Remembers and restores dialog window positions across sessions. Automatically recovers windows that become inaccessible (e.g., when a monitor is disconnected).

- **Repository**: https://github.com/uw-loci/qupath-extension-dialog-manager

### Gated Object Classifier
Apply a saved object classifier to a *gated* subset of objects, defined by class membership, a measurement threshold, the current viewer selection, or any combination. Includes a live preview of how many objects will be classified, and records each apply as a reusable workflow step that can be replayed across a project.

- **Repository**: https://github.com/uw-loci/qupath-extension-gated-object-classifier

### OCR for Labels
Optical character recognition for extracting text and barcodes from slide labels. Supports template-based metadata extraction.

- **Repository**: https://github.com/uw-loci/qupath-extension-ocr4labels

### Project Metadata Browser
Browse, search, and edit metadata across all images in a QuPath project from a single table view.

- **Repository**: https://github.com/uw-loci/qupath-extension-project-metadata-browser

### QuIET - Image Export Toolkit
Comprehensive batch export of rendered overlays, label masks, raw pixel data, and ML training tiles with wizard UI, script generation, and publication advice.

- **Repository**: https://github.com/uw-loci/qupath-extension-image-export-toolkit

### Wizard Wand
Interactive magic wand tool with adjustable tolerance for region-growing annotation.

- **Repository**: https://github.com/uw-loci/qupath-extension-wizard-wand

## Requirements

- QuPath 0.6.0 or later

## For Developers

This catalog follows the [QuPath Extension Catalog Model](https://github.com/qupath/extension-catalog-model).
