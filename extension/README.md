# grist_jupyterlab_widget

This is a JupyterLab extension that connects the Grist and JupyterLab APIs. It's tightly coupled with the JupyterLite deployment in this repo (the parent folder) and doesn't work on its own.

This folder was originally [its own repo](https://github.com/gristlabs/jupyterlab-widget-extension) generated using `copier` following the [extension tutorial](https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html). This is the source of a lot of boilerplate configuration that probably isn't *all* needed but also probably shouldn't be messed with. Usually this extension would be published on PyPI (and maybe NPM) under the package name `grist_jupyterlab_widget`, but now the parent folder just installs it from the local filesystem.

## Code overview

Most of the logic is in `src/index.ts`.

1. The entrypoint is the exported `plugin: JupyterFrontEndPlugin` which JupyterLab picks up as an extension, running `activate(app: JupyterFrontEnd)` on startup.
2. The extension adds a `<script>` tag for `grist-plugin-api.js` to the page and uses the grist API once it loads.
3. `grist.getOption/setOption` and `app.serviceManager.contents` are used to save/load a notebook file in the widget options. All changes to the notebook are saved immediately.
4. JupyterLite automatically starts a Pyodide (Python) kernel for the notebook. Once it's ready, we execute the Python code in `src/initKernelPy.ts` which bootstraps the rest of the Python code - see the [parent README](../README.md) for more details.
5. The Pyodide kernel runs in a separate web worker. To give the user's Python code access to the `grist` API object in the main browser thread, the [`Comlink`](https://github.com/GoogleChromeLabs/comlink) library is used to `expose` the `grist` object to the worker. This requires the `Worker` object which the JupyterLab API doesn't provide, so the `Worker` constructor is monkeypatched to intercept its creation.