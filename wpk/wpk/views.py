from django.http import JsonResponse
from django.http import FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


#kto zalogowany
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone
import time
import datetime

from .forms import DocumentForm
from django.shortcuts import redirect
from .models import Dopacjenta
from .models import Document
from django.db import connection

chattext = ""
listauserowchatu = ""
chatreqcount = 0
timer = 0


f= open("/dev/shm/chattext.txt","w")
f.write("")
f.close()

l= open("/dev/shm/listauserowchatu.txt","w")
l.write(" ")
l.close()

#

#


def ssl(request):
    return FileResponse(open('ssl.txt', 'rb'))


def hi(request):
    l= open("wejsc.txt","r")
    wejsc = l.read()
    l.close()

    wejsc=int(wejsc)
    wejsc = wejsc + 1

    x= open("wejsc.txt","w")
    x.write(str(wejsc))
    x.close()

    return redirect('/wpk/')



def skypeframe(request):
    l= open("status.txt","r")
    status = l.read()
    l.close()
    l= open("videolink.txt","r")
    videolink = l.read()
    l.close()
    return render(request, 'skype_frame.html', {'status': status, 'videolink': videolink})

def statusskype(request):
    if request.method == 'POST':
        f= open("status.txt","w")
        f.write(request.POST.__getitem__("status"))
        f.close()

        f= open("videolink.txt","w")
        f.write(request.POST.__getitem__("videolink"))
        f.close()

        return HttpResponse("status ustawiony")

    else:
        return render(request, 'status.html')

def skrzynka_pacjenta(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "nikt"
    wiadomosci = Dopacjenta.objects.filter(pacjent=username)
    return render(request, 'skrzynka_pacj.html', {'wiadomosci': wiadomosci})

def logout_view(request):
    logout(request)
    return render(request, "afterlogout.html")



#def get_current_users():
#    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#    user_id_list = []
#    for session in active_sessions:
#       data = session.get_decoded()
#        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
#    return str(User.objects.filter(id__in=user_id_list))

@csrf_exempt
def usunwiadomosc(request):
    if request.method == 'POST':
        jsonstr = json.loads(request.body)
        jsondict = json.loads(jsonstr)


        wiadId = int(jsondict["usun"])

        Dopacjenta.objects.filter(id=wiadId).delete()


        return JsonResponse({"info": "usunięto"}, status=200)

@csrf_exempt
def usunwiadomoscf(request):
    if request.method == 'POST':
        jsonstr = json.loads(request.body)
        jsondict = json.loads(jsonstr)


        wiadId = int(jsondict["usun"])

        Document.objects.filter(id=wiadId).delete()


        return JsonResponse({"info": "usunięto"}, status=200)



@csrf_exempt
def poufneajaxp(request):
    if request.method == 'POST':
        jsonstr = json.loads(request.body)
        jsondict = json.loads(jsonstr)

        txt0 = jsondict["txt0"]
        txt1 = jsondict["txt1"]
        txt2 = jsondict["txt2"]

        dopacjenta = Dopacjenta.objects.create(pacjent=txt0, message=txt1, contact=txt2)


        return JsonResponse({"info": "zapisano w bazie danych"}, status=200)

    else:

        return render(request, "dopacjenta.html")



@csrf_exempt
def poufneajax(request):
    jsonstr = json.loads(request.body)
    jsondict = json.loads(jsonstr)

    txt0 = jsondict["txt0"]
    txt1 = jsondict["txt1"]
    txt2 = jsondict["txt2"]
#    txt3 = str(datetime.datetime.now())

    wiadomosc = Document.objects.create(pacjent=txt0, description=txt1, document=txt2)


    return JsonResponse({"info": "git"}, status=200)



def wiadomosci(request):
    if request.user.is_superuser:

        przesylki = Document.objects.all()

        return render(request, "wiadomosci.html", {"przesylki": przesylki})
    else:
        return HttpResponse("kaszanka")






@csrf_exempt
def chat(request):
    jsonstr = json.loads(request.body)
    jsondict = json.loads(jsonstr)
    global chattext
    global listauserowchatu
    global chatreqcount
    global timer

    if (timer + 30) < int(time.time()):
        timer = int(time.time())
        l= open("/dev/shm/listauserowchatu.txt","w")
        l.write(" ")
        l.close()

    if jsondict["znak"] != "":
        l= open("/dev/shm/listauserowchatu.txt","r")
        listauserowchatu = l.read()
        l.close()
        if jsondict["znak"] not in listauserowchatu:
            l= open("/dev/shm/listauserowchatu.txt","a")
            l.write(jsondict["znak"] + " ")
            l.close()

    if jsondict["command"] == "czekamnatxt":
        if jsondict["mess"] != "":
            f= open("/dev/shm/chattext.txt","r")
            chattext = f.read()
            f.close()
            if jsondict["nick"][:3] == "$z$":
                chattext = chattext + "<i><b style='color: lime;'>" + jsondict["nick"][3:] + ":</b></i> " + "<i style='color: lime;'>" + jsondict["mess"] + "</i><br>"
            elif jsondict["nick"] == "piotrek":
                chattext = chattext + "<i><b style='color: red;'>" + jsondict["nick"] + ":</b></i> " + "<i style='color: red;'>" + jsondict["mess"] + "</i><br>"
            else:
                chattext = chattext + "<i><b>" + jsondict["nick"] + ":</b></i> " + jsondict["mess"] + "<br>"
            while len(chattext) > 1000:
                chattext = chattext[1:len(chattext)]

            f= open("/dev/shm/chattext.txt","w")
            f.write(chattext)
            f.close()

            l= open("/dev/shm/listauserowchatu.txt","r")
            listauserowchatu = l.read()
            l.close()

            return JsonResponse({"info": chattext, "chatownicy": listauserowchatu}, status=200)
        else:
            f= open("/dev/shm/chattext.txt","r")
            chattext = f.read()
            f.close()

            l= open("/dev/shm/listauserowchatu.txt","r")
            listauserowchatu = l.read()
            l.close()
            return JsonResponse({"info": chattext, "chatownicy": listauserowchatu}, status=200)


def poufne(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return render(request, "dzienks.html") #!
    else:
        form = DocumentForm()

        return render(request, 'poufne_frame.html', {
        'form': form
        })

def dzienks(request):
    return render(request, "dzienks.html")

##########

def newsy(request):
    cursor = connection.cursor()
    cursor.execute('SELECT content from forum_conversation_post WHERE topic_id="21"')
    posty = cursor.fetchall()
    ogloszenia = ""
    for i in reversed(posty):
        ogloszenia = ogloszenia + i[0]

    return render(request, "newsy.html", {"ogloszenia": ogloszenia})


##########


def liczbaodebranychpw(request):
    return render(request, "pw.html")

