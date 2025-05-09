# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from .forms import *
# from django.contrib.gis.geos import Point
# from django.contrib.gis.geos import GEOSGeometry
# from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test

# from django.http import JsonResponse
# def is_admin(user):
#     return user.is_staff
# @login_required
# def create_farmer(request):
#     if request.method == 'POST':
#         form = FarmerForm(request.POST, request.FILES)  # Include request.FILES
#         lat = request.POST.get('latitude')
#         lng = request.POST.get('longitude')

#         if form.is_valid() and lat and lng:
#             farmer = form.save(commit=False)
#             farmer.block_id = request.POST.get("block_id")  # Save the block_id
#             farmer.geo_tag = Point(float(lng), float(lat))
#             farmer.created_by = request.user  # Link the farmer to the current user
#             farmer.save()  # Save the farmer with the file

#             # Return a JSON response for AJAX
#             return JsonResponse({"success": True, "farmer_id": farmer.id})

#         else:
#             # Return errors as JSON
#             return JsonResponse({"success": False, "errors": form.errors})

#     else:
#         form = FarmerForm()

#     return render(request, 'data_collection/templates/create_farmer.html', {'form': form})

# from django.http import JsonResponse
# from django.shortcuts import render, get_object_or_404
# from django.contrib.gis.geos import GEOSGeometry
# from .models import Farmer, Farm
# from .forms import FarmForm

# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from PIL import Image
# import io

# def generate_pdf_from_image(image_file):
#     """ Convert an image file to a PDF and return the PDF file. """
#     image = Image.open(image_file)
#     pdf_bytes = io.BytesIO()
#     image.save(pdf_bytes, format="PDF")
#     pdf_bytes.seek(0)
#     return pdf_bytes

# import uuid
# import time
# def generate_unique_filename(base_name):
#     timestamp = int(time.time())  # Get current timestamp
#     unique_id = uuid.uuid4().hex[:6]  # Generate a short unique ID
#     return f"{base_name}_{timestamp}_{unique_id}.pdf"
#  # Ensure these functions exist

# @login_required
# def add_farm(request, farmer_id):
#     farmer = get_object_or_404(Farmer, id=farmer_id)
#     village_name = farmer.village  # Assuming 'village' is a field in Farmer model
#     base_name = f"{farmer.first_name}_{village_name}_Farm"

#     # Check for existing farm names and increment if necessary
#     existing_farms = Farm.objects.filter(farmer=farmer, farm_name__startswith=base_name)
#     farm_count = existing_farms.count() + 1  # Ensure uniqueness
#     default_farm_name = f"{base_name}_{farm_count}"  # Example: "John_Village_Farm_1"

#     if request.method == "POST":
#         form = FarmForm(request.POST, request.FILES)
#         boundary_geojson = request.POST.get("boundary", None)

#         if form.is_valid():
#             farm = form.save(commit=False)
#             farm.farmer = farmer

#             # ✅ Set farm name if the user didn't change it
#             farm.name = request.POST.get("farm_name", default_farm_name)

#             # ✅ Handle boundary conversion
#             if boundary_geojson:
#                 try:
#                     farm.boundary = GEOSGeometry(boundary_geojson)
#                 except Exception as e:
#                     return JsonResponse({"success": False, "errors": {"boundary": str(e)}})

#             # ✅ Process land ownership document (Convert image to PDF)
#             land_ownership_image = request.FILES.get("land_ownership")
#             if land_ownership_image:
#                 pdf_file = generate_pdf_from_image(land_ownership_image)  # Convert to PDF
#                 unique_filename = generate_unique_filename(f"{farmer_id}_land_ownership")
#                 pdf_path = f"land_documents/{unique_filename}"
#                 default_storage.save(pdf_path, ContentFile(pdf_file.read()))
#                 farm.land_ownership = pdf_path  # Store the file path

#             # ✅ Process landlord declaration (Convert image to PDF)
#             landlord_declaration_image = request.FILES.get("landlord_declaration")
#             if landlord_declaration_image:
#                 pdf_file = generate_pdf_from_image(landlord_declaration_image)  # Convert to PDF
#                 unique_filename = generate_unique_filename(f"{farmer_id}_landlord_declaration")
#                 pdf_path = f"farm_landlord_declarations/{unique_filename}"
#                 default_storage.save(pdf_path, ContentFile(pdf_file.read()))
#                 farm.landlord_declaration = pdf_path  # Store the file path

#             farm.save()
#             return JsonResponse({"success": True, "farm_id": farm.id})
#         else:
#             return JsonResponse({"success": False, "errors": form.errors})

#     return render(
#         request, 
#         "data_collection/templates/add_farm.html", 
#         {"form": FarmForm(initial={"farm_name": default_farm_name}), "farmer": farmer, "farmer_id": farmer.id, "default_farm_name": default_farm_name}
#     )





