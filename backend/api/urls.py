from django.urls import path

from api.views import Statistics_ViewSet

urlpatterns = [
    path('', Statistics_ViewSet.as_view(actions={
        'get': 'list',
        'post': 'create',
        'delete': 'destroy'
    })),
]
