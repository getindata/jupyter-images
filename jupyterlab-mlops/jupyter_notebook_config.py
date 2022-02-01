import os

c = get_config()  # noqa: F821
c.NotebookApp.open_browser = False
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.base_url=os.getenv('NB_PREFIX', '')
c.ServerApp.root_dir = f"/home/{os.environ['NB_USER']}"

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

c.ServerProxy.servers = {
    'mlflow': {
            'command': ['/usr/local/bin/start-mlflow.sh'],
            'port': 5000,
            'absolute_url': False,
            'timeout': 30,
            'launcher_entry': {
                'title': "mlflow",
                'icon_path': '/usr/local/share/mlflow-logo.svg'
        }
    }
}

if os.getenv('VSCODE_VERSION', 'NONE') != 'NONE':
    c.ServerProxy.servers['vscode'] = {
        'command': ['/bin/bash', '-c', '/usr/local/bin/start-vscode.sh', '{port}'],
        'port': 7000,
        'absolute_url': False,
        'timeout': 30,
        'launcher_entry': {
            'title': "VSCode",
            'icon_path': '/usr/local/share/vscode-logo.svg',
        }
    }
