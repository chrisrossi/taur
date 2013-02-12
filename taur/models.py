import churro
import os

from .utils import make_unique_name


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
                site = churro.Churro(folder, create=False).root()
                self._add_site(name, site)

    def keys(self):
        return self.sites.keys()

    def create(self, title):
        name = make_unique_name(self.sites, title)
        folder = os.path.join(self.path, name)
        site = churro.Churro(folder, factory=Site).root()
        site.title = title
        self._add_site(name, site)
        return site

    def _add_site(self, name, site):
        site.__name__ = name
        self.sites[name] = {
            'hostname': site.hostname,
            'title': site.title}
        if site.hostname:
            self.sites_by_hostname[site.hostname] = name


class Site(churro.PersistentFolder):
    title = churro.PersistentProperty()
    hostname = churro.PersistentProperty()
