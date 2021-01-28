from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from jsonfield import JSONField

# class User(models.Model):
#     user_id = models.IntegerField()
#     email = models.CharField(max_length=200)
#     password = models.CharField(_('password'), max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))

#     def set_password(self, raw_password):
#         import random
#         algo = 'sha1'
#         salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
#         hsh = get_hexdigest(algo, salt, raw_password)
#         self.password = '%s$%s$%s' % (algo, salt, hsh)
# class OwnerUser(User):
#     paypalEmail = models.CharField(max_length=200)

# class AuthUser(User):
#     algorandID = models.CharField(max_length=200)

# class FunderUser(User):
#     temp = models.CharField(max_length=200)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'funder'),
        (2, 'owner'),
        (3, 'auth')
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)
    USERNAME_FIELD = 'username'

class OwnerUser(models.Model):
    user = models.OneToOneField(User, related_name='owner_detail', on_delete=models.CASCADE, primary_key=True)
    paypal_email = models.CharField(max_length=200)

class AuthUser(models.Model):
    user = models.OneToOneField(User, related_name='auth_detail', on_delete=models.CASCADE, primary_key=True)
    algorand_id = models.CharField(max_length=200)

class FunderUser(models.Model):
    user = models.OneToOneField(User, related_name='funder_detail', on_delete=models.CASCADE, primary_key=True)

class Forest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    # GEEtif = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True)
    gee_image = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True) #filename
    gee_loss = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True) #filename
    lat1 = models.FloatField()
    lat2 = models.FloatField()
    long1 = models.FloatField()
    long2 = models.FloatField()
    owner = models.ForeignKey(OwnerUser, on_delete=models.CASCADE) #forest_set
    varified = models.BooleanField()

    def __str__(self):
        return self.name
class Region(models.Model):
    description = models.CharField(max_length=200, blank=True)
    attr1 = models.IntegerField()
    attr2 = models.IntegerField()
    attr3 = models.IntegerField()
    attr4 = models.IntegerField()
    area = JSONField()
    block_size = models.FloatField()
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, related_name="region")
# Create your models here.
