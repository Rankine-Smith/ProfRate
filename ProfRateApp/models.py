from django.db import models
#need to import user model 


class Professors(models.Model):
    code = models.CharField(max_length=3) #make uniquie?
    name = models.CharField(max_length=30)
    def __str__(self):
        return u'%s %s' % (self.code, self.name) 
    
class Modules(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=30)
    taughtYear = models.IntegerField()
    semester = models.IntegerField()
    taughtBy = models.ManyToManyField(Professors)
    def __str__(self):
        return u'%s %s' % (self.code, self.name) 


class Ratings(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    module_year = models.IntegerField()
    Professor = models.ForeignKey(Professors, on_delete=models.CASCADE)
    rating = models.IntegerField()
    def __str__(self):
        return u'%s %s %s' % (self.module, self.Professor, self.rating) 
    
    




    



# Create your models here.
