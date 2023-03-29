from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.sample.book.models import Author, Book, TypeBook
from django import forms
from django.contrib import admin
from drf_yasg.generators import EndpointEnumerator
from apps.account.models import GroupApiPermission, UserApiPermission
User = get_user_model()


class UserApiPermissionForm(forms.ModelForm):
    api_code = forms.ChoiceField()

    class Meta:
        model = UserApiPermission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['api_code'].choices = self.get_all_api()

    def get_all_api(self):
        endpoints = EndpointEnumerator().get_api_endpoints()
        data = []
        for endpoint in endpoints:
            method = endpoint[1].lower()
            action = endpoint[2].actions.get(method)
            class_name = endpoint[2].cls.__name__.lower()
            api_code = f'{class_name}.{action}'
            data.append((api_code, api_code + ' | ' + endpoint[0]))

        return data


class GroupApiPermissionForm(forms.ModelForm):
    api_code = forms.ChoiceField()

    class Meta:
        model = GroupApiPermission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['api_code'].choices = self.get_all_api()

    def get_all_api(self):
        endpoints = EndpointEnumerator().get_api_endpoints()
        data = []
        for endpoint in endpoints:
            method = endpoint[1].lower()
            action = endpoint[2].actions.get(method)
            class_name = endpoint[2].cls.__name__.lower()
            api_code = f'{class_name}.{action}'
            data.append((api_code, api_code + ' | ' + endpoint[0]))

        return data


class UserApiPermissionAdmin(admin.ModelAdmin):
    model = UserApiPermission
    form = UserApiPermissionForm


class GroupApiPermissionAdmin(admin.ModelAdmin):
    model = GroupApiPermission
    form = GroupApiPermissionForm

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(TypeBook)
admin.site.register(User)
admin.site.register(GroupApiPermission, GroupApiPermissionAdmin)
admin.site.register(UserApiPermission, UserApiPermissionAdmin)
