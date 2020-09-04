from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from random import randint

markdowner= Markdown()
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,title):
    content=util.get_entry(title)
    if  content == None:
        content = "page was not found!"
        return render(request, "encyclopedia/entry.html", {"viki":
        content})
    else:
        content=markdowner.convert(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
            "entries": content,
        "title": title})


def search(request):
    q = request.GET.get('q')
    viki=[]
    if q in util.list_entries():
        return redirect("entry", title=q)
    for entry in util.list_entries():
        if q.upper() in entry.upper():
           viki.append(entry)
    return render(request, "encyclopedia/search.html", {"search": viki})



def newentry(request):
    viki = request.POST.get('text')
    riki=request.POST.get('content')
    if request.method== "POST":
        if viki == "" or riki == "" :
            return render(request, "encyclopedia/newentry.html", {
            "message": 'Title or content must be filled'
        })
        elif viki in util.list_entries():
            return render(request, "encyclopedia/newentry.html", {
            "message": 'Title already exist'
        })
        else:
            util.save_entry(viki, riki)
            return redirect("entry", title = viki)
    return render(request, "encyclopedia/newentry.html")




def  edit(request , title) :
    content = markdowner.convert(util.get_entry(title.strip()))
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})
    if request.method== "POST":
        content= request.POST.get('content')
        if content == "":
            return render(request, "encyclopedia/newentry.html", {
                "message": 'Title or content must be filled'
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {
        "content": content, "title": title
    })





def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)
