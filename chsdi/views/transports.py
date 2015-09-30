# -*- coding: utf-8 -*-

from sqlalchemy import and_
from pyramid.view import view_config, view_defaults
from chsdi.models.vector.uvek import Oev_departures
import datetime


@view_defaults(renderer='jsonp', route_name='transports')
class TransportView(object):

    def __init__(self, request):
        self.request = request
        if request.matched_route.name == 'transports':
            self.id = request.matchdict['id']

    @view_config(request_method='GET')
    def get_departures(self):
        current_date = datetime.datetime.now()
        #next_thirty_minutes = current_date + datetime.timedelta(minutes=30)
        query = self.request.db.query(Oev_departures).filter(and_(Oev_departures.stop == self.id, Oev_departures.time > current_date)).order_by(Oev_departures.time).limit(10)

        def serialize(time):
            return time.strftime('%Y/%m/%d %H:%M:%S')

        def type_transports(type):
            if type == 0:
                return 'Tram'
            elif type == 1:
                return 'Metro'
            elif type == 2:
                return 'Train'
            elif type == 3:
                return 'Bus'
            elif type == 4:
                return 'Bateau'
            elif type == 5:
                return 'Telepherique'
            elif type == 6:
                return 'Funiculaire'
            elif type == 7:
                return '7'
            elif type == 8:
                return '8'
            elif type == 9:
                return '9'
            elif type == 10:
                return '10'
            elif type == 11:
                return '11'
            elif type == 12:
                return '12'
            elif type == 13:
                return '13'
            elif type == 14:
                return '14'
            elif type == 15:
                return '15'
            elif type == 16:
                return '16'
            elif type == 17:
                return '17'

        results = [{
            'id': q.stop,
            'time': serialize(q.time),
            'label': q.label,
            'destination': q.destination,
            'via': q.via,
            'type': type_transports(q.type)
        } for q in query]
        return results
