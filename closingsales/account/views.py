import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .tokens import account_activation_token
from .forms import SignUpForm
from .models import User


class SignupView(View):
    form_class = SignUpForm
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your ClosingSales Account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uuid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, 'contact@closingshops.de')
            return redirect('account_activation_sent')
        return render(request, self.template_name, {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class UserNameAvailableView(View):

    def post(self, request, *args, **kwargs):
        # TODO fix it later it is nice to have but not needed now.
        all_users = User.objects.where(username="helloworld")
        return JsonResponse({'foo': 'bar'})

class ActionActivationSentView(TemplateView):
    template_name = 'account/account_activation_sent.html'



class ActivateAccount(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64.encode()))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExit):
            uer = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('account-activation-invalid')

class AccountActivationInvalidView(TemplateView):
    template_name = 'account/account_activation_invalid.html'


class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'profile'

    def get_context_data(self, **kwargs):
        user = self.request.user
        ctx = super(ProfileView, self).get_context_data(**kwargs)
        ctx['user'] = user
        return ctx

    def get(self, request, *args, **kwargs):
        return render(request, 'account/profile.html')


class ChangePasswordView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'account/change_password.html', {'form': {}})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.sucess(request, 'Your password was sucessfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below')
        return render(request, 'account/change_password.html', {'form': form})
