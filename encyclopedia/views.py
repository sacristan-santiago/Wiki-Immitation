from django.shortcuts import render
from . import util
import markdown2
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from django import forms
import random

class PageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Content. Please use markdown formatting.'}))

class NewPageForm(PageForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            raise ValidationError("Title entry already exists.")
        return title

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    content = util.get_entry(title)
    html = markdown2.markdown(content)

    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "content": html
    })


def search(request):
    q = request.GET.get("q").lower()

    if q in [entry.lower() for entry in util.list_entries()]:
        return HttpResponseRedirect(reverse("wiki", args=[q]))
    else:
        filtered = [entry for entry in util.list_entries() if q in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "entries": filtered,
        })
    

def addPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })
    

def editPage(request, title):
    if request.method == "POST":
        form = PageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki", args=[title]))
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": title
            })
    else:
        content = util.get_entry(title)
        initial_data = {
            'title': title, 
            'content': content
        }
        form = PageForm(initial=initial_data)

        return render(request, "encyclopedia/edit_page.html", {
            "form": form,
            "title": title
        })


def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return wiki(request, title)