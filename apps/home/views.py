# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import pandas as pd
from contextlib import redirect_stderr
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.shortcuts import render, redirect
from .LexicalAnalyzerClass import LexicalAnalyzer
 
from .models import TBA
from .forms import FormTBA

@login_required(login_url="/login/")
def index(request):

    if request.method == "POST":
        form = FormTBA(request.POST)
        if form.is_valid():
            form.save()
            
            # Process to Read and Parser
            rex = {
                'sentence': form.cleaned_data['words'],
                'parse_table_file': '/mnt/x/School/College/4th Semester/Teori Bahasa dan Automata/Tubes/apps/templates/home/parser.csv',
                'lexical_transition_file': '/mnt/x/School/College/4th Semester/Teori Bahasa dan Automata/Tubes/apps/templates/home/lexical.csv',
                'debug': True
            }

            Check_L =  None
            L= LexicalAnalyzer(rex)
            Temp_L, Check_L = L.reading(Check_L)
            print(Check_L)

            if Check_L:
                messages.success(request, Temp_L)
            elif not Check_L:
                messages.info(request, Temp_L)

            return redirect('home')
        else:
            messages.error(request, 'Something Wrong! HAD NO IDEA')
            return redirect("home")
    else:
        form = FormTBA()
    return render(request, 'home/tba.html', {'form':form})