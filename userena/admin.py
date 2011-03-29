from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from userena.models import UserenaSignup
from userena.utils import get_profile_model

    
class UserenaUserProfileInline(admin.StackedInline):
    model = get_profile_model()
    verbose_name = "User Profile"
    can_delete = False
    max_num = 1

class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1

class UserenaAdmin(UserAdmin):
    def send_activation_email(self, request, queryset):
        "send initial activation mails for (manually) validated new users"
        for u in queryset:            
            u.userena_signup.send_activation_email()
            self.message_user(request, "Activation mail sent to %s" % u)
    send_activation_email.short_description = \
        "Send activation (approval) emails."
    
    inlines = [UserenaUserProfileInline, UserenaSignupInline, ]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'date_joined')
    actions = [ 'send_activation_email', ]
     

admin.site.unregister(User)
admin.site.register(User, UserenaAdmin)
#admin.site.register(get_profile_model())
