from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import (
    User,Yatri,Country,
    Interest,
    SahayatriExpert,
    SahayatriGuide,
    Language,
    SOSRequest,
    PoliceStation,
)

class UserModelAdmin(BaseUserAdmin):


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','is_admin','type')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password','type')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    #this add_fields are displays teh feilds when creating the user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','type'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User,UserModelAdmin)
admin.site.register(Yatri)
admin.site.register(SahayatriGuide)
admin.site.register(SahayatriExpert)
admin.site.register(Country)
admin.site.register(Interest)
admin.site.register(Language)

admin.site.register(PoliceStation)
admin.site.register(SOSRequest)



