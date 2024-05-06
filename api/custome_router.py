from rest_framework import routers

class PatchRouter(routers.DefaultRouter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routes[0].mapping.update({"patch": "bulk_update"}
    )