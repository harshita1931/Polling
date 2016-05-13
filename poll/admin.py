from django.contrib import admin
from .models import MainTable, PreferenceTable

# Register your models here.

admin.site.register(MainTable)
admin.site.register(PreferenceTable)