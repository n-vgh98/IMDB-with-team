from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.models import User
from users.forms import CustomUserCreationForm


class SignUpViews(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('login')

