# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
import pandas as pd
import matplotlib.pyplot as plt
import emoji
import os
import operator #for sorting dictionary


# Create your views here.
def home(request):
    return render(request, 'index.html')


def fileupload(request):
    if request.method == "POST":
        user_ip = request.META.get("REMOTE_ADDR")
        if not os.path.exists('./whatsapp/uploaded_files/' + user_ip):
            os.makedirs('./whatsapp/uploaded_files/' + user_ip)
        path_to_upload = './whatsapp/uploaded_files/' + user_ip + "/"

        files = request.FILES
        for file in files.getlist('file'):
            if os.path.exists(path_to_upload + "chat.txt"):
                os.remove(path_to_upload + "chat.txt")
            with open(path_to_upload + "chat.txt", 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
        file_check = "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info."
        file_check_group = "created group"
        message = 'error'
        with open(path_to_upload + "chat.txt", 'r', encoding="utf8") as f:
            first_line = f.readline();
            if first_line.__contains__(file_check) or first_line.__contains__(file_check_group):
                message = 'success'

        return render(request, 'index.html', {'message': message})
    return redirect(home)


def fileread(user_ip):
    chat = []
    exclude_string = "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info."
    with open('./whatsapp/uploaded_files/' + user_ip + '/chat.txt', encoding='utf8') as f:
        for line in f:
            lines = line.split(' - ')  # Divide between date and the rest
            if len(lines) > 1:
                if not lines[1].__contains__(exclude_string):
                    lines2 = lines[1].split(': ')  # Divide between user and text
                    if len(lines2) > 1:
                        speaker = lines2[0]
                        text = lines2[1]
                        timestamp = lines[0]
                        chat += [[timestamp, speaker, text]]
    return chat
# 9767452363

def messagecount(request):
    user_ip = request.META.get("REMOTE_ADDR")
    count = {}
    chat = fileread(user_ip)
    for c in chat:
        speaker = c[1]
        if c[1] not in count.keys():
            count[c[1]] = 1
        else:
            count[c[1]] += 1
    sorted_count = sorted(count.items(), key=lambda kv: kv[1], reverse=True)
    return render(request, 'index.html', {'count': sorted_count})