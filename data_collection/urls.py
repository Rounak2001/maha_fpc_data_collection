from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .postapi import *
from .vaarha_api import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    # path('', create_farmer, name='create_farmer'),
    # path('add_farm/<int:farmer_id>/', add_farm, name='add_farm'),
    # path("api/farms/<int:farmer_id>/", get_farms_for_farmer, name="get_farms"),
    # path('add-plantation/<int:farmer_id>/', add_plantation, name='add_plantation'),
    # path('add-species/<int:farmer_id>/', add_specie, name='add_specie'),
    # path("dashboard-data/<int:farmer_id>/", get_farmer_details, name="dashboard_data"),
    # path("dashboard-farmers/", get_farmers_list, name="dashboard_farmers"),
    path('dashboard/', dashboard, name='dashboard'),
    # path('get-plantations/<int:farm_id>/', get_plantations_for_farm, name='get_plantations_for_farm'),
    #path("upload-media/<int:farmer_id>/", upload_media, name="upload_media"),
    # path("dashboard-second/", dashboard_2, name="dashboard_2"),
    # path("api/sync-status/", get_sync_status, name="get_sync_status"),
    # path("api/push-all-data/", push_all_data_to_vaarha, name="push_all_data_to_vaarha"),



    #POST API 
    # path('send-farmer/<int:farmer_id>/', send_farmer_data, name='send_farmer_data'),
    # path('send-farm/<int:farm_id>/',send_farm_data, name = "send_farm"),
    # path('send-plantation/<int:plantation_id>/',send_plantation_data, name = "send_plantation_data"),
    # path('send-species/<int:specie_id>/', send_specie_data, name = "send_species_data"),
    #Get API call from Vaarha
    path("api/states/", get_states, name="get_states"),
    path("api/districts/<int:state_id>/",get_districts, name="get_districts"),
    path("api/blocks/<int:district_id>/",get_blocks, name="get_blocks"),
    path("api/plantation/species/all/", get_species, name="get_species"),
    path('farmerlist', farmer_list, name='farmer_list'),
    path('', create_farmer, name='create_farmer'),
    path('farmer/<int:farmer_id>/', farmer_details, name='farmer_details'),
    path('farmer/<int:farmer_id>/delete/', delete_farmer, name='delete_farmer'),
    path('add_farm/<int:farmer_id>/', add_farm, name='add_farm'),
    path('farm/<int:farm_id>/', farm_details, name='farm_details'),
    path('farm/<int:farm_id>/delete/', delete_farm, name='delete_farm'),
    path('dashboard-farmers/', dashboard_farmers, name='dashboard_farmers'),
    path('dashboard-data/<int:farmer_id>/', dashboard_farmer_data, name='dashboard_farmer_data'),
    
    # API endpoints
    path('api/farmers/', api_farmers, name='api_farmers'),
    path('api/farms/', api_farms, name='api_farms'),
    path('api/farmer/<int:farmer_id>/farms/', api_farms, name='api_farmer_farms'),




    re_path(r'^tiles/(?P<layer>[a-z])/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)$', proxy_google_tiles, name='proxy_google_tiles'),
]
# Compare this snippet from KMcollect/data_collection/views.py: 

if settings.DEBUG:  # Serve static and media files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)