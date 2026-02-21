from django_filters import rest_framework as filters

from apps.lottery.models import Winner


class WinnerFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="selected_at", lookup_expr="date")

    class Meta:
        model = Winner
        fields = ("date",)
