from django.contrib import admin
from cryptoclient.models import *
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin


admin.site.register(userapp)


class EngineAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dropbox Information', {'fields':['app_key','app_secret','email']}),
        ('Special Information', {'fields':['user_name','pass_word','date']})
    ]
    list_display = ('app_key','app_secret','is_set','date')
    readonly_fields = ('date','is_set')

admin.site.register(engine,EngineAdmin)

'''
class AppuserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Information', {'fields':['space_allowed']}),
        ('Special Information', {'fields':['publib_key','sym_key_size','date']})
    ]
    list_display = ('space_allowed','date')
    readonly_fields = ('space_allowed','date')

admin.site.register(userapp,AppuserAdmin)
'''

class PilotAdmin(admin.ModelAdmin):
    fieldsets = [
        ('File Information', {'fields':['file_name','timestamp','size']}),
        ('Special Information', {'fields':['path','sym_key','iv']})
    ]
    list_display = ('file_name','timestamp','size')
    readonly_fields = ('sym_key','iv','path','size')

admin.site.register(pilot,PilotAdmin)

class LogAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Log Information', {'fields':['user','log_type','description','date']})
    ]
    list_display = ('log_type','description','date')
    readonly_fields = ('log_type','description','date')

admin.site.register(logs,LogAdmin)