# # def add_plantation(request, farm_id):
# #     farm = get_object_or_404(Farm, id=farm_id)

# #     if request.method == "POST":
# #         form = PlantationForm(request.POST)
# #         boundary_geojson = request.POST.get("boundary")

# #         if form.is_valid() and boundary_geojson:
# #             plantation = form.save(commit=False)
# #             plantation.farm = farm
# #             plantation.boundary = GEOSGeometry(boundary_geojson)  # ✅ Convert GeoJSON to Polygon
# #             plantation.save()
# #             return JsonResponse({"success": True, "plantation_id": plantation.id})

# #         return JsonResponse({"success": False, "errors": form.errors}, status=400)

# #     else:
# #         form = PlantationForm()

# #     return render(request, "data_collection/templates/add_plantation.html", {"form": form, "farm": farm})
# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.contrib.gis.geos import GEOSGeometry
# from .models import Farmer, Farm, Plantation
# from .forms import PlantationForm
# import json

# @login_required
# def add_plantation(request, farmer_id):
#     farmer = get_object_or_404(Farmer, id=farmer_id)
#     farms = Farm.objects.filter(farmer=farmer)
    
#     if not farms.exists():
#         return JsonResponse({"success": False, "errors": "No farms available for this farmer."})

#     # ✅ Auto-select first farm
#     first_farm = farms.first()
#     first_farm_id = first_farm.id if first_farm else None
#     # ✅ Generate auto Kyari Name (farmer + farm + kyari + count)
#     base_kyari_name = f"{farmer.first_name}_Kyari"
#     existing_kyaris = Plantation.objects.filter(farm=first_farm, kyari_name__startswith=base_kyari_name)
#     kyari_count = existing_kyaris.count() + 1  # Ensure uniqueness
#     default_kyari_name = f"{base_kyari_name}_{kyari_count}"

#     if request.method == "POST":
#         print("DEBUG: Request POST Data:", request.POST)
#         form = PlantationForm(request.POST)
#         farm_id = request.POST.get("farm_id", first_farm.id)  # Default to first farm
#         boundary_geojson = request.POST.get("boundary")

#         if form.is_valid() and boundary_geojson:
#             plantation = form.save(commit=False)
#             plantation.farmer = farmer
#             plantation.farm = get_object_or_404(Farm, id=farm_id)

#             # ✅ Auto-set kyari_name if empty
#             plantation.kyari_name = request.POST.get("kyari_name", default_kyari_name)

#             # ✅ Parse and store GeoJSON boundary
#             try:
#                 geojson_obj = json.loads(boundary_geojson)
#                 geometry_json = json.dumps(geojson_obj['geometry']) if geojson_obj.get('type') == 'Feature' else boundary_geojson
#                 plantation.boundary = GEOSGeometry(geometry_json)
#                 plantation.save()
#                 return JsonResponse({"success": True, "plantation_id": plantation.id, "farmer_id": farmer_id})
#             except Exception as e:
#                 print(f"ERROR parsing GeoJSON: {str(e)}")
#                 return JsonResponse({"success": False, "errors": f"Invalid boundary format: {str(e)}"})
#         else:
#             return JsonResponse({"success": False, "errors": dict(form.errors)})

#     return render(
#         request, 
#         "data_collection/templates/add_plantation.html", 
#         {"form": PlantationForm(initial={"kyari_name": default_kyari_name}), "farms": farms, "farmer": farmer, "farmer_id": farmer.id, "default_kyari_name": default_kyari_name, "first_farm_id": first_farm_id}
#     )



# from django.db.models import Q
# from django.db.models import Count

# from django.db.models import Exists, OuterRef

# from django.db.models import Count
# @login_required
# def add_specie(request, farmer_id):
#     farmer = get_object_or_404(Farmer, id=farmer_id)

#     # Annotate the count of related species and filter plantations without species
#     plantations = Plantation.objects.filter(
#         farm__farmer=farmer
#     ).annotate(
#         species_count=Count('species')
#     ).filter(species_count=0)  # Only include plantations without species

#     first_plantation_id = plantations.first().id if plantations.exists() else None  # Get first plantation ID

#     if request.method == "POST":
#         form = SpecieForm(request.POST, request.FILES)
#         plantation_id = request.POST.get("plantation_id")

#         if form.is_valid() and plantation_id:
#             plantation = get_object_or_404(Plantation, id=plantation_id)

#             specie = form.save(commit=False)
#             specie.plantation = plantation
#             specie.save()
#             return JsonResponse({"success": True, "specie_id": specie.id, "message": "Species added successfully!", "farmer_id": farmer_id })
#         else:
#             errors = form.errors
#             if not plantation_id:
#                 errors['plantation_id'] = ['Please select a plantation']
#             return JsonResponse({"success": False, "errors": errors}, status=400)

