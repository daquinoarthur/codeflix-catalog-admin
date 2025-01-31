from django.contrib import admin

from .models import CastMember


# Register your models here.
class CastMemberAdmin(admin.ModelAdmin): ...


admin.site.register(CastMember, CastMemberAdmin)
