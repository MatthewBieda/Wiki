from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from markdown2 import Markdown
import secrets

from . import util

# initalize markdown conversion
markdowncoversion = Markdown()

# Views are essentially functions that inform template rendering,
# acting like the controller from the MVC paradigm. They bridge the model and template (known as View in MVC).

#This function simply returns the index template and shows all existing entries.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#This function converts the entry and displays it in the entry template, returning a 404 template instead if not found. 
def entry(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/404.html", {
            "entrytitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowncoversion.convert(entry_page),
            "entrytitle": entry
        })

# Dealing with the user's search query
def search(request):
    # Grab user input into a variable
    usersearch = request.GET.get('q')
    if util.get_entry(usersearch) is not None:
        # Using Django's reverse function to reverse URL resolution
        named_redirect = reverse("entry", kwargs={'entry': usersearch})
        return HttpResponseRedirect(named_redirect)
    # If the search was invalid, return possible matches constructed with an array
    else:
        possiblematches = []
        for entry in util.list_entries():
            if usersearch.upper() in entry.upper():  #normalisng case
                possiblematches.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": possiblematches
        })

# If a user wishes to add a new entry, first send them to the entry form
def newpage(request):
    return render(request, "encyclopedia/newpage.html")

# Capture the user submitted data and save it as a new entry
def savepage(request):
    new_title = request.POST['title']
    new_body = request.POST['body']
    # Validate that this entry does not already exist
    if new_title in util.list_entries():
        return render(request, "encyclopedia/alreadyexists.html", {
            "entrytitle": new_title
        })
    else:
        util.save_entry(new_title, new_body)
        markdowncoversion.convert(new_body)
        saved_redirect = reverse("entry", kwargs={'entry': new_title})
        return HttpResponseRedirect(saved_redirect)

# Simply uses a library to pick a random element from existing entries and returns it
def random(request):
    entrylist = util.list_entries()
    chooserandom = secrets.choice(entrylist)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': chooserandom}))

# Returns an editing page prefilled with existing data, note the Title is immutable. 
def edit(request, entry):
    entryPage = util.get_entry(entry)
    return render(request, "encyclopedia/edit.html", {
        "entry": entryPage,
        "entrytitle": entry
    })

# Commit an edit to the database
def saveedit(request):
    title = request.POST['title']
    new_body = request.POST['body']
    util.save_entry(title, new_body)
    markdowncoversion.convert(new_body)
    saved_redirect = reverse("entry", kwargs={'entry': title})
    return HttpResponseRedirect(saved_redirect)