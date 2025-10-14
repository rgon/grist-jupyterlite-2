function code() {
  const packageUrl = new URL('../files/package.tar.gz', window.location.href).href;

  // language=Python
  return `
import sys
import types

async def __bootstrap_grist(url):
  from pyodide.http import pyfetch  # noqa
  import io
  import tarfile
  import importlib

  response = await pyfetch(url)
  bytes_file = io.BytesIO(await response.bytes())



  with tarfile.open(fileobj=bytes_file) as tar:
    # List all files in the tarball for debugging
    print("Tarball contents:", tar.getnames())
    import os
    cwd = os.getcwd()
    # Manually extract files for Pyodide compatibility
    for member in tar.getmembers():
      target_path = os.path.join(cwd, member.name)
      if member.isdir():
        if not os.path.exists(target_path):
          os.makedirs(target_path, exist_ok=True)
      elif member.isfile():
        # Ensure parent directory exists
        parent = os.path.dirname(target_path)
        if not os.path.exists(parent):
          os.makedirs(parent, exist_ok=True)
        with open(target_path, "wb") as out_f, tar.extractfile(member) as in_f:
          out_f.write(in_f.read())

  # Debug: print current working directory and its contents
  print("CWD:", cwd)
  print("Files in CWD:", os.listdir())
  print("grist in CWD:", os.path.isdir("grist"))
  print("grist/browser in CWD:", os.path.isdir("grist/browser"))
  if os.path.isdir("grist"):
    print("grist dir:", os.listdir("grist"))
  if os.path.isdir("grist/browser"):
    print("grist/browser dir:", os.listdir("grist/browser"))


  # Ensure current directory is in sys.path
  import os
  cwd = os.getcwd()
  if cwd not in sys.path:
    sys.path.insert(0, cwd)

  # Invalidate import caches so Python sees new files
  importlib.invalidate_caches()

  # Force reload in case grist was previously loaded
  if 'grist' in sys.modules:
    importlib.reload(sys.modules['grist'])
  if 'grist.browser' in sys.modules:
    importlib.reload(sys.modules['grist.browser'])

  import grist.browser  # noqa
  grist_obj = grist.browser.grist
  # Expose grist at module level
  globals()['grist'] = grist_obj
  return grist_obj

grist = await __bootstrap_grist(${JSON.stringify(packageUrl)})
`;
}

export default code;
