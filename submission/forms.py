from django import forms
from .models import Announcement
from PIL import Image

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'start_date', 'end_date', 'image', 'chapel', 'praise']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'chapel': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500'
            }),
            'praise': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        chapel = cleaned_data.get('chapel')
        praise = cleaned_data.get('praise')
        image = cleaned_data.get('image')

        if not chapel and not praise:
            raise forms.ValidationError("You must select at least one: 'Chapel' or 'Praise'.")

        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("The image must be in JPG or PNG format.")

            try:
                img = Image.open(image)
                width, height = img.size
                required_width, required_height = 1920, 1080  # Example resolution
                aspect_ratio = required_width / required_height
                if not (width / height == aspect_ratio):
                    raise forms.ValidationError(
                        f"The image must have a resolution of {required_width}x{required_height} "
                        f"or a scaled version with the same aspect ratio."
                    )
            except Exception as e:
                raise forms.ValidationError("Invalid image file.")

        return cleaned_data
