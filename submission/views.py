from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import AnnouncementForm
from .models import Announcement

class AnnouncementCreateView(CreateView):
    template_name = 'submission/submit.html'
    form_class = AnnouncementForm
    model = Announcement
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        messages.success(self.request, "Announcement created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please correct the errors below.")
        return super().form_invalid(form)

