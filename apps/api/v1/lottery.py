from rest_framework import generics

from apps.api.serializers import LotterySerializer
from apps.lottery.models import Lottery


class LotteryListView(generics.ListAPIView):
    serializer_class = LotterySerializer
    queryset = Lottery.objects.all()
