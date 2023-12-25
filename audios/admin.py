from django.contrib import admin

from .models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display =  ('title', 'shiekh',) 


class AudioEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'book',)
    list_filter = ('book',)
    



admin.site.register(Shiekh)
admin.site.register(Book, BookAdmin)
admin.site.register(AudioEpisode, AudioEpisodeAdmin)
admin.site.register(Logo)
admin.site.register(bukMosque)
