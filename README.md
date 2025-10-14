# JupyterLite Notebook Grist Custom Widget

> [!TIP]
> See [USAGE.md](./USAGE.md) for instructions on how to use this widget in Grist. This README is for developers.

This repo is a custom deployment of JupyterLite generated from https://github.com/jupyterlite/demo.

## Development

1. Ensure `uv` is installed
2. Run `./dev.sh` to start a local JupyterLite server.

## Files

- `extension/` contains the JupyterLab extension that connects the Grist and JupyterLab APIs. See the [README there](./extension/README.md) for more details.
- `grist/` contains most of the Python code that runs inside the JupyterLite Pyodide and that users can call.
- `package.sh` packages the files under `grist` and puts them in `files/package.tar.gz`. JupyterLite picks up the contents of `files` when building, so the package can be downloaded from http://localhost:8000/files/package.tar.gz. `package.sh` is run by both `dev.sh` and the GitHub Action.
- `extension/src/initKernelPy.ts` contains the 'bootstrapping' Python code that the extension runs in the kernel on startup. It downloads the package, extracts it, and imports it.
- `dev.sh` cleans out old state, does some minimal building for development, and starts a local JupyterLite server.
- `jupyter-lite.json` contains configuration for the JupyterLite deployment.

## Dependencies

The widget loads many resources at runtime:

- The Grist plugin API (used by all custom widgets) from https://docs.getgrist.com/grist-plugin-api.js
- An optimised, pre-compiled Pyodide distribution from URLs starting with https://cdn.jsdelivr.net/pyodide/v0.24.0/pyc/
- Python packages (whether required by the widget itself or imported by the user's code) from https://pypi.org/ (for metadata) and https://files.pythonhosted.org/ (for wheel files containing the actual packages).
