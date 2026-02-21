from rest_framework import serializers

from apps.lottery.models import Lottery


class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = "__all__"
