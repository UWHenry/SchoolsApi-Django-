from django.contrib import admin
from django.apps import apps

# Get all models from all installed apps
all_models = apps.get_models()

# Register all models
for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass