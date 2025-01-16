from django.core.serializers import serialize

from E_learning.app.models import Assignments


class AssignmentsSerializer(serialize.ModelSerializer):
    class Meta:
        models = Assignments
        fields= '__all__'
