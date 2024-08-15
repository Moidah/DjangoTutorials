from typing import Any
from django import forms
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

#def homePageView(request): #new
#    return HttpResponse("Hello World!") #new
class homePageView(TemplateView):
    template_name ='pages/home.html'
    
    
class AboutPageView(TemplateView):
    template_name='pages/about.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title":"About us - Online Store",
            "subtitle":"About us",
            "description":"This is an about page...",
            "author":"Developed by: Your Name",
        })
        
        return context
    

def contactPageView(request):
    return render(request, 'pages/contact.html', {
        "title": "Contact Us",
        "subtitle": "Get in touch with us",
        "email": "contact@example.com",
        "phone": "+1234567890",
        "address": "123 Django Lane"
    })
    
    
class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": "299.99"},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": "999.99"},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": "49.99"},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": "129.99"}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products
        }
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)  
            product = next((p for p in Product.products if int(p['id']) == product_id), None)
            if not product:
                raise ValueError("Product not found")
            
            product['price'] = float(product['price'])  
        except (ValueError, StopIteration):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": product["name"] + " - Online Store",
            "subtitle": product["name"] + " - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)
    
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        print("GET method called in ProductCreateView")  
        form = ProductForm()
        viewData = {
        "title": "Create Product",
        "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
        
            new_product = Product(name=form.cleaned_data['name'], price=form.cleaned_data['price'])
            new_product.save()
            return redirect('product_index')
        else:
            viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)