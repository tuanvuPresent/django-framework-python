from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from apps.sample.book.models import Author, Book, TypeBook
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import UserChangeForm
from drf_yasg.generators import EndpointEnumerator
from apps.account.models import GroupApiPermission, UserApiPermission
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
User = get_user_model()


def get_all_api():
    endpoints = EndpointEnumerator().get_api_endpoints()
    data = []
    for endpoint in endpoints:
        method = endpoint[1].lower()
        action = endpoint[2].actions.get(method)
        class_name = endpoint[2].cls.__name__.lower()
        api_code = f'{class_name}.{action}'
        data.append((api_code, api_code + ' | ' + endpoint[0]))

    return data


class CustomUserChangeForm(UserChangeForm):
    api_code = forms.MultipleChoiceField(
        label='API Permission Code',
        widget=FilteredSelectMultiple('API Permission Code', is_stacked=False),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = UserApiPermission.objects.filter(user=self.instance).values_list('api_code', flat=True)
        self.fields['api_code'].choices = get_all_api()
        self.initial['api_code'] = list(initial)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user = user.save()
        UserApiPermission.objects.filter(user=user).delete()
        data_objs = []
        for api_code in self.cleaned_data['api_code']:
            data_objs.append(UserApiPermission(user=user, api_code=api_code))
        UserApiPermission.objects.bulk_create(data_objs)
        return user


class GroupForm(forms.ModelForm):
    api_code = forms.MultipleChoiceField(
        label='API Permission Code',
        widget=FilteredSelectMultiple('API Permission Code', is_stacked=False),
        required=False
    )

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = self.instance.groupapipermission_set.all().values_list('api_code', flat=True)
        self.fields['api_code'].choices = get_all_api()
        self.initial['api_code'] = list(initial)

    def save(self, commit=True):
        group = super().save(commit=commit)
        group.save()
        self.instance.groupapipermission_set.all().delete()
        data_objs = []
        for api_code in self.cleaned_data['api_code']:
            data_objs.append(GroupApiPermission(group=group, api_code=api_code))
        GroupApiPermission.objects.bulk_create(data_objs)
        return group


class CustomGroupAdmin(GroupAdmin):
    form = GroupForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'api_code'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(TypeBook)
admin.site.register(User)
