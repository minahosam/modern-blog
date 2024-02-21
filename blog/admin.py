from django.contrib import admin
from .models import *

# Register your models here.
class postAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    

admin.site.register(Post,postAdmin)
admin.site.register(Tag)
admin.site.register(Subscripe)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)