#     else:
#         form = SpecieForm()

#     return render(
#         request,
#         "data_collection/templates/add_specie.html",
#         {
#             "form": form, 
#             "plantations": plantations, 
#             "farmer": farmer, 
#             "farmer_id": farmer_id, 
#             "first_plantation_id": first_plantation_id  # ✅ Pass first plantation ID
#         },
#     )

@login_required
def dashboard(request):
    return render(request, "data_collection/templates/dashboard.html") 


from django.shortcuts import render
from django.http import JsonResponse
from .models import Farmer, Farm

def get_farmers_list(request):
    search_query = request.GET.get("search", "").strip()  # Get search input
    farmers = Farmer.objects.filter(created_by=request.user)

    if search_query:
        farmers = farmers.filter(first_name__icontains=search_query)  # Case-insensitive search

    farmer_data = [
        {
            "id": farmer.id,
            "name": f"{farmer.first_name} {farmer.last_name}",
            "mobile": farmer.mobile_number,
            "village": farmer.village
        }
        for farmer in farmers
    ]

    return JsonResponse({"farmers": farmer_data})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def get_farmer_details(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farms = Farm.objects.filter(farmer=farmer)
   
    # species = Specie.objects.filter(plantation__in=plantations)
    # ✅ Ensure image URL is absolute (Fixes issue)
    
    farmer_data = {
        "id": farmer.id,
        "name": f"{farmer.first_name} {farmer.last_name}",
        "mobile": farmer.mobile_number,
        "gender": farmer.gender,
        "guardian": farmer.guardian_name,
        "village": farmer.village,
        "pincode": farmer.pincode,
        "farmer_consent": farmer.farmer_consent,
        "geo_tag": {
            "type": "Point",
            "coordinates": [farmer.geo_tag.x, farmer.geo_tag.y]
        }
    }

    farm_data = [
        {
            "id": farm.id,
            "farm_name": farm.farm_name,
            "area": farm.area_in_acres,
            "ownership": farm.ownership,
            "boundary_method": farm.boundary_method,
            "boundary": {
                "type": "Polygon",
                "coordinates": [[list(reversed(coord)) for coord in farm.boundary.coords[0]]] 
            }
        }
        for farm in farms
    ]


    

    # specie_data = [
    #     {
    #         "id": specie.id,
    #         "plantation_id": specie.plantation.id,
    #         "specie_name": specie.specie_name,
    #         "number_of_plants": specie.number_of_plants,
    #         "plant_spacing": specie.plant_spacing
    #     }
    #     for specie in species
    # ]

    return JsonResponse({
        "farmer": farmer_data,
        "farms": farm_data,
        
        # "species": specie_data
    })

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.contrib.gis.geos import GEOSGeometry
# from .models import Farmer, Farm

# def get_farms_for_farmer(request, farmer_id):
#     """Return a list of farms for the given farmer with valid GeoJSON boundary."""
#     farmer = get_object_or_404(Farmer, id=farmer_id)
#     farms = Farm.objects.filter(farmer=farmer)

#     farm_data = [
#         {
#             "id": farm.id,
#             "farm_name": farm.farm_name,
#             "boundary": GEOSGeometry(farm.boundary).geojson  # ✅ Convert to GeoJSON format
#         }
#         for farm in farms
#     ]

#     return JsonResponse({"farms": farm_data})

# def get_plantations_for_farm(request, farm_id):
#     """Return all plantations for the given farm with their GeoJSON boundaries."""
#     farm = get_object_or_404(Farm, id=farm_id)
#     plantations = Plantation.objects.filter(farm=farm)
    
#     plantation_data = [
#         {
#             "id": plantation.id,
#             "kyari_name": plantation.kyari_name,
#             "area_in_acres": plantation.area_in_acres,
#             "year": plantation.plantation_year,
#             "kyari_type": plantation.kyari_type,
#             "boundary": GEOSGeometry(plantation.boundary).geojson  # Convert to GeoJSON format
#         }
#         for plantation in plantations
#     ]
    
#     # Also return the farm boundary for validation
#     farm_boundary = GEOSGeometry(farm.boundary).geojson
    
#     return JsonResponse({
#         "plantations": plantation_data,
#         "farm_boundary": farm_boundary
#     })

# # from django.core.files.base import ContentFile
# # import base64

# # def upload_media(request, farmer_id):
# #     farmer = get_object_or_404(Farmer, id=farmer_id)

# #     if request.method == "POST":
# #         try:
# #             # Create a new FarmerMedia instance
# #             media = FarmerMedia(farmer=farmer)

# #             # Handle file uploads
# #             if "picture" in request.FILES:
# #                 media.picture = request.FILES["picture"]
# #             if "photo_of_english_epic" in request.FILES:
# #                 media.photo_of_english_epic = request.FILES["photo_of_english_epic"]
# #             if "photo_of_regional_language_epic" in request.FILES:
# #                 media.photo_of_regional_language_epic = request.FILES["photo_of_regional_language_epic"]
# #             if "id_proof_front" in request.FILES:
# #                 media.id_proof_front = request.FILES["id_proof_front"]
# #             if "id_proof_back" in request.FILES:
# #                 media.id_proof_back = request.FILES["id_proof_back"]
# #             if "land_ownership" in request.FILES:
# #                 media.land_ownership = request.FILES["land_ownership"]
# #             if "picture_of_tree" in request.FILES:
# #                 media.picture_of_tree = request.FILES["picture_of_tree"]

# #             # Handle digital signature (base64 string from canvas)
# #             signature_data = request.POST.get("digital_signature")
# #             if signature_data and ';base64,' in signature_data:
# #                 format, imgstr = signature_data.split(';base64,')
# #                 ext = format.split('/')[-1]
# #                 signature_file = ContentFile(base64.b64decode(imgstr), name=f"signature_{farmer.id}.{ext}")
# #                 media.digital_signature.save(f"signature_{farmer.id}.{ext}", signature_file, save=False)

# #             # Save the media instance
# #             media.save()
            
# #             print("Successfully uploaded farmer media!")
# #             return JsonResponse({
# #                 "success": True,
# #                 "message": "Farmer media uploaded successfully!",
# #                 "farmer_id": farmer_id
# #             })
# #         except Exception as e:
# #             import traceback
# #             print(f"Error uploading media: {str(e)}")
# #             print(traceback.format_exc())
# #             return JsonResponse({
# #                 "success": False, 
# #                 "errors": str(e)
# #             }, status=400)
    
# #     return render(request, "data_collection/templates/farmer_media.html", {"farmer": farmer, "farmer_id": farmer.id})



# from django.http import JsonResponse
# from django.core.files.base import ContentFile
# import base64
# from PIL import Image
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from .models import FarmerMedia
# from io import BytesIO
# from PIL import Image
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import tempfile
# from io import BytesIO
# from PIL import Image
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import tempfile
# import os
# from django.core.files.base import ContentFile
# from django.http import JsonResponse
# from django.shortcuts import render, get_object_or_404

# def optimize_image(image_file, max_size=(1200, 1200), quality=85):
#     """
#     Resizes and optimizes an image to reduce file size.
#     Returns a BytesIO object containing the optimized image.
#     """
#     # Open the image
#     img = Image.open(image_file)
    
#     # Convert image to RGB if it's not (handles RGBA and other formats)
#     if img.mode != 'RGB':
#         img = img.convert('RGB')
    
#     # Resize the image while maintaining aspect ratio
#     img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
#     # Create a BytesIO object to store the optimized image
#     optimized = BytesIO()
    
#     # Save the image with reduced quality
#     img.save(optimized, format='JPEG', quality=quality, optimize=True)
    
#     # Reset the buffer position
#     optimized.seek(0)
    
#     return optimized

# def generate_pdf_from_image(image):
#     """
#     Creates a PDF from a single image.
#     Returns a BytesIO object containing the PDF data.
#     """
#     # Create a BytesIO buffer to store the PDF
#     pdf_buffer = BytesIO()

#     # Create a PDF canvas
#     c = canvas.Canvas(pdf_buffer, pagesize=letter)
#     width, height = letter  # Width and height of the PDF page
    
#     try:
#         # Optimize the image first
#         optimized_image = optimize_image(image)
        
#         # Open the optimized image
#         img = Image.open(optimized_image)
#         img_width, img_height = img.size
#         aspect_ratio = img_height / img_width

#         # Calculate new dimensions while maintaining aspect ratio
#         max_width = width * 0.9
#         max_height = height * 0.9
        
#         new_width = min(max_width, img_width)
#         new_height = new_width * aspect_ratio

#         if new_height > max_height:
#             new_height = max_height
#             new_width = new_height / aspect_ratio

#         # Save the image to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
#             temp_filename = temp_file.name
#             img.save(temp_filename, format="JPEG", quality=85)

#         # Draw the image onto the PDF using the temporary file path
#         c.drawImage(
#             temp_filename,
#             30, height - 30 - new_height,
#             width=new_width,
#             height=new_height
#         )
        
#         # Delete the temporary file after drawing
#         os.unlink(temp_filename)
        
#     except Exception as e:
#         # Log the error for debugging
#         import logging
#         logging.error(f"Error processing image: {str(e)}")
#         raise

#     # Save the PDF
#     c.save()

#     # Move the buffer pointer to the beginning
#     pdf_buffer.seek(0)
#     return pdf_buffer

# def generate_pdf_from_images(front_image, back_image):
#     """
#     Combines two images (front and back) into a single PDF file.
#     Returns a BytesIO object containing the PDF data.
#     Handles both InMemoryUploadedFile and TemporaryUploadedFile.
#     """
#     # Create a BytesIO buffer to store the PDF
#     pdf_buffer = BytesIO()

#     # Create a PDF canvas
#     c = canvas.Canvas(pdf_buffer, pagesize=letter)
#     width, height = letter  # Width and height of the PDF page

#     # Helper function to add an image to the PDF
#     def add_image_to_pdf(image, x, y, max_width, max_height):
#         try:
#             # Optimize the image first
#             optimized_image = optimize_image(image)
            
#             # Open the optimized image
#             img = Image.open(optimized_image)
#             img_width, img_height = img.size
#             aspect_ratio = img_height / img_width

#             # Calculate new dimensions while maintaining aspect ratio
#             new_width = min(max_width, img_width)
#             new_height = new_width * aspect_ratio

#             if new_height > max_height:
#                 new_height = max_height
#                 new_width = new_height / aspect_ratio

#             # Save the image to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
#                 temp_filename = temp_file.name
#                 img.save(temp_filename, format="JPEG", quality=85)

#             # Draw the image onto the PDF using the temporary file path
#             c.drawImage(
#                 temp_filename,
#                 x, y - new_height,
#                 width=new_width,
#                 height=new_height
#             )
            
#             # Delete the temporary file after drawing
#             os.unlink(temp_filename)
            
#         except Exception as e:
#             # Log the error for debugging
#             import logging
#             logging.error(f"Error processing image: {str(e)}")
#             raise

#     # Add the front image to the first page
#     if front_image:
#         add_image_to_pdf(front_image, 30, height - 30, width * 0.9, height * 0.9)

#     # Add the back image to the second page
#     if back_image:
#         c.showPage()  # Start a new page
#         add_image_to_pdf(back_image, 30, height - 30, width * 0.9, height * 0.9)

#     # Save the PDF
#     c.save()

#     # Move the buffer pointer to the beginning
#     pdf_buffer.seek(0)
#     return pdf_buffer

# @login_required
# def upload_media(request, farmer_id):
#     farmer = get_object_or_404(Farmer, id=farmer_id)
#     if farmer.media.exists():
#         return render(request, "data_collection/templates/farmer_media.html", {
#             "farmer": farmer,
#             "farmer_id": farmer.id,
#             "error": "Media already uploaded for this farmer."
#         })

#     if request.method == "POST":
#         try:
#             # Create a new FarmerMedia instance
#             media = FarmerMedia(farmer=farmer)

#             # Process and optimize profile picture
#             if "picture" in request.FILES:
#                 optimized = (request.FILES["picture"])
#                 media.picture.save(f"picture_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
#             # Handle English EPIC
#             if "photo_of_english_epic" in request.FILES:
#                 english_epic = request.FILES["photo_of_english_epic"]
#                 # Create both optimized image and PDF version
#                 optimized = (english_epic)
#                 # media.photo_of_english_epic.save(f"epic_en_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
#                 # Generate PDF for English EPIC
#                 english_epic.seek(0)  # Reset file pointer
#                 pdf_buffer = generate_pdf_from_image(english_epic)
#                 media.photo_of_english_epic.save(f"epic_en_{farmer.id}.pdf", ContentFile(pdf_buffer.read()), save=False)
                
#             # Handle Regional EPIC
#             if "photo_of_regional_language_epic" in request.FILES:
#                 regional_epic = request.FILES["photo_of_regional_language_epic"]
#                 # Create both optimized image and PDF version
#                 optimized = (regional_epic)
#                 # media.photo_of_regional_language_epic.save(f"epic_reg_{farmer.id}.jpg", ContentFile(optimized.read()), save=False)
                
#                 # Generate PDF for Regional EPIC
#                 regional_epic.seek(0)  # Reset file pointer
#                 pdf_buffer = generate_pdf_from_image(regional_epic)
#                 media.photo_of_regional_language_epic.save(f"epic_reg_{farmer.id}.pdf", ContentFile(pdf_buffer.read()), save=False)
                
#             # Handle Land Ownership document
            

#             # Handle ID proof generation
#             front_image = request.FILES.get("id_proof_front")
#             back_image = request.FILES.get("id_proof_back")
#             if front_image and back_image:
#                 # Generate PDF from the uploaded images
#                 pdf_buffer = generate_pdf_from_images(front_image, back_image)
#                 pdf_file = ContentFile(pdf_buffer.read(), name=f"id_proof_{farmer.id}.pdf")

#                 # Save the PDF to the media model
#                 media.id_proof.save(f"id_proof_{farmer.id}.pdf", pdf_file, save=False)

#             id_type = request.POST.get("id_type")
#             print("ID Type:",id_type)
#             id_number = request.POST.get("id_number")
#             id_expiry_date = request.POST.get("id_expiry_date")  # Optional field

#             if id_type:
#                 media.id_type = id_type
#             if id_number:
#                 media.id_number = id_number
#             if id_expiry_date and id_type == "driving_licence":  # Only process expiry date for Driving License
#                 media.id_expiry_date = id_expiry_date

#             # Handle digital signature (base64 string from canvas)
#             signature_data = request.POST.get("digital_signature")
#             if signature_data and ';base64,' in signature_data:
#                 format, imgstr = signature_data.split(';base64,')
#                 ext = format.split('/')[-1]
#                 signature_file = ContentFile(base64.b64decode(imgstr), name=f"signature_{farmer.id}.{ext}")
#                 media.digital_signature.save(f"signature_{farmer.id}.{ext}", signature_file, save=False)

#             # Save the media instance
#             media.save()

#             return JsonResponse({
#                 "success": True,
#                 "message": "Farmer media uploaded successfully!",
#                 "farmer_id": farmer_id
#             })

#         except Exception as e:
#             import traceback
#             print(f"Error uploading media: {str(e)}")
#             print(traceback.format_exc())
#             return JsonResponse({
#                 "success": False, 
#                 "errors": str(e)
#             }, status=400)

#     return render(request, "data_collection/templates/farmer_media.html", {"farmer": farmer, "farmer_id": farmer.id})



# views.py
import os
import requests
from django.http import HttpResponse
from django.conf import settings

def proxy_google_tiles(request, layer, z, x, y):
    """
    Proxy Google Maps tile requests through Django backend
    """
    # Get API key from settings
    api_key = os.getenv('GOOGLE_API_KEY')
    
    # Choose a random subdomain
    import random
    subdomain = random.choice(['mt0', 'mt1', 'mt2', 'mt3'])
    
    # Construct the URL
    url = f"https://{subdomain}.google.com/vt/lyrs={layer}&x={x}&y={y}&z={z}&key={api_key}"
    
    try:
        # Get the tile from Google
        response = requests.get(url, stream=True)
        
        # Check if request was successful
        if response.status_code == 200:
            # Create Django response with same content type
            django_response = HttpResponse(
                content=response.content,
                content_type=response.headers['Content-Type'],
                status=response.status_code
            )
            
            # Add caching headers
            django_response['Cache-Control'] = 'public, max-age=86400'  # Cache for one day
            
            return django_response
        else:
            return HttpResponse(status=response.status_code)
            
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Tile proxy error: {str(e)}")
        return HttpResponse(status=500)
    

# # views.py

# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test

# # Helper function to check if the user is an admin
# def is_admin(user):
#     return user.is_staff

# # Admin dashboard view

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
# from .forms import CustomUserCreationForm

# # Helper function to check if the user is an admin
# def is_admin(user):
#     return user.is_staff

# # Admin dashboard view
# @login_required
# @user_passes_test(is_admin)  # Only admins can access this view
# def admin_dashboard(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')
#     else:
#         form = CustomUserCreationForm()

#     users = User.objects.all()  # List all users
#     return render(request, 'data_collection/templates/admin_dashboard.html', {'form': form, 'users': users})
# # @login_required
# # @user_passes_test(is_admin)  # Only admins can access this view
# # def admin_dashboard(request):
# #     if request.method == 'POST':
# #         form = UserCreationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             user.is_staff = False  # Ensure the user is not an admin
# #             user.save()
# #             return redirect('admin_dashboard')
# #     else:
# #         form = UserCreationForm()

# #     users = User.objects.all()  # List all users
# #     return render(request, 'data_collection/templates/admin_dashboard.html', {'form': form, 'users': users})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.gis.geos import Point, Polygon
from django.views.decorators.http import require_http_methods
import json

from .models import Farmer, Farm
from .forms import FarmerForm, FarmForm

@login_required
def farmer_list(request):
    """View to list all farmers created by the current user"""
    farmers = Farmer.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'data_collection/farmer_list.html', {'farmers': farmers})

