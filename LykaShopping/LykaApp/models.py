from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Cate(models.Model):
    typeName = models.CharField(max_length = 250, unique = True)
    slug = models.SlugField(max_length = 250, unique = True)

    def __str__(self):
        return self.typeName
    
    def getUrl(self):
        return reverse('devCat', args=[self.slug])



class Device(models.Model):
    category = models.ForeignKey(Cate, on_delete = models.CASCADE)
    brand = models.CharField(max_length = 50)
    price = models.IntegerField()
    modelName = models.CharField(max_length = 100, unique = True)
    slugModel = models.SlugField(max_length = 100, unique = True)
    stock = models.IntegerField()
    availability = models.BooleanField()
    desc = models.TextField(max_length = 500)

    def __str__(self):
        n = self.brand + " " + self.modelName
        return n

    def show_image_1(self):
        return self.images.all()[0]
    
    def show_image_2(self):
        return self.images.all()[1]
    
    def show_image_3(self):
        try:
            return self.images.all()[2]
        except IndexError:
            return "img not found"

               
    def show_image_4(self):
        try:
            return self.images.all()[3]
        except IndexError:
            return "img not found"
    
    def getUrlDev(self):
        return reverse('devDetail' , args=[self.category.slug,self.slugModel])
    

    
def get_image_filename(instance, filename):
    title = instance.DeviceName.modelName
    slug = slugify(title)
    return "product_images/%s-%s" % (slug, filename) 


class Image(models.Model):
    imgname = models.CharField(max_length = 50)
    DeviceName = models.ForeignKey(Device, related_name = "images", on_delete = models.CASCADE)
    image = models.ImageField(upload_to = get_image_filename, verbose_name='Image') 
    def __str__(self):
        return self.imgname

class DeviceFeatures(models.Model):
    deviceName = models.ForeignKey(Device, related_name="features", on_delete = models.CASCADE)
    camera =  models.CharField(max_length = 100)
    battery = models.IntegerField()
    display = models.CharField(max_length = 100)
    ram = models.IntegerField()
    rom = models.IntegerField()
    processor = models.CharField(max_length = 100)

    def __str__(self):
        return self.deviceName.brand + " " + self.deviceName.modelName