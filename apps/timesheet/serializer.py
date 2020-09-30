from rest_framework import serializers

from apps.timesheet.models import TimeSheet


class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'user_id', 'date', 'time_start', 'time_end']
        model = TimeSheet