@login_required
def create_farmer(request):
    """View to create a new farmer"""
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            farmer = form.save(commit=False)
            
            # Set the creator
            farmer.created_by = request.user
            
            # Process location data
            lat = form.cleaned_data.get('latitude')
            lon = form.cleaned_data.get('longitude')
            if lat and lon:
                farmer.geo_tag = Point(lon, lat)
            
            farmer.save()
            
            # Handle AJAX requests (for mobile app or SPA)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'farmer_id': farmer.id})
            
            # For regular form submissions, redirect to add farm
            return redirect('add_farm', farmer_id=farmer.id)
        else:
            # If the form is invalid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = FarmerForm()
    
    return render(request, 'data_collection/templates/create_farmer.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
import json

from .models import Farmer, Farm
from .forms import FarmForm

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
import json

from .models import Farmer, Farm, Crop
from .forms import FarmForm, CropForm

@login_required
def add_farm(request, farmer_id):
    """View to add a farm for a specific farmer"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    # Check if the logged-in user created this farmer
    if farmer.created_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        farm_form = FarmForm(request.POST)
        
        # Get crop data from POST
        crop_data = []
        i = 0
        while f'crop_name_{i}' in request.POST:
            if request.POST.get(f'crop_name_{i}'):  # Only add if name is provided
                crop_data.append({
                    'crop_name': request.POST.get(f'crop_name_{i}'),
                    'number_of_plants': request.POST.get(f'number_of_plants_{i}', 0),
                    'area_in_acres': request.POST.get(f'crop_area_{i}', 0),
                    'sowing_date': request.POST.get(f'crop_sowing_date_{i}')  #
                })
            i += 1
        
        if farm_form.is_valid() and crop_data:  # Ensure we have at least one crop
            farm = farm_form.save(commit=False)
            farm.farmer = farmer
            
            # Process boundary data
            boundary_data = request.POST.get('boundary_coordinates')
            if boundary_data:
                try:
                    # Parse the JSON data
                    geo_json = json.loads(boundary_data)
                    
                    # Handle different GeoJSON structures
                    if 'type' in geo_json:
                        if geo_json['type'] == 'Feature':
                            # This is a GeoJSON Feature - extract the geometry
                            geometry_json = json.dumps(geo_json['geometry'])
                        else:
                            # This is already a GeoJSON geometry
                            geometry_json = json.dumps(geo_json)
                    else:
                        # Try to use it directly
                        geometry_json = json.dumps(geo_json)
                    
                    # Create a GEOSGeometry object from the GeoJSON
                    farm.boundary = GEOSGeometry(geometry_json)
                    
                except Exception as e:
                    import traceback
                    print(f"Error processing boundary: {e}")
                    print(f"Boundary data: {boundary_data}")
                    print(traceback.format_exc())
                    return JsonResponse({
                        'success': False, 
                        'errors': f"Could not process boundary: {str(e)}"
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': "Boundary data is required"
                })
            
            try:
                # Save farm
                farm.save()
                
                # Save crops
                for crop_item in crop_data:
                    Crop.objects.create(
                        farm=farm,
                        crop_name=crop_item['crop_name'],
                        number_of_plants=crop_item['number_of_plants'],
                        area_in_acres=crop_item['area_in_acres'],
                        sowing_date=crop_item['sowing_date']
                    )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'farm_id': farm.id, 'farmer_id': farmer.id})
                
                return redirect('farm_details', farm_id=farm.id)
            except Exception as e:
                import traceback
                print(f"Error saving farm: {e}")
                print(traceback.format_exc())
                return JsonResponse({
                    'success': False,
                    'errors': f"Error saving farm: {str(e)}"
                })
        else:
            errors = farm_form.errors
            if not crop_data:
                errors['crops'] = ['At least one crop must be added']
                
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
    else:
        farm_form = FarmForm()
    
    return render(request, 'data_collection/templates/add_farm.html', {
        'form': farm_form, 
        'farmer': farmer,
        'crop_form': CropForm()  # Pass an empty crop form for the template
    })

@login_required
def farm_details(request, farm_id):
    """View farm details"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    # Check if the logged-in user created the farmer associated with this farm
    if farm.farmer.created_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    return render(request, 'data_collection/farm_details.html', {'farm': farm})

@login_required
def farmer_details(request, farmer_id):
    """View farmer details and associated farms"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    # Check if the logged-in user created this farmer
    if farmer.created_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    farms = Farm.objects.filter(farmer=farmer)
    
    return render(request, 'data_collection/farmer_details.html', {
        'farmer': farmer,
        'farms': farms
    })

@login_required
@require_http_methods(["DELETE"])
def delete_farmer(request, farmer_id):
    """Delete a farmer"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    # Check if the logged-in user created this farmer
    if farmer.created_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    farmer.delete()
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["DELETE"])
def delete_farm(request, farm_id):
    """Delete a farm"""
    farm = get_object_or_404(Farm, id=farm_id)
    
    # Check if the logged-in user created the farmer associated with this farm
    if farm.farmer.created_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    farm.delete()
    return JsonResponse({'success': True})

