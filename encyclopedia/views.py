from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.contrib.messages import get_messages





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

    return render(request, "encyclopedia/article_page.html", {
        "content": content,
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

    creation_form = NewEntryForm()
    return render(request, "encyclopedia/create_new.html", {
        'creation_form' : creation_form
    })

def edit(request, title):

    initial_data = {
        'title': title,
        'content': util.get_entry(title)
        }

    edit_form = NewEntryForm(initial=initial_data)

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


class NewEntryForm(forms.Form):
    title = forms.CharField(label = "Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea)
