from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):

    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        # only if this additional_routes_by_method is present
        # we will add that to routes
        additional_routes_by_method = getattr(viewset, "additional_routes_by_method", {})
        if len(additional_routes_by_method) > 0:
            for route in routes:
                if route.name == "{basename}-list":
                    route.mapping.update(additional_routes_by_method)
        return routes