# API endpoints for mobile app or frontend frameworks
@login_required
def api_farmers(request):
    """API endpoint to get all farmers created by the current user"""
    farmers = Farmer.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Convert to JSON-serializable format
    farmers_data = []
    for farmer in farmers:
        farmers_data.append({
            'id': farmer.id,
            'name': f"{farmer.first_name} {farmer.last_name}",
            'mobile': farmer.mobile_number,
            'village': farmer.village,
            'district': farmer.district,
            'created_at': farmer.created_at.isoformat()
        })
    
    return JsonResponse({'farmers': farmers_data})

@login_required
def api_farms(request, farmer_id=None):
    """API endpoint to get farms, optionally filtered by farmer"""
    if farmer_id:
        farmer = get_object_or_404(Farmer, id=farmer_id)
        # Check if the logged-in user created this farmer
        if farmer.created_by != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        farms = Farm.objects.filter(farmer=farmer)
    else:
        # Get all farms for all farmers created by this user
        farms = Farm.objects.filter(farmer__created_by=request.user)
    
    # Convert to JSON-serializable format
    farms_data = []
    for farm in farms:
        farms_data.append({
            'id': farm.id,
            'name': farm.farm_name,
            'farmer_id': farm.farmer.id,
            'farmer_name': f"{farm.farmer.first_name} {farm.farmer.last_name}",
            'area': farm.area_in_acres,
            'plant_name': farm.plant_name,
            'sowing_date': farm.sowing_date.isoformat()
        })
    
    return JsonResponse({'farms': farms_data})


# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.gis.geos import GEOSGeometry
from .models import Farmer, Farm, Crop

def dashboard(request):
    """
    Main dashboard view showing the map and farmer search interface
    """
    farmer_count = Farmer.objects.count()
    farm_count = Farm.objects.count()
    total_area = Farm.objects.aggregate(total=Sum('area_in_acres'))['total'] or 0
    
    context = {
        'farmer_count': farmer_count,
        'farm_count': farm_count,
        'total_area': round(total_area, 2),
    }
    return render(request, 'data_collection/templates/dashboard.html', context)

def dashboard_farmers(request):
    """
    API endpoint that returns farmers list, optionally filtered by search query
    """
    search_query = request.GET.get('search', '')
    
    if search_query:
        farmers = Farmer.objects.filter(
            first_name__icontains=search_query
        ) | Farmer.objects.filter(
            last_name__icontains=search_query
        ) | Farmer.objects.filter(
            mobile_number__icontains=search_query
        )
    else:
        farmers = Farmer.objects.all()
    
    farmers_data = []
    for farmer in farmers:
        farmers_data.append({
            'id': farmer.id,
            'name': f"{farmer.first_name} {farmer.last_name}",
            'village': farmer.village,
            'mobile': farmer.mobile_number,
        })
    
    return JsonResponse({'farmers': farmers_data})

