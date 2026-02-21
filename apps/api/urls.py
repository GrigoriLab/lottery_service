from django.urls import include, path

from apps.api.v1.lottery import LotteryListView

apipatterns_v1 = [
    path("lotteries/", LotteryListView.as_view(), name="lotteries"),
]

urlpatterns = [
    path("v1/", include(apipatterns_v1)),
]
