from django.db import models

# Create your models here.

class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.TextField()
    project_date = models.DateField()
    class Meta:
        db_table = 'projects'

class Batches(models.Model):
    id = models.AutoField(primary_key=True)
    batch_num = models.IntegerField()
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column='project_id')
    batch_date = models.DateField() 
    batch_normalized = models.BooleanField()
    class Meta:
        db_table = 'batches'

class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.TextField()
    class Meta:
        db_table = 'groups'
    
class Samples(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, db_column='group_id')
    batch_id = models.ForeignKey(Batches, on_delete=models.CASCADE, db_column='batch_id')
    sample_name = models.TextField(null=True)
    class Meta:
        db_table = 'samples'

class Metabolites(models.Model):
    id = models.AutoField(primary_key=True)
    metabolite_name = models.TextField()
    class Meta:
        db_table = 'metabolites'

class Metabolites_conc(models.Model):
    id = models.AutoField(primary_key=True)
    sample_id = models.ForeignKey(Samples, on_delete=models.CASCADE, db_column='sample_id')
    metabolite_id = models.ForeignKey(Metabolites, on_delete=models.CASCADE, db_column='metabolite_id')
    concentration = models.FloatField(db_column='concentration')
    class Meta:
            db_table = 'metabolite_conc'