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

    def __init__(self, folder, site=None):
        self.name = os.path.split(folder)[1]
        self.folder = folder
        if site is None:
            site = churro.Churro(folder, create=False).root()
        self.title = site.title
        self.hostname = site.hostname

    def __call__(self):
        return churro.Churro(self.folder, create=False).root()


class Page(churro.PersistentFolder):
    title = churro.PersistentProperty()
    body = churro.PersistentProperty()


class Site(Page):
    hostname = churro.PersistentProperty()
