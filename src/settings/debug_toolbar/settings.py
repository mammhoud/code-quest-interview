# from src import env
# from src.envs import Environment

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "src.settings.debug_toolbar.setup.show_toolbar",  # change this based on path of show_toolbar
    # Toolbar options
    "RESULTS_CACHE_SIZE": 3,
    "SHOW_COLLAPSED": False,
    # Panel options
    "SQL_WARNING_THRESHOLD": 100,  # milliseconds
}

DEBUG_TOOLBAR_CONFIG["IS_RUNNING_TESTS"] = True
# You can place additional settings below
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html
DEBUG_TOOLBAR_ENABLED = True

# if not DEBUG_TOOLBAR_ENABLED:

#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    # "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    # "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]
