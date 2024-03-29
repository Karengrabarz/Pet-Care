from rest_framework import serializers
from pets.models import SexOptions
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices= SexOptions.choices,
        default = SexOptions.not_informed
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
   