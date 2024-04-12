import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.contrib.messages import get_messages
from markdown2 import Markdown




from . import util


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):

    search_term = (request.GET.get('q'))

    found_articles = util.list_entries()

    if search_term in found_articles:
        return HttpResponseRedirect(reverse("title", kwargs={'title':search_term})) 
    
    search_results = []
    
    for found_article in found_articles:
        if search_term in found_article:
            search_results.append(found_article)

    return render(request, "encyclopedia/search_results.html", {
        "search_results": search_results
    })

def title(request, title):
    
    content = util.get_entry(title)

    if content:
        markdowner = Markdown()
        result = markdowner.convert(content)
    
    else:
        return HttpResponseRedirect(reverse("not_found"))

    return render(request, "encyclopedia/article_page.html", {
        "content": result,
        "title" : title
    })
 
def new(request):

    if request.method == 'POST':
        form_data = NewEntryForm(request.POST)
                
        if form_data.is_valid():
            title = form_data.cleaned_data["title"]
            content = form_data.cleaned_data["content"]

            if util.get_entry(title):
                messages.add_message(request, messages.ERROR, "Entry Already Exists")

            else: 
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("title", kwargs={'title':title})) 

    form = NewEntryForm()

    creation_form = form.render("encyclopedia/form_snippet.html")


    return render(request, "encyclopedia/create_new.html", {
        'creation_form' : creation_form
    })

def edit(request, title):

    initial_data = {
        'title': title,
        'content': util.get_entry(title)
        }

    form = NewEntryForm(initial=initial_data)
    edit_form = form.render("encyclopedia/form_snippet.html")

    return render(request, "encyclopedia/edit_page.html",{
        'edit_form': edit_form
    })

def edit_post(request):

    if request.method == 'POST':
        form_data = NewEntryForm(request.POST)

        if form_data.is_valid():
            title = form_data.cleaned_data["title"]
            content = form_data.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", kwargs={'title':title})) 


def random_page():

    available_entries = util.list_entries()
    title = available_entries[random.randint(0,len(available_entries)-1)]

    return HttpResponseRedirect(reverse("title", kwargs={'title':title})) 

def not_found(request):
    return render(request, "encyclopedia/404.html")

class NewEntryForm(forms.Form):
    title = forms.CharField(label = "Title", max_length=100, widget=forms.TextInput(attrs={"class": "form-control-lg form-control"}))

    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "style": "height: 50vh;"}), label= "Content")
