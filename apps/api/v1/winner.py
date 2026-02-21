from django_filters import rest_framework as filters
from rest_framework import generics, permissions

from apps.api.filters import WinnerFilter
from apps.api.serializers import WinnerSerializer
from apps.lottery.models import Winner


class WinnerListView(generics.ListAPIView):
    serializer_class = WinnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WinnerFilter

    def get_queryset(self):
        return Winner.objects.all()
