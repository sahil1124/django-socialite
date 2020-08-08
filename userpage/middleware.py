from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        response=self.get_response(request)
        return response

    def process_view(self,request,view_func,view_args,view_kwargs):
        authenicated=request.user.is_authenticated
        url=request.path
        if(authenicated and url == settings.LOGIN_URL):
            logout(request)
            return

        if not authenicated and  (url !=settings.HOME_URL and url!=settings.LOGIN_URL and url!=settings.REGISTER_URL):
            return redirect(settings.LOGIN_URL)


        else:
            print("Anonymous User")
