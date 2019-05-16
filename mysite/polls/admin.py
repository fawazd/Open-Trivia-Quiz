from django.contrib import admin

from .models import Tournament

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')

admin.site.register(Tournament, TournamentAdmin)