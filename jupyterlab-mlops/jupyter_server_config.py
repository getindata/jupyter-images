import os
import requests

c = get_config()  # noqa: F821
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.open_browser = False

try:
    proxy_url_response = requests.get(
            'http://metadata.google.internal/computeMetadata/v1/instance/attributes/proxy-url',
            headers={'Metadata-Flavor': 'Google'})
    assert proxy_url_response.status_code == 200
    c.ServerApp.allow_origin_pat = 'https://' + proxy_url_response.text
    c.ServerApp.port = 8080
except Exception: # not running on Vertex AI
    import traceback
    traceback.print_exc()
    c.ServerApp.port = 8888

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ["NB_UMASK"], 8))
