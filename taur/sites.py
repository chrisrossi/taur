import churro
import os


class Sites(object):
    __parent__ = None
    __name__ = None

    def __init__(self, settings):
        self.path = path = settings['sites']
        if not os.path.exists(path):
            os.makedirs(path)
        self.scan_sites()

    def scan_sites(self):
        self.sites = sites = {}
        self.sites_by_hostname = by_hostname = {}
        path = self.path
        for name in os.listdir(path):
            folder = os.path.join(path, name)
            try:
                site = churro.Churro(folder, create=False)
                sites[name] = {
                    'hostname': site.hostname,
                    'title': site.title}
                if site.hostname:
                    by_hostname[site.hostname] = name
            except:
                continue

    def keys(self):
        return self.sites.keys()
