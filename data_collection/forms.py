from django import forms
from django.contrib.gis.geos import Point, Polygon
from .models import Farmer, Farm

class FarmerForm(forms.ModelForm):
    # Regular form fields matching the model fields
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    
    class Meta:
        model = Farmer
        fields = [
            'first_name', 'last_name', 'mobile_number', 'gender',
            'district', 'village', 'pincode'
        ]
        widgets = {
            
            'gender': forms.Select(attrs={'class': 'form-select'}),
            
        }
    
    def clean_mobile_number(self):
        """Validate mobile number format"""
        mobile = self.cleaned_data.get('mobile_number')
        if mobile and not mobile.isdigit():
            raise forms.ValidationError("Mobile number should contain only digits")
        if mobile and len(mobile) != 10:
            raise forms.ValidationError("Mobile number should be 10 digits")
        return mobile

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Create a point from the latitude and longitude
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')
        if lat and lon:
            instance.geo_tag = Point(lon, lat)
        
        if commit:
            instance.save()
        return instance

from .models import Farm, Crop

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['area_in_acres']
        widgets = {
            'sowing_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_area_in_acres(self):
        """Validate that area is positive"""
        area = self.cleaned_data.get('area_in_acres')
        if area and area <= 0:
            raise forms.ValidationError("Area must be greater than zero")
        return area
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process boundary coordinates from the form data
        boundary_data = self.cleaned_data.get('boundary_coordinates')
        if boundary_data:
            try:
                # Parse the boundary data (assuming it's a JSON string of coordinate pairs)
                import json
                coordinates = json.loads(boundary_data)
                
                # Create a polygon from the coordinates
                # Format should be [[[lon1, lat1], [lon2, lat2], ..., [lon1, lat1]]]
                # Note: The first and last point must be the same to close the polygon
                if coordinates and coordinates[0] != coordinates[-1]:
                    coordinates.append(coordinates[0])  # Close the polygon if needed
                
                instance.boundary = Polygon(coordinates)
            except Exception as e:
                # Log the error but continue with saving
                print(f"Error processing boundary: {e}")
        
        if commit:
            instance.save()
        return instance
    
class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_name', 'number_of_plants', 'area_in_acres','sowing_date']
        widgets = {
            'sowing_date': forms.DateInput(attrs={'type': 'date'}),
        }