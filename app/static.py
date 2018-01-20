# -*- coding: utf-8 -*-

from django.shortcuts import render

from app.auth import get_default_context


def get_links(request):
    context = get_default_context(request)
    return render(
        request,
        'app/static/links.html',
        context
    )


def get_agreement(request):
    context = get_default_context(request)
    return render(
        request,
        'app/static/agreement.html',
        context
    )


def get_inf(request):
    context = get_default_context(request)
    return render(
        request,
        'app/static/inf.html',
        context
    )
