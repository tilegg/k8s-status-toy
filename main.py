from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from distutils import util
import platform


live = True
ready = True


def hello_world(request):
    return Response('Hello from {}'.format(platform.node()))


def not_found(request):
    return Response(status=404)


def liveness(request):
    global live

    if request.method == "POST":
        live = request.json_body
        return Response(status=200, body="Liveness set to {}".format(live))

    else:
        if live:
            return Response(status=200, body="Service is alive")
        else:
            return Response(status=500, body="Service is dead")

def readyness(request):
    global ready

    if request.method == "POST":
        ready = request.json_body
        return Response(status=200, body="Readyness set to {}".format(live))

    else:
        if ready:
            return Response(status=200, body="Service is ready to serve traffic")
        else:
            return Response(status=500, body="Service is NOT ready to serve traffic")


if __name__ == '__main__':
    with Configurator() as config:

        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')

        config.add_route('notfound', '/nf')
        config.add_view(not_found, route_name='notfound')

        config.add_route('liveness', '/healthz')
        config.add_view(liveness, route_name='liveness')

        config.add_route('readyness', '/healthy')
        config.add_view(readyness, route_name='readyness')

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