def dashboard_farmer_data(request, farmer_id):
    """
    API endpoint that returns detailed data for a specific farmer
    """
    try:
        farmer = Farmer.objects.get(id=farmer_id)
        
        # Get farmer data
        farmer_data = {
            'id': farmer.id,
            'name': f"{farmer.first_name} {farmer.last_name}",
            'village': farmer.village,
            'district': farmer.district,
            'mobile': farmer.mobile_number,
            'gender': farmer.gender,
            'geo_tag': {
                'type': 'Point',
                'coordinates': [farmer.geo_tag.x, farmer.geo_tag.y]  # Convert to [longitude, latitude]
            }
        }
        
        # Get farms data
        farms_data = []
        for farm in Farm.objects.filter(farmer=farmer):
            # Convert the boundary to a format suitable for Leaflet
            boundary_coords = []
            for point in farm.boundary[0]:  # Assuming simple polygons
                boundary_coords.append([point[1], point[0]])  # Swap to [latitude, longitude] for Leaflet
            
            farms_data.append({
                'id': farm.id,
                'farm_name': f"Farm {farm.id}",  # Using ID as name if you don't have farm_name
                'area': farm.area_in_acres,
                'boundary': {
                    'type': 'Polygon',
                    'coordinates': boundary_coords
                }
            })
        
        # Get crop data grouped by name
        crops = Crop.objects.filter(farm__farmer=farmer)
        species_data = []
        species_dict = {}
        
        for crop in crops:
            if crop.crop_name in species_dict:
                species_dict[crop.crop_name]['number_of_plants'] += crop.number_of_plants
            else:
                species_dict[crop.crop_name] = {
                    'specie_name': crop.crop_name,
                    'number_of_plants': crop.number_of_plants
                }
        
        for specie in species_dict.values():
            species_data.append(specie)
        
        # Since you don't have plantations in your model, we'll return an empty list
        plantations_data = []
        
        return JsonResponse({
            'farmer': farmer_data,
            'farms': farms_data,
            'plantations': plantations_data,
            'species': species_data
        })
    
    except Farmer.DoesNotExist:
        return JsonResponse({'error': 'Farmer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)