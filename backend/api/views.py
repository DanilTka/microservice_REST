from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import *
from rest_framework.permissions import IsAdminUser

from api.service import sort_response


class Statistics_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = Statistics_serializer
    ordering_fields = ['date', 'views', 'clicks', 'cost', 'cpc', 'cpm']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if self.request.query_params.get("ordering"):
            return sort_response(response, request)
        else:
            return response

    def get_queryset(self):
        """
        Gets queryset in the date range if url has params (from, to) if not returns all objects.
        Sort result queryset by date.
        :return: sorted by date queryset.
        """
        if self.request.query_params.get("from") and self.request.query_params.get("to"):
            from_ = self.request.query_params['from']
            to_ = self.request.query_params['to']
            queryset = Statistics.objects.filter(
                date__range=[from_, to_]
            ).order_by('-date')
        else:
            queryset = Statistics.objects.all().order_by('-date')
        return queryset

    def destroy(self, request, *args, **kwargs):
        Statistics.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
