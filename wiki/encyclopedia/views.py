from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
import random

import markdown2
from . import util

class NewTaskForm(forms.Form):
    search = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Search'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Enter text here ...'}))
    def clean_title(self):
        data = self.cleaned_data['title']
        if data in util.list_entries():
            raise ValidationError("That title is already in use!")
        return data


def index(request):
    if request.method == "POST":

        form = NewTaskForm(request.POST)

        if form.is_valid():
            search = form.cleaned_data["search"]
            entry_list = util.list_entries()
            similar=[]

            for entry in entry_list:
                if search.lower() == entry.lower():
                    return HttpResponseRedirect(reverse("wiki:display", args=[search]))
                elif search.lower() in entry.lower():
                    similar.append(entry)
            return render(request, "encyclopedia/results.html", {
                "entries": similar,
                "form": NewTaskForm()
             })
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/index.html", {
                "form": form
            })


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTaskForm()
    })




def display_info(request, title):

    if title.lower() == "create":
        return HttpResponseRedirect(reverse("wiki:create_page"))
    if util.get_entry(title)== None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/information.html", {
            "title": title,
            "entries": markdown2.markdown(util.get_entry(title)),
            "form": NewTaskForm()
        })



def create_page(request):
    if request.method == "POST":
        
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:display", args=[title]))
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new_page.html", {
                "form2": form,
                "form": NewTaskForm()
            })

    return render(request, "encyclopedia/new_page.html",{
        "form": NewTaskForm(),
        "form2": NewPageForm()
    })

def edit_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        
        return render(request, "encyclopedia/edit.html",{
            "entries": util.get_entry(title),
            "form":NewTaskForm(),
            "title": title
        })

def save_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("wiki:display", args=[title]))
    
def random_page(request):
    titles = util.list_entries()
    pick = random.randint(0, len(titles)-1)
    title = titles[pick]
    return HttpResponseRedirect(reverse("wiki:display", args=[title]))
    
        


