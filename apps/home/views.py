# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from contextlib import redirect_stderr
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.shortcuts import render, redirect
from .lexical_analyzer_class import LexicalAnalyzer
from .parser_class import Parser
 
from .models import TBA
from .forms import FormTBA

@login_required(login_url="/login/")
def index(request):

    if request.method == "POST":
        form = FormTBA(request.POST)
        if form.is_valid():
            form.save()
            
            # Process to Read and Parse
            config = {
                'kalimat': form.cleaned_data['words'],
                'parse_table': './apps/templates/home/parser_.csv',
                'transisi_lexical': './apps/templates/home/lexical.csv',
                'debug': True
            }

            '''lexical analyzer'''
            Check_L =  None
            L = LexicalAnalyzer(config)
            Temp_L, Check_L = L.reading(Check_L)
            print(Check_L)

            if Check_L:
                messages.success(request, Temp_L)
            elif not Check_L:
                messages.info(request, Temp_L)

            '''parser'''
            Check_P =  None
            P = Parser(config)
            Temp_P, Check_P = P.reading(Check_P)
            print(Check_P)

            if Check_P:
                messages.success(request, Temp_P)
            elif not Check_P:
                messages.info(request, Temp_P)

            return redirect('home')

        else:
            messages.error(request, 'Something Wrong! HAD NO IDEA')
            return redirect("home")
    else:
        form = FormTBA()
    return render(request, 'home/tba.html', {'form':form})