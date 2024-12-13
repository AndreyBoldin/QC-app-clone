from rest_framework import serializers
from .models import Projects, Batches, Samples, Groups, Metabolites, Metabolites_conc

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
        
class BatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batches
        fields = '__all__'

class SamplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Samples
        fields = '__all__'

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'
        
class MetabolitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metabolites
        fields = '__all__'
        
class Metabolites_concSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metabolites_conc
        fields = '__all__'

