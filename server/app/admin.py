from django.contrib import admin
from django import forms
from .models import Forest, FunderUser, User, OwnerUser, AuthUser, Region
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# class UserAdmin(BaseUserAdmin):
#     add_form = UserCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')}
#         ),
#     )
class CustomUserChangeForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'password', 'user_type')
    def clean_password(self):
        return self.initial["password"]

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        print("asdfasd")
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'user_type',)

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'username', 'password', 'user_type')
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('user_type',),
        }),
    )

# admin.site.register(User, CustomUserAdmin)
admin.site.register(Forest)
admin.site.register(FunderUser)
admin.site.register(OwnerUser)
admin.site.register(AuthUser)
admin.site.register(Region)
admin.site.register(User, UserAdmin)

# Register your models here.
