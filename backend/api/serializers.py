from rest_framework import serializers
from api.models import Statistics
from api.service import calc_cpm, calc_cpc
from datetime import date

class Statistics_serializer(serializers.ModelSerializer):
    cpc = serializers.ReadOnlyField()
    cpm = serializers.ReadOnlyField()

    def validate_date(self, date_):
        """
        Checks if date >= 2000-01-01 and <= today's date.
        :param date_: input date. format(YYYY-MM-DD).
        :return: date or validation error.
        """
        min_date = date(2000, 1, 1)
        max_date = date.today()
        print(max_date)
        if date_ <= min_date or date_ >= max_date:
            raise serializers.ValidationError('The date has to be >= 2000-01-01 and <= today')
        else:
            return date_

    def is_valid(self, raise_exception=False):
        return super().is_valid(True)

    def save(self, **kwargs):
        """
        Before saving, it calculates CPC, CPM then, adding them to validated_data.
        :param kwargs:
        :return:
        """
        self.validated_data['cpc'] = calc_cpc(self.validated_data)
        self.validated_data['cpm'] = calc_cpm(self.validated_data)
        print(self.validated_data)
        return super(Statistics_serializer, self).save()

    class Meta:
        model = Statistics
        fields = ('date', 'views', 'clicks', 'cost', 'cost_currency', 'cpc', 'cpm')
