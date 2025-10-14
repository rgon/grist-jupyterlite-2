function code() {
  const packageUrl = new URL('../files/grist-0.0.0-py3-none-any.whl', window.location.href).href;

  // language=Python
  return `
import micropip
await micropip.install(${JSON.stringify(packageUrl)})

async def __bootstrap_grist():
  import grist.browser.api as browser
  return browser.grist

grist = await __bootstrap_grist()
`;
}

export default code;
