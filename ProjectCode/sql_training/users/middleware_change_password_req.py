from .models import Profile
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from datetime import timedelta


class ChangePasswordCheck:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("process_request called")
        user = request.user
        path = request.path_info
        print(path)
        path = path.replace("/", "")
        print(path)
        EXEMPT_URLS = [
            r'logout',
            r'change_password',
        ]
        if request.user.is_authenticated:
            if path not in EXEMPT_URLS:
                try:
                    if user:
                        profile = Profile.objects.get(user=request.user)
                        if profile:
                            print(profile.password_changed)
                            timeToExpire = timedelta(seconds=60)
                            LastPassword_Changed = profile.password_changed
                            now_timestamp = timezone.now()

                            print(now_timestamp > LastPassword_Changed + timeToExpire)
                            if now_timestamp > LastPassword_Changed + timeToExpire:
                                messages.success(request,
                                                 f'Please Change the password the time for this password expired')
                                return redirect('change_password')

                            print("timeToExpire: {} , now timestamp: {} , LastPassword Changed: {}".format(timeToExpire,
                                                                                                           now_timestamp,
                                                                                                           LastPassword_Changed))
                except Exception as e:
                    print(e)
