from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    Product.objects.create(name="Atssini")
    product = Product.objects.all()
    print (product)
    return render(request,'first_app/index.html')
