from pyramid.events import subscriber
from pyramid.events import BeforeRender


class Layout(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.js_url = request.static_url('taur:static/js/')

    def static(self, path):
        return self.request.static_url('taur:static/' + path)


@subscriber(BeforeRender)
def add_layout(event):
    event['layout'] = Layout(event['context'], event['request'])
