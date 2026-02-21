from rest_framework import serializers

from apps.lottery.models import Ballot, Lottery


class BallotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ballot
        fields = "__all__"


class BallotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ballot
        exclude = ("participant",)

    def validate_lottery(self, lottery):
        if lottery.status != Lottery.Status.ACTIVE:
            raise serializers.ValidationError(f"Lottery with id={lottery.id} is not valid")

        return lottery


    def create(self, validated_data):
        request = self.context["request"]
        item = {
            "participant": request.user,
            **validated_data,
        }
        return Ballot.objects.create(**item)
