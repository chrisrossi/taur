from pyramid.traversal import find_interface
from pyramid_layout.layout import layout_config

from .models import Site


@layout_config(template="templates/main_layout.pt")
class MainLayout(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.js_url = request.static_url('taur:js/')
        self.site = site = find_interface(context, Site)

        if site is context:
            self.page_title = site.title
        else:
            self.page_title = "%s: %s" % (site.title, context.title)

    def static(self, path):
        return self.request.static_url('taur.site:static/' + path)

    def js(self, path):
        return self.request.static_url('taur:js/' + path)
