import os
import shutil
import time

import requests

c = get_config()  # noqa: F821
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True

# HOME_PATH = "/home/jupyter"
c.NotebookApp.open_browser = False
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.base_url = os.getenv('NB_PREFIX', '')
# c.ServerApp.root_dir = HOME_PATH
# c.ServerApp.notebook_dir = HOME_PATH

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

# c.FileCheckpoints.checkpoint_dir = f'{HOME_PATH}/checkpoints'


def _get_gooogle_instance_attribute(attribute_name):
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
    maybe_vertex_framework = _get_gooogle_instance_attribute('framework')
    assert maybe_vertex_framework == 'Container'  # Vertex AI Notebook
    for _ in range(60):
        proxy_url = _get_gooogle_instance_attribute('proxy-url')
        if proxy_url is not None:
            break
        time.sleep(1)
    assert proxy_url.endswith('notebooks.googleusercontent.com')  # Proxy was set
    c.ServerApp.allow_origin_pat = 'https://' + proxy_url
    c.ServerApp.port = 8080
except Exception:  # not running on Vertex AI
    pass

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ["NB_UMASK"], 8))


def _codeserver_command():
    full_path = shutil.which('code-server')
    if not full_path:
        raise FileNotFoundError('Can not find code-server in $PATH')
    working_dir = os.getenv("CODE_WORKINGDIR", None) or os.getenv("JUPYTER_SERVER_ROOT", ".")
    return [full_path, f'--port=7000', "--auth", "none", working_dir]


c.ServerProxy.servers = {
    'flink_ui': {
        'command': ['echo'],
        'port': 8099,
        'absolute_url': False,
        'timeout': 180,
        'new_browser_tab': False,
        'launcher_entry': {
            'title': "Flink UI",
            'icon_path': '/opt/logos/flink.svg',
        }
    },
    'vscode': {
        'command': _codeserver_command(),
        'port': 7000,
        'absolute_url': False,
        'new_browser_tab': False,
        'timeout': 180,
        'launcher_entry': {
            'title': "VSCode",
            'icon_path': '/opt/logos/vs-code.svg',
        }
    }
}
