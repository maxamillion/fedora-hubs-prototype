from hubs.widgets import dummy
from hubs.widgets import stats
from hubs.widgets import rules
from hubs.widgets import sticky

from hubs.widgets.base import AGPLv3, smartcache

registry = {
    'dummy': dummy,
    'stats': stats,
    'rules': rules,
    'sticky': sticky,
}


def validate_registry(registry):
    """ Ensure that the widgets in the registry have the bits they need.

    - Check that a template is available and has a render callable.
    - Look for a data function, etc..
    """
    for name, module in registry.items():
        if not hasattr(module, 'template'):
            raise AttributeError('%r has no "template"' % module)
        if not hasattr(module.template, 'render'):
            raise AttributeError('%r\'s template has no "render"' % module)
        if not callable(module.template.render):
            raise TypeError('%r\'s template.render not callable' % module)

        if not hasattr(module, 'data'):
            raise AttributeError('%r has not "data" function' % module)
        if not callable(module.data):
            raise TypeError('%r\'s "data" is not callable' % module)

        if hasattr(module, 'chrome'):
            if not callable(module.chrome):
                raise TypeError('%r\'s "chrome" is not callable' % module)


def prepare_registry(registry):
    """ Do things ahead of time that we can to the registry.

    - Wrap a cache layer around the data functions.
    - Wrap any chrome around the render functions.
    """
    for name, module in registry.items():
        # Wrap chrome around the render function
        module.render = module.template.render
        if hasattr(module, 'chrome'):
            module.render = module.chrome(module.render)

        # Put source links in all API results
        module.data = AGPLv3(name)(module.data)

        # Wrap the data functions in a cache layer to be invalidated by fedmsg
        module.data = smartcache(module)(module.data)


validate_registry(registry)
prepare_registry(registry)

def render(module, session, widget, *args, **kwargs):
    """ Main API entry point.

    Call this to render a widget into HTML
    """
    # The API returns exactly this data.  Shared cache
    data = module.data(session, widget, *args, **kwargs)

    # Use the API data to fill out a template, and potentially decorate it.
    return module.render(**data)
