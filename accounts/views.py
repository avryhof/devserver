import bleach as bleach
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from accounts.forms import LoginForm


class LoginView(TemplateView):
    """Check authentication credentials provided by user and if they pass log in user."""

    page_title = "Log In"
    extra_css = ["css/login.css"]
    extra_javascript = []
    form = LoginForm
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = locals()
        context["page_title"] = self.page_title
        context["extra_css"] = self.extra_css
        context["extra_javascript"] = self.extra_javascript

        return context

    def get(self, request, *args, **kwargs):
        """PortalUser has not submitted yet, just requesting login page."""
        context = self.get_context_data()

        remembered_username = request.COOKIES.get("remembered_username")

        context["form"] = self.form(initial=dict(username=remembered_username))

        if "next" in request.GET:
            next_url = bleach.clean(request.GET["next"])
            request.session["next_url"] = next_url

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle user submission of login form from all web browser sources."""
        context = self.get_context_data()
        form = self.form(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_username = form.cleaned_data.get("remember_username")

            next_url = None
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                if "next" in request.GET:
                    next_url = bleach.clean(request.GET["next"])

                elif "next_url" in request.session:
                    next_url = request.session["next_url"]

                url = next_url
                request.session["next_url"] = None

                if not url:
                    url = "home"

                redirect_response = HttpResponseRedirect(resolve_url(url, *args, **kwargs))

                if remember_username:
                    redirect_response.set_cookie('remembered_username', username)

                return redirect_response

        context['form'] = form

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


@login_required
@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()

    # Redirect back to their previous page or the home page as default
    return redirect(request.META.get("HTTP_REFERER", "/"))
