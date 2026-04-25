from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subcategory, Supplier, Review
from django.db.models import Avg
from .forms import ReviewForm

@login_required
def suppliers(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('categoria', '')
    subcategory_filter = request.GET.get('subcategoria', '')

    suppliers_list = Supplier.objects.annotate(
        average_rating=Avg('reviews__rating')
    ).all()

    if search_query:
        suppliers_list = suppliers_list.filter(name__icontains=search_query) | suppliers_list.filter(location__icontains=search_query)

    if category_filter:
        suppliers_list = suppliers_list.filter(subcategory__category=category_filter)

    if subcategory_filter:
        suppliers_list = suppliers_list.filter(subcategory_id=subcategory_filter)

    return render(request, "suppliers/suppliers.html", {
        'suppliers': suppliers_list,
        'categories_list': Subcategory.CATEGORY_CHOICES,
        'all_subcategories': Subcategory.objects.all()
    })

@login_required
def supplier(request, supplier_id):
    supplier_obj = get_object_or_404(Supplier, id=supplier_id)
    reviews = supplier_obj.reviews.all()
    average = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, "suppliers/supplier.html", {
        'supplier': supplier_obj,
        'reviews': reviews,
        'average': round(average, 1),
        'count': reviews.count()
    })

@login_required
def rate_supplier(request, supplier_id):
    supplier_obj = get_object_or_404(Supplier, id=supplier_id)
    
    if request.method == 'POST':
        rating = request.POST.get('nota')
        comment = request.POST.get('comentario')
        
        if rating:
            Review.objects.update_or_create(
                supplier=supplier_obj,
                user=request.user,
                defaults={
                    'rating': int(rating),
                    'comment': comment
                }
            )
            return redirect('supplier', supplier_id=supplier_obj.id)
            
    return render(request, 'suppliers/rate_supplier.html', {'supplier': supplier_obj})

@login_required
def delete_review(request, supplier_id):
    supplier_obj = get_object_or_404(Supplier, id=supplier_id)
    review = Review.objects.filter(supplier=supplier_obj, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        return redirect('supplier', supplier_id=supplier_obj.id)
        
    return redirect('supplier', supplier_id=supplier_obj.id)

@login_required
def categories(request):
    if request.method == "POST":
        subcategory_name = request.POST.get('nome')
        category_value = request.POST.get('categoria')
        
        if subcategory_name and category_value:
            Subcategory.objects.create(
                name=subcategory_name, 
                category=category_value
            )
            return redirect('categories')

    subcategories = Subcategory.objects.all()
    categories_list = Subcategory.CATEGORY_CHOICES
    
    return render(request, "suppliers/categories.html", {
        'subcategories': subcategories,
        'categories_list': categories_list
    })

@login_required
def delete_subcategory(request, sub_id):
    subcategory = get_object_or_404(Subcategory, id=sub_id)
    subcategory.delete()
    return redirect('categories')

@login_required
def create_supplier(request):
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        description = request.POST.get('description')
        subcategory_id = request.POST.get('subcategory')

        if name and email and subcategory_id:
            try:
                sub = get_object_or_404(Subcategory, id=subcategory_id)
                Supplier.objects.create(
                    name=name,
                    location=location,
                    phone=phone,
                    email=email,
                    description=description,
                    subcategory=sub
                )
                return redirect('suppliers')
            except:
                pass

    subcategories = Subcategory.objects.all()
    categories_list = Subcategory.CATEGORY_CHOICES
    
    return render(request, "suppliers/create_supplier.html", {
        'subcategories': subcategories,
        'categories_list': categories_list
    })
