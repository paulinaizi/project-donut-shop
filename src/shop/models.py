from django.db import models
    
class Donut(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/donuts/')
    is_custom_base = models.BooleanField(default=False)
    coating = models.ForeignKey('Coating', null=True, blank=True, on_delete=models.CASCADE)
    sprinkle = models.ForeignKey('Sprinkle', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Donuty'

class Sprinkle(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='uploads/sprinkles/')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Posypka'
        verbose_name_plural = 'Posypki'

class Coating(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='uploads/coatings/')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Polewa'
        verbose_name_plural = 'Polewy'