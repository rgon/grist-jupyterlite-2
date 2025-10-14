import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the grist-jupyterlite-2 extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'grist-jupyterlite-2:plugin',
  description: 'Jupiterlite within grist',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension grist-jupyterlite-2 is activated!');
  }
};

export default plugin;
