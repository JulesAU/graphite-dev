import whisper
import time
import re
import os.path
import json

from urlparse import parse_qs

def application(environ, start_response):
    server = Server(environ)

    response = server.run()

    return response.display(start_response)

class Server:
    def __init__(self, environ):
        self.environ = environ

    def run(self):
        query = parse_qs(self.environ['QUERY_STRING'])

        if not 'metric' in query:
            return Response(400, "Should contain at least one metric name")

        if 'from' in query:
            from_ = int(query['from'][0])
        else:
            from_ = int(time.time()) - 60 * 60 * 24

        if 'until' in query:
            until = int(query['until'][0])
        else:
            until = int(time.time())

        datas = {}

        for metric in query['metric']:
            filteredMetric = re.sub('[^\w\d/]', '', metric)

            filename = '/opt/graphite/storage/whisper/'+filteredMetric+'.wsp'

            if not os.path.exists(filename):
                print "Metric not found", metric
                datas[metric] = None
                continue

            (timeInfo, values) = whisper.fetch(filename, from_, until)

            (start,end,step) = timeInfo

            datas[metric] = {
                'start': start,
                'end': end,
                'step': step,
                'values': values
            }

        response = Response(200, "callback("+json.dumps(datas)+");")
        response.set_content_type('application/json')

        return response

class Response:
    descriptions = {400: 'Bad request', 200: 'OK'}

    def __init__(self, code, body):
        self.code = code
        self.body = body
        self.content_type = 'text/plain'

    def set_content_type(self, type):
        self.content_type = type

    def display(self, start_response):
        description = Response.descriptions[self.code] if self.code in Response.descriptions else ''

        start_response(str(self.code) + description, [("Content-Type", self.content_type), ("Content-Length", str(len(self.body)))])

        return [self.body]