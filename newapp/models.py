from django.db import models

class Students(models.Model):
    name=models.CharField(max_length=255,db_column='name')
    age = models.IntegerField(db_column='age')
    address=models.CharField(max_length=255,db_column='address')
    roll_number= models.AutoField(primary_key=True,db_column='roll_number')
    created_timestam=models.DateTimeField(db_column='created_timestamp')

    class Meta:
        managed = False
        db_table = 'Master\".\"studnet'



class Marks(models.Model):
    id = models.AutoField(primary_key=True,db_column='id')
    roll_number=models.ForeignKey('Students',on_delete=models.CASCADE,db_column='roll_number')
    english = models.IntegerField(db_column='english')
    tamil = models.IntegerField(db_column='tamil')
    maths= models.IntegerField(db_column='maths')

    class Meta:
        managed = False
        db_table = 'Master\".\"marks'