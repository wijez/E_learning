from rest_framework import serializers

from E_learning.app.models import Lessions


class LessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessions
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']

