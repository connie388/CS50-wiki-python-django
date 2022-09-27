from contextlib import redirect_stderr
from django.shortcuts import redirect, render
import random
from . import util
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from django.contrib import messages


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def search(request):
    instr = request.GET["q"]
    titlelist = list(
        filter((lambda x: instr.lower() in x.lower()), util.list_entries())
    )
    if len(titlelist) == 1 and titlelist[0].lower() == instr.lower():
        return redirect("entries", title=instr)
    else:
        return render(request, "encyclopedia/index.html", {"entries": titlelist})


def randompage(request):
    title = random.choice(util.list_entries())
    return entries(request, title)


def entries(request, title):

    entry = util.get_entry(title)
    if entry:
        # convert markdown to html and render the entry route
        translator = Markdown()
        html = translator.convert(entry)
        return render(
            request,
            "encyclopedia/entry.html",
            {"entry": html, "title": title},
        )
    else:
        messages.error(request, "Entry not found")
        return redirect("index")


def newpage(request):
    if request.method == "POST":
        entrytitle = request.POST["title"].strip()
        entrytextarea = request.POST["textarea"].strip()
        if entrytitle == "" or entrytextarea == "":
            messages.warning(request, "Title and Markdown content should not empty!")
            return render(request, "encyclopedia/newpage.html")
        else:
            entry = util.get_entry(entrytitle)
            if entry:
                messages.warning(request, "Record with title already exists!")
                return render(request, "encyclopedia/newpage.html")
            else:
                util.save_entry(entrytitle, entrytextarea)
                messages.success(request, "Record with title saved.")
                return render(request, "encyclopedia/newpage.html")
    elif request.method == "GET":
        return render(request, "encyclopedia/newpage.html")


def editpage(request, title):
    if request.method == "POST":
        entrytextarea = request.POST["textarea"].strip()
        util.save_entry(title, entrytextarea)
        messages.success(request, "Record with title updated.")
        return redirect("entries", title=title)
    elif request.method == "GET":
        entry = util.get_entry(title)
        return render(
            request, "encyclopedia/editpage.html", {"title": title, "textarea": entry}
        )
