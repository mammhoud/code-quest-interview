from django.urls import include, path

# from src import logger
# from common import loggerDjango as logger


def show_toolbar(*args, **kwargs) -> bool:
    """
    The general idea is the following:

    1. We show the toolbar if we have it installed & we have it configured to be shown.
        - This opens up the option to move the dependency as a local one, if one chooses to do so.
    2. This function acts as the single source of truth of that.
        - No additional checks elsewhere are required.

    This means we can have the following options possible:

    - Show on a production environments.
    - Exclude the entire dependency from production environments.
    - Have the flexibility to control the debug toolbar via a single Django setting.

    Additionally, we don't sure if you want to deal with the INTERNAL_IPS thing.
    """
    from .settings import DEBUG_TOOLBAR_ENABLED

    if not DEBUG_TOOLBAR_ENABLED:
        return False

    try:
        import debug_toolbar  # noqa
    except ImportError:
        # logger.debug("No installation found for: django_debug_toolbar")
        return False

    return True


class DebugToolbarSetup:
    """
    We use a class, just for namespacing convenience.
    """

    @staticmethod
    def update_middleware(MIDDLEWARE, middleware_position=None):
        if not show_toolbar():
            return MIDDLEWARE
        else:
            debug_toolbar_middleware = "debug_toolbar.middleware.DebugToolbarMiddleware"

            if middleware_position is None:
                MIDDLEWARE = MIDDLEWARE + [debug_toolbar_middleware]
            else:
                # Grab a new copy of the list, since insert mutates the internal structure
                _middleware = MIDDLEWARE[::]
                _middleware.insert(middleware_position, debug_toolbar_middleware)

                MIDDLEWARE = _middleware

            return MIDDLEWARE

    @staticmethod
    def do_settings(
        INSTALLED_APPS,
        MIDDLEWARE,
        middleware_position=None,
    ):
        _show_toolbar: bool = show_toolbar()
        # logger.debug(f"Django Debug Toolbar in use: {_show_toolbar}")

        if not _show_toolbar:
            # if SHARED_APPS:  # noqa: F823
            #     SHARED_APPS = SHARED_APPS + ["debug_toolbar"]  # noqa: F841
            #     logger.debug("debug_toolbar Added to SHARED_APPS")
            return INSTALLED_APPS, MIDDLEWARE
        INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar"]
        # logger.debug("debug_toolbar Added to INSTALLED_APPS")

        # In order to deal with that:
        # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-middleware
        # The order of MIDDLEWARE is important.
        # You should include the Debug Toolbar middleware as early as possible in the list.
        # However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware.
        # We support inserting the middleware at an arbitrary position in the list.
        # If position is not specified, we will just include it at the end of the list.

        debug_toolbar_middleware = "debug_toolbar.middleware.DebugToolbarMiddleware"

        if middleware_position is None:
            MIDDLEWARE = MIDDLEWARE + [debug_toolbar_middleware]
        else:
            # Grab a new copy of the list, since insert mutates the internal structure
            _middleware = MIDDLEWARE[::]
            _middleware.insert(middleware_position, debug_toolbar_middleware)

            MIDDLEWARE = _middleware

        return INSTALLED_APPS, MIDDLEWARE

    @staticmethod
    def do_urls(urlpatterns):
        if not show_toolbar():
            return urlpatterns

        import debug_toolbar  # noqa

        # logger.debug("debug_toolbar Added to urlpatterns")

        return urlpatterns + [path("__debug__/", include(debug_toolbar.urls))]
