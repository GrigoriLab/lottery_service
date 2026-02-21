from rest_framework import generics, permissions

from apps.api.serializers import LotterySerializer
from apps.lottery.models import Lottery


class LotteryListView(generics.ListAPIView):
    serializer_class = LotterySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Lottery.objects.exclude(status=Lottery.Status.DRAFT)
