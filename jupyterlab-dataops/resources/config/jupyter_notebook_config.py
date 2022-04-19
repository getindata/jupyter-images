import os

c = get_config()  # noqa: F821
c.NotebookApp.open_browser = False
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.base_url=os.getenv('NB_PREFIX', '')

c.FileContentsManager.delete_to_trash = False

c.ServerProxy.servers = {}
c.ServerProxy.servers['vscode'] = {
    'command': ['/bin/bash', '-c', '/opt/tools/bin/start-vscode.sh', '{port}'],
    'port': 7000,
    'absolute_url': False,
    'timeout': 30,
    'new_browser_tab': False,
    'launcher_entry': {
        'title': "VSCode",
        'icon_path': '/opt/tools/logos/vs-code.svg',
    }
}
c.ServerProxy.servers['cloudbeaver'] = {
    'command': ['/bin/bash', '-c', 'cd /opt/tools/cloudbeaver && ./run-server.sh', '{port}'],
    'port': 8978,
    'absolute_url': True,
    'timeout': 30,
    'new_browser_tab': False,
    'launcher_entry': {
        'title': "CloudBeaver",
        'icon_path': '/opt/tools/logos/cloudbeaver.svg',
    }
}
c.ServerProxy.servers['dbt_docs'] = {
    'command': ['echo'],
    'port': 9328,
    'absolute_url': False,
    'timeout': 180,
    'new_browser_tab': False,
    'launcher_entry': {
        'title': "DBT Docs",
        'icon_path': '/opt/tools/logos/docs.svg',
    }
}
