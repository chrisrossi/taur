from pyramid.traversal import find_interface
from pyramid_layout.layout import layout_config

from .models import Site
from .models import Sites


@layout_config(context=Sites, template="templates/admin_layout.pt")
class AdminLayout(object):
    page_title = "Taur"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.js_url = request.static_url('taur:static/js/')

    def static(self, path):
        return self.request.static_url('taur:static/' + path)


@layout_config(containment=Site, template="skin/templates/main_layout.pt")
class MainLayout(AdminLayout):

    def __init__(self, context, request):
        super(MainLayout, self).__init__(context, request)
        self.site = site = find_interface(context, Site)

        if site is context:
            self.page_title = site.title
        else:
            self.page_title = "%s: %s" % (site.title, context.title)
