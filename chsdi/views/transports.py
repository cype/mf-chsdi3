# -*- coding: utf-8 -*-

from pyramid.view import view_config, view_defaults

from chsdi.models.vector.uvek import Oev_departures


@view_defaults(renderer='jsonp', route_name='transports')
class TransportView(object):

    def __init__(self, request):
        self.request = request
        if request.matched_route.name == 'transports':
            self.id = request.matchdict['id']

    @view_config(request_method='GET')
    def get_departures(self):
        query = self.request.db.query(Oev_departures).filter(Oev_departures.stop == self.id).limit(10)
        results = [q.stop for q in query]
        return results
