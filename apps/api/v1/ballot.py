from rest_framework import generics, permissions

from apps.api.serializers import BallotCreateSerializer, BallotSerializer
from apps.lottery.models import Ballot


class BallotListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ballot.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            return BallotCreateSerializer
        return BallotSerializer
