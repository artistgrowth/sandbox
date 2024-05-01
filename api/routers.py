from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):
    """
    Custom Router to add a patch mapping to the bulk_update method in the default list path
    """

    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        # Modify default routes to add bulk_update
        for route in routes:
            if route.name == "{basename}-list":
                route.mapping.update({'patch': 'bulk_update'})
        return routes
