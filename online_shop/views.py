from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
import ipdb

class ProductsList(View):
    def get(self, request):
        pass
        return render(request, 'index.html')
