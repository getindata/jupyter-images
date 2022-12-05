import os
import requests
import time

c = get_config()  # noqa: F821
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True

def get_gooogle_instance_attribute(attribute_name):
    try:
        response = requests.get(
                f'http://metadata.google.internal/computeMetadata/v1/instance/attributes/{attribute_name}',
                headers={'Metadata-Flavor': 'Google'})
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

try:
    maybe_vertex_framework = get_gooogle_instance_attribute('framework')
    assert maybe_vertex_framework == 'Container' # Vertex AI Notebook
    for _ in range(60):
        proxy_url = get_gooogle_instance_attribute('proxy-url')
        if proxy_url is not None:
            break
        time.sleep(1)
    assert proxy_url.endswith('notebooks.googleusercontent.com') # Proxy was set
    c.ServerApp.allow_origin_pat = 'https://' + proxy_url
    c.ServerApp.port = 8080
except Exception: # not running on Vertex AI
    pass

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ["NB_UMASK"], 8))
