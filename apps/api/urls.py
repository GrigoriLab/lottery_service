from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.api.v1.ballot import BallotListCreateView
from apps.api.v1.lottery import LotteryListView
from apps.api.v1.register import RegisterView
from apps.api.v1.winner import WinnerListView

apipatterns_v1 = [
    path("lotteries/", LotteryListView.as_view(), name="lotteries"),
    path("ballots/", BallotListCreateView.as_view(), name="ballots"),
    path("winners/", WinnerListView.as_view(), name="winners"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]

urlpatterns = [
    path("v1/", include(apipatterns_v1)),
]
