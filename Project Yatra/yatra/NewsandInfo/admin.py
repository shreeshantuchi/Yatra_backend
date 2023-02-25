from django.contrib import admin
from .models import News,Info,NewsImage,InfoImage

admin.site.register(News)
admin.site.register(Info)

admin.site.register(NewsImage)
admin.site.register(InfoImage)