from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from bom.demand_prediction import sarima
from bom.demand_prediction import bom_calculator
from .models import Product, RawMaterial, BillOfMaterials

def index(request):
    return render(request, "bom/home.html")


def products(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "bom/products.html", context)


def product_details(request, product_sku):
    product = get_object_or_404(Product , sku = product_sku)
    context = {"product": product}
    return render(request, "bom/product_details.html", context)


def raw_materials(request):
    context = {"rawmaterials":RawMaterial.objects.all()}
    return render(request, "bom/rawmaterials.html", context)

def raw_material_details(request, slug):
    raw_material = get_object_or_404(RawMaterial , slug = slug)
    context = {"rawmaterial": raw_material}
    return render(request, "bom/rawmaterial_details.html", context)


def boms(request):
    context = {"boms":BillOfMaterials.objects.all()}
    return render(request, "bom/boms.html", context)


def bom_detail(request, product_sku):
    product = get_object_or_404(Product, sku=product_sku)
    bom_items = BillOfMaterials.objects.filter(final_product=product)

    context = {
        "product": product,
        "bom_items": bom_items,
    }
    return render(request, "bom/bom_details.html", context)

def material_needs_view(request, product_sku):
    product = Product.objects.get(sku=product_sku)
    
    predicted_sales = sarima.calculate_sarima()
    
    material_needs = bom_calculator.calculate_material_needs_recursive(product, predicted_sales)
    
    return render(request, 'bom/material_needs.html', {'material_needs': material_needs, 'product': product})