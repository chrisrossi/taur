from pyramid.config import Configurator

from .models import Sites


def main(global_config, **config):
    settings = global_config.copy()
    settings.update(config)
    config = Configurator(settings=settings, root_factory=find_root)
    config.registry.sites = Sites(settings)
    config.include('pyramid_layout')
    config.include('pyramid_tm')
    config.add_static_view('css', 'taur:static/css/')
    config.add_static_view('js', 'taur:static/js/')
    config.scan()
    return config.make_wsgi_app()


def find_root(request):
    sites = request.registry.sites
    return sites
