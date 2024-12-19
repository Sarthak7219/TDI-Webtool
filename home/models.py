from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings


# Create your models here.

class Tribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tribe',default=settings.ADMIN_USER_PHONE_NUMBER)
    year = models.IntegerField()
    name = models.CharField(max_length=50)
    total_tribals = models.IntegerField(null=True, blank=True)
    H_DI = models.FloatField(null=True, blank=True)
    E_DI = models.FloatField(null=True, blank=True)
    S_DI = models.FloatField(null=True, blank=True)
    C_DI = models.FloatField(null=True, blank=True)
    G_DI = models.FloatField(null=True, blank=True)
    tribal_incidence = models.FloatField(null=True, blank=True)
    tribal_intensity = models.FloatField(null=True, blank=True)
    TDI = models.FloatField(null=True, blank=True)
    UNC_CD_score= models.FloatField(null=True, blank=True)
    UNC_IM_score= models.FloatField(null=True, blank=True)
    UNC_MC_score= models.FloatField(null=True, blank=True)
    UNC_CM_score= models.FloatField(null=True, blank=True)
    UNC_FS_score= models.FloatField(null=True, blank=True)
    UNC_LE_score= models.FloatField(null=True, blank=True)
    UNC_DRO_score= models.FloatField(null=True, blank=True)
    UNC_IC_score= models.FloatField(null=True, blank=True)
    UNC_OW_score= models.FloatField(null=True, blank=True)
    UNC_SANI_score= models.FloatField(null=True, blank=True)
    UNC_FUEL_score= models.FloatField(null=True, blank=True)
    UNC_DRWA_score= models.FloatField(null=True, blank=True)
    UNC_ELECTR_score= models.FloatField(null=True, blank=True)
    UNC_ASS_score= models.FloatField(null=True, blank=True)
    UNC_LAN_score= models.FloatField(null=True, blank=True)
    UNC_ARTS_score= models.FloatField(null=True, blank=True)
    UNC_EV_score= models.FloatField(null=True, blank=True)
    UNC_MEET_score= models.FloatField(null=True, blank=True)

    CEN_CD_score= models.FloatField(null=True, blank=True)
    CEN_IM_score= models.FloatField(null=True, blank=True)
    CEN_MC_score= models.FloatField(null=True, blank=True)
    CEN_CM_score= models.FloatField(null=True, blank=True)
    CEN_FS_score= models.FloatField(null=True, blank=True)
    CEN_LE_score= models.FloatField(null=True, blank=True)
    CEN_DRO_score= models.FloatField(null=True, blank=True)
    CEN_IC_score= models.FloatField(null=True, blank=True)
    CEN_OW_score= models.FloatField(null=True, blank=True)
    CEN_SANI_score= models.FloatField(null=True, blank=True)
    CEN_FUEL_score= models.FloatField(null=True, blank=True)
    CEN_DRWA_score= models.FloatField(null=True, blank=True)
    CEN_ELECTR_score= models.FloatField(null=True, blank=True)
    CEN_ASS_score= models.FloatField(null=True, blank=True)
    CEN_LAN_score= models.FloatField(null=True, blank=True)
    CEN_ARTS_score= models.FloatField(null=True, blank=True)
    CEN_EV_score= models.FloatField(null=True, blank=True)
    CEN_MEET_score= models.FloatField(null=True, blank=True)

    CD_contri_to_H= models.FloatField(null=True, blank=True)
    IM_contri_to_H= models.FloatField(null=True, blank=True)
    MC_contri_to_H= models.FloatField(null=True, blank=True)
    CM_contri_to_H= models.FloatField(null=True, blank=True)
    FS_contri_to_H= models.FloatField(null=True, blank=True)

    LE_contri_to_E= models.FloatField(null=True, blank=True)
    DRO_contri_to_E= models.FloatField(null=True, blank=True)

    IC_contri_to_S= models.FloatField(null=True, blank=True)
    OW_contri_to_S= models.FloatField(null=True, blank=True)
    SANI_contri_to_S= models.FloatField(null=True, blank=True)
    FUEL_contri_to_S= models.FloatField(null=True, blank=True)
    DRWA_contri_to_S= models.FloatField(null=True, blank=True)
    ELECTR_contri_to_S= models.FloatField(null=True, blank=True)
    ASS_contri_to_S= models.FloatField(null=True, blank=True)

    LAN_contri_to_C= models.FloatField(null=True, blank=True)
    ARTS_contri_to_C= models.FloatField(null=True, blank=True)

    EV_contri_to_G= models.FloatField(null=True, blank=True)
    MEET_contri_to_G= models.FloatField(null=True, blank=True)

    H_contri_to_TDI= models.FloatField(null=True, blank=True)
    E_contri_to_TDI= models.FloatField(null=True, blank=True)
    S_contri_to_TDI= models.FloatField(null=True, blank=True)
    C_contri_to_TDI= models.FloatField(null=True, blank=True)
    G_contri_to_TDI= models.FloatField(null=True, blank=True)


    village_details = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'year', 'name')


    def save(self, *args, **kwargs):
        # self.slug = slugify(self.name)
        super(Tribe, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}-{self.year}-{self.id}"
    


class Tribe_Image(models.Model):
    tribe = models.ForeignKey(Tribe, on_delete=models.SET_NULL, related_name='tribe_image', null=True, blank=True)
    logo_image=models.ImageField(upload_to='images/logo_images')
    main_image=models.ImageField(upload_to='images/main_images')
    main_desc = models.CharField(max_length=100,null=True, blank=True)
    village_image=models.ImageField(upload_to='images/village_images')
    village_desc = models.CharField(max_length=100,null=True, blank=True)
    location=models.CharField(max_length=50, null=True, blank=True)
    map_image = models.ImageField(upload_to='images/map_images')
    date = models.DateField(null=True, blank=True)

    # def __str__(self):
    #     return f"{self.tribe.name} images"

    
