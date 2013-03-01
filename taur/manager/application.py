import churro
import os

from pyramid.config import Configurator
from pyramid.exceptions import NotFound

from ..site.models import Site
from ..utils import make_unique_name


def main(global_config, **config):
    settings = global_config.copy()
    settings.update(config)
    config = Configurator(settings=settings, root_factory=find_root)
    config.registry.sites = Sites(settings)
    config.include('pyramid_layout')
    config.include('pyramid_tm')
    config.add_static_view('css', 'taur.manager:static/css/')
    config.add_static_view('js', 'taur:js/')
    config.scan('taur.manager')
    config.add_route('site', '/sites/{site}*path')
    config.add_view(site_dispatch, route_name='site')
    return config.make_wsgi_app()


def find_root(request):
    sites = request.registry.sites
    return sites


class Sites(object):
    __parent__ = None
    __name__ = None

    def __init__(self, settings):
        self.path = path = settings['sites']
        if not os.path.exists(path):
            os.makedirs(path)
        self.scan_sites()

    def scan_sites(self):
        self.sites = {}
        self.sites_by_hostname = {}
        path = self.path
        for name in os.listdir(path):
            folder = os.path.join(path, name)
            if os.path.isdir(folder):
                site = LazySite(folder)
                self._add_site(site)

    def proxies(self):
        sites = self.sites.values()
        sites.sort(key=lambda site: site.title)
        return sites

    def create(self, title):
        name = make_unique_name(self.sites, title)
        folder = os.path.join(self.path, name)
        site = churro.Churro(folder, factory=Site).root()
        site.title = title
        site = LazySite(folder, site)
        self._add_site(site)
        return site

    def _add_site(self, site):
        self.sites[site.name] = site
        if site.hostname:
            self.sites_by_hostname[site.hostname] = site.name


class LazySite(object):
    __parent__ = None
    __name__ = None
    app = None

    def __init__(self, folder, site=None):
        self.name = os.path.split(folder)[1]
        self.folder = folder
        if site is None:
            site = churro.Churro(folder, create=False).root()
        self.title = site.title
        self.hostname = site.hostname

    def get_root(self, request=None):
        return churro.Churro(self.folder, create=False).root()

    def application(self):
        if self.app is not None:
            return self.app

        site = self.get_root()
        config = Configurator(settings=site.settings,
                              root_factory=self.get_root)
        config.include('pyramid_layout')
        config.add_static_view('css', 'taur.site:static/css/')
        config.add_static_view('js', 'taur:js/')
        config.scan('taur.site')
        self.app = app = config.make_wsgi_app()
        return app


def site_dispatch(context, request):
    print 'Hello', request.url
    name = request.matchdict['site']
    site = context.sites.get(name)
    if not site:
        raise NotFound

    # Copy request, getting rid of bfg keys from the environ
    path = request.matchdict['path']
    environ = request.environ.copy()
    for key in list(environ.keys()):
        if key.startswith('bfg.'):
            del environ[key]
    request = request.__class__(environ)

    request.script_name = '/'.join((request.script_name, 'sites', name))
    request.path_info = '/' + '/'.join(path)

    print 'Script', request.script_name
    print 'Path', request.path_info
    return request.get_response(site.application())
