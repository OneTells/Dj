from django.contrib import admin
from django.urls import path

from DjangoProject.views import index, geography, demand, skills, vacancies

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path("geography", geography),
    path("demand", demand),
    path("skills", skills),
    path("vacancies", vacancies),
]
