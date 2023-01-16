import shutil
import os


def _codeserver_command():
    full_path = shutil.which('code-server')
    if not full_path:
        raise FileNotFoundError('Can not find code-server in $PATH')
    working_dir = os.getenv("CODE_WORKINGDIR", None) or os.getenv("JUPYTER_SERVER_ROOT", ".")
    return [full_path, f'--port=7000',  "--extensions-dir", "/var/tmp/extension","--auth", "none", working_dir]


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
