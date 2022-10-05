c = get_config()  # noqa: F821

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
    }
}