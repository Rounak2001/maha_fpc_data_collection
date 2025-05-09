# from django.contrib.auth.models import User
# from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     full_name = models.CharField(max_length=200, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return f"{self.full_name} ({self.user.username})"

# from django.contrib.gis.db import models

# class Farmer(models.Model):
#     country_id = models.IntegerField(default=2)
#     block_id = models.IntegerField()
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     mobile_number = models.CharField(max_length=15,unique=True)
#     gender = models.CharField(
#         max_length=10, 
#         choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
#         default='Male'
#     )
#     guardian_name = models.CharField(max_length=100, blank=True)
#     geo_tag = models.PointField()
#     farmer_consent = models.BooleanField(default=True)
#     village = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     metadata = models.JSONField(default=dict, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     vaarha_id = models.IntegerField(null=True, blank=True)

#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="farmers")

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"  

# class Farm(models.Model):
#     farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
#     farm_name = models.CharField(max_length=100)
#     area_in_acres = models.FloatField()
#     ownership = models.CharField(max_length=10, choices=[('OWNED', 'Owned'), ('LEASED', 'Leased')])
#     owner_mobile_number = models.CharField(max_length=15, blank=True, null=True)
#     owner_full_name = models.CharField(max_length=100, blank=True, null=True)
#     boundary_method = models.CharField(max_length=10, choices=[('Drawing', 'Drawing'), ('Tapping', 'Tapping')],default='Drawing')
#     boundary = models.PolygonField()
#     metadata = models.JSONField(default=dict, blank=True, null=True)
#     vaarha_id = models.IntegerField(null=True, blank=True)
#     land_ownership = models.FileField(upload_to='land_documents/',null=True, blank=True)
#     landlord_declaration = models.FileField(upload_to='farm_landlord_declarations/', null=True, blank=True)
#     def __str__(self):
#         return self.farm_name

# class Plantation(models.Model):
#     farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='plantations')
#     kyari_name = models.CharField(max_length=100)
#     area_in_acres = models.FloatField()
#     plantation_model = models.CharField(max_length=50, default="BLOCK")
#     plantation_year = models.IntegerField()
#     kyari_type = models.CharField(max_length=50, default="RETROSPECTIVE")
#     is_feasible = models.BooleanField(default=True)
#     boundary = models.PolygonField()
#     metadata = models.JSONField(default=dict, blank=True, null=True)
#     kyari_attributes = models.JSONField(default=dict, blank=True, null=True)
#     vaarha_id = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.kyari_name

# import os
# import uuid

# def specie_image_upload(instance, filename):
#     """Generate a unique filename for Specie images."""
#     ext = filename.split('.')[-1]  # Get file extension
#     unique_filename = f"tree_pictures/{instance.plantation.farm.farmer.id}_{instance.plantation.id}_{uuid.uuid4()}.{ext}"
#     return unique_filename

# class Specie(models.Model):
#     plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name='species')
#     specie_id = models.IntegerField()
#     number_of_plants = models.IntegerField()
#     plant_spacing = models.CharField(max_length=10)
#     spacing_cr = models.FloatField()
#     spacing_cl = models.FloatField()
#     spacing_ct = models.FloatField()
#     spacing_cb = models.FloatField()
    
#     # Assign unique filenames
#     centre_top = models.ImageField(upload_to=specie_image_upload, null=True, blank=True)
#     centre_bottom = models.ImageField(upload_to=specie_image_upload, null=True, blank=True)
#     centre_left = models.ImageField(upload_to=specie_image_upload, null=True, blank=True)
#     centre_right = models.ImageField(upload_to=specie_image_upload, null=True, blank=True)

#     specie_attributes = models.JSONField(default=dict, blank=True, null=True)
#     metadata = models.JSONField(default=dict, blank=True, null=True)
#     plantation_date = models.DateField()
#     vaarha_id = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"Specie {self.specie_id} in {self.plantation.kyari_name}"


# # class GeotaggedSapling(models.Model):
# #     plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name='saplings')
# #     specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='saplings')
# #     geo_tag = models.PointField()
# #     metadata = models.JSONField(default=dict, blank=True, null=True)

# #     def __str__(self):
# #         return f"Sapling in {self.plantation.kyari_name}"


# def farmer_media_path(instance, filename):
#     # Store files under media/farmer_media/<farmer_id>/
#     return f"farmer_media/{instance.farmer.id}/{filename}"

# class FarmerMedia(models.Model):
#     # Linked to the Farmer model
#     farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="media")

#     # Media fields
#     picture = models.ImageField(upload_to=farmer_media_path, null=True, blank=True)
#     photo_of_english_epic = models.FileField(upload_to=farmer_media_path, null=True, blank=True)
#     photo_of_regional_language_epic = models.FileField(upload_to=farmer_media_path, null=True, blank=True)

#     # ID-related fields
#     ID_TYPE_CHOICES = [
#         ("aadhar", "Aadhar Card"),
#         ("driving_licence", "Driving License"),
#         ("voter_id", "Voter ID"),
#         ("pan_card", "PAN Card"),
#     ]
#     id_type = models.CharField(
#         max_length=50,
#         choices=ID_TYPE_CHOICES,
#         null=True,
#         blank=True,
#         help_text="Type of ID proof provided by the farmer."
#     )
#     id_number = models.CharField(
#         max_length=100,
#         null=True,
#         blank=True,
#         help_text="The ID number corresponding to the selected ID type."
#     )
#     id_proof = models.FileField(
#         upload_to=farmer_media_path,
#         null=True,
#         blank=True,
#         help_text="PDF file containing both front and back sides of the ID card."
#     )

#     id_expiry_date = models.DateField(null=True, blank=True)

#     # Other media fields

#     # picture_of_tree = models.ImageField(upload_to=farmer_media_path,null=True, blank=True)

#     digital_signature = models.ImageField(upload_to=farmer_media_path, null=True, blank=True)
#     vaarha_document_id = models.IntegerField(null=True, blank=True)
#     vaarha_id = models.IntegerField(null=True, blank=True)
#     vaarha_doc_metadata = models.JSONField(null=True, blank=True)

#     # Timestamp
#     uploaded_at = models.DateTimeField(auto_now_add=True)

 

#     def __str__(self):
#         return f"Media for {self.farmer.first_name} {self.farmer.last_name}"
    
from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Farmer(models.Model):
    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        default='Male'
    )

    
    # Location information
    district = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    geo_tag = models.PointField()  # For storing the location coordinates
    
    
    # Creation metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="farmers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# models.py
from django.db import models
from django.contrib.gis.db import models as gis_models

class Farm(models.Model):
    # Relationship
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    
    # Basic farm information
    area_in_acres = models.FloatField()
    
    
    # Geography
    boundary = gis_models.PolygonField()  # For storing the farm boundary
    
    def __str__(self):
        return f"Farm of {self.farmer.first_name} {self.farmer.last_name}"

class Crop(models.Model):
    # Relationship
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    
    # Crop details
    crop_name = models.CharField(max_length=100)
    number_of_plants = models.PositiveIntegerField()
    area_in_acres = models.FloatField()
    sowing_date = models.DateField()
    
    def __str__(self):
        return f"{self.crop_name} in {self.farm}"