from django.contrib import admin

# Register your models here.
from .models import TitleAkas, TitleBasics, TitleCrew, TitleEpisode, TitlePrincipals, TitleRatings, NameBasics

admin.site.register(TitleAkas)
admin.site.register(TitleBasics)
admin.site.register(TitleCrew)
admin.site.register(TitleEpisode)
admin.site.register(TitlePrincipals)
admin.site.register(TitleRatings)
admin.site.register(NameBasics)