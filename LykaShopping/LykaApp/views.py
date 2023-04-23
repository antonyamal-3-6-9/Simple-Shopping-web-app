from django.shortcuts import get_object_or_404, render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request, cSlug = None):
    devs = None
    categ = None
    if cSlug is not None:
        categ = get_object_or_404(Cate,slug = cSlug)
        devs = Device.objects.filter(category = categ)
    else:
        devs = Device.objects.all()
    cat = Cate.objects.all()
    pg = Paginator(devs, 4)
    try:
        pgNum = int(request.GET.get('page','1'))
    except PageNotAnInteger:
        pgNum = 1
    try:
        pageContent = pg.get_page(pgNum)
    except EmptyPage:
        pageContent = pg.page(pg.num_pages)

    return render(request, 'index.html', {'cats' : cat , 'products' : pageContent})


def detail(request,cSlug = None, dSlug = None):
    dev = Device.objects.get(category__slug=cSlug, slugModel = dSlug)
    return render(request, 'detail.html', {"device" : dev})


def search(request):
    searchQuery = None;
    prodc = None;
    if request.method == "GET":
        searchQuery = request.GET.get('query')
        prodc = Device.objects.all().filter(Q(brand__icontains=searchQuery)|Q(modelName__icontains=searchQuery))
    pg = Paginator(prodc, 2)
    try:
        pgNum = int(request.GET.get('page','1'))
    except PageNotAnInteger:
        pgNum = 1
    try:
        pageContent = pg.get_page(pgNum)
    except EmptyPage:
        pageContent = pg.page(pg.num_pages)
    return render(request, 'search.html', {'query' : searchQuery, 'products' : pageContent})

