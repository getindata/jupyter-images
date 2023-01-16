import os

HOME_PATH = "/home/jupyter"

c = get_config()  # noqa: F821

c.NotebookApp.open_browser = False
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.base_url = os.getenv('NB_PREFIX', '')
c.ServerApp.root_dir = HOME_PATH
c.ServerApp.notebook_dir = HOME_PATH
