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
    organization_name = models.CharField(max_length=200)

class AuthUser(models.Model):
    user = models.OneToOneField(User, related_name='auth_detail', on_delete=models.CASCADE, primary_key=True)
    # algorand_id = models.CharField(max_length=200)

class FunderUser(models.Model):
    user = models.OneToOneField(User, related_name='funder_detail', on_delete=models.CASCADE, primary_key=True)

class Forest(models.Model):
    id = models.AutoField(primary_key=True)
    STATE_CREATED = 1
    STATE_VARIFIED = 2
    STATE_COMPLETED = 3
    STATE_CHOICES = (
        (STATE_CREATED, 'created'),
        (STATE_VARIFIED, 'varified'),
        (STATE_COMPLETED, 'completed'),
    )
    state = models.IntegerField(choices=STATE_CHOICES, default=1)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    # GEEtif = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True)
    gee_image = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True) #filename
    gee_loss = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True) #filename
    maps_image = models.FileField( upload_to=settings.MEDIA_ROOT, null=True, blank=True) #filename
    metadata_file = models.FileField( upload_to='files/', null=True, blank=True) #filename
    lat1 = models.FloatField()
    lat2 = models.FloatField()
    long1 = models.FloatField()
    long2 = models.FloatField()
    owner = models.ForeignKey(OwnerUser, on_delete=models.CASCADE) #forest_set
    varified = models.BooleanField()

    def __str__(self):
        return self.name
class Region(models.Model):
    SCALE_NONE = 0
    SCALE_LOW = 1
    SCALE_MED = 2
    SCALE_HIGH = 3
    SCALE_VERY_HIGH = 4
    SCALE_PRELIM = 5
    SCALE_IN_HOUSE = 6
    SCALE_3RD_PARTY = 7
    SCALE_CHOICES = (
        (SCALE_NONE, 'none'),
        (SCALE_LOW, 'low'),
        (SCALE_MED, 'med'),
        (SCALE_HIGH, 'high'),
        (SCALE_VERY_HIGH, 'very high'),
        (SCALE_PRELIM, 'prelim'),
        (SCALE_IN_HOUSE, 'in house'),
        (SCALE_3RD_PARTY, '3rd party'),
    )
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, blank=True)
    biodiversity_benefit = models.IntegerField(choices=SCALE_CHOICES, blank=True)
    livelihood_benefit = models.IntegerField(choices=SCALE_CHOICES, blank=True)
    local_benefit = models.IntegerField(choices=SCALE_CHOICES, blank=True)
    carbon_credit_status = models.IntegerField(choices=SCALE_CHOICES, blank=True)
    minised_leakage = models.IntegerField(choices=SCALE_CHOICES, blank=True)    
    carbon_sequestration = models.FloatField(blank=True)
    domestic = models.BooleanField(blank=True)
    international = models.BooleanField(blank=True)
    nature_based = models.BooleanField(blank=True)
    area = JSONField(blank=True)
    block_size = models.FloatField(blank=True)
    certificates = JSONField()
    funding_goal = models.IntegerField(blank=True, null=True)
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, related_name="region")
    