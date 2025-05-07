from django import forms
from .models import Announcement
from PIL import Image

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'start_date', 'end_date', 'image', 'chapel', 'praise']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
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
