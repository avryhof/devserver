import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from music.forms import SongSearchForm, PlaylistForm
from utilities.helper_functions import join_url, path_explode


class HomeView(TemplateView):
    template_name = "home.html"
    extra_css = []
    extra_javascript = []
    name = "Home"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["page_title"] = self.name
        context["extra_css"] = self.extra_css
        context["extra_javascript"] = self.extra_javascript
        context["request"] = self.request

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['form'] = SongSearchForm()
        context['results'] = False

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = SongSearchForm(request.POST)
        results = False

        if form.is_valid():
            search_data = dict(format="json")
            for sk in list(form.cleaned_data.keys()):
                if sk == "search":
                    key = sk
                else:
                    key = "%s__icontains" % sk

                if form.cleaned_data.get(sk):
                    search_data.update({key: form.cleaned_data.get(sk)})

                url_path = path_explode(reverse("find_song"))
                search_url = join_url(request.build_absolute_uri(), *url_path)
                resp = requests.get(search_url, params=search_data)

                results = resp.json()

            context['form'] = form
            context['results'] = results

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


class PlaylistsView(TemplateView):
    template_name = "home.html"
    extra_css = []
    extra_javascript = []
    name = "Home"

    def get_context_data(self, **kwargs):
        context = super(PlaylistsView, self).get_context_data(**kwargs)
        context["page_title"] = self.name
        context["extra_css"] = self.extra_css
        context["extra_javascript"] = self.extra_javascript
        context["request"] = self.request

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['form'] = PlaylistForm()
        context['playlists'] = requests.get(reverse(""))

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = SongSearchForm(request.POST)
        results = False

        if form.is_valid():
            search_data = dict(format="json")
            for sk in list(form.cleaned_data.keys()):
                if sk == "search":
                    key = sk
                else:
                    key = "%s__icontains" % sk

                if form.cleaned_data.get(sk):
                    search_data.update({key: form.cleaned_data.get(sk)})

                url_path = path_explode(reverse("find_song"))
                search_url = join_url(request.build_absolute_uri(), *url_path)
                resp = requests.get(search_url, params=search_data)

                results = resp.json()

            context['form'] = form
            context['results'] = results

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(PlaylistsView, self).dispatch(*args, **kwargs)