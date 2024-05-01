from django.urls import include, path, URLResolver
from rest_framework.response import Response
from rest_framework.views import APIView
from django.apps import apps
from importlib import import_module


class AllAPIEndpointsView(APIView):
    apps_to_include = ['authentication', 'Api',
                       'stylist', 'client', 'administration']

    def get(self, request):
        all_endpoints = {}

        for app_name in self.apps_to_include:
            try:
                urls_module = import_module(app_name + '.urls')
            except ModuleNotFoundError:
                continue  # Skip apps without URLs

            urlpatterns = urls_module.urlpatterns
            endpoints = self._get_endpoints(urlpatterns, app_name)
            all_endpoints[app_name] = endpoints

        return Response({'endpoints': all_endpoints})

    def _get_endpoints(self, urlpatterns, app_name):
        endpoints = []

        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                endpoints.extend(self._get_endpoints(
                    pattern.url_patterns, app_name))
            else:
                path = str(pattern.pattern)
                if hasattr(pattern, 'name') and pattern.name:
                    endpoint = {
                        'name': pattern.name,
                        'path': path,
                        'full_url': f'http://localhost:8000/{path}',
                        'app': app_name
                    }
                    endpoints.append(endpoint)

        return endpoints
