from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404
from .models import Subcategory, Supplier, Review
from django.db.models import Avg
from django.db import IntegrityError


# Filters and lists suppliers with calculated average ratings and category grouping.
@login_required
def suppliers(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('categoria', '')
    subcategory_filter = request.GET.get('subcategoria', '')

    suppliers_list = Supplier.objects.select_related('subcategory').annotate(
        average_rating=Avg('reviews__rating')
    ).order_by('name')

    if search_query:
        suppliers_list = suppliers_list.filter(name__icontains=search_query) | suppliers_list.filter(
            location__icontains=search_query)

    if category_filter:
        suppliers_list = suppliers_list.filter(subcategory__category=category_filter)

    if subcategory_filter:
        suppliers_list = suppliers_list.filter(subcategory_id=subcategory_filter)

    return render(request, "suppliers/suppliers.html", {
        'suppliers': suppliers_list,
        'categories_list': Subcategory.CATEGORY_CHOICES,
        'all_subcategories': Subcategory.objects.all().order_by('name')
    })


# Displays detailed information for a single supplier, including user reviews and metrics.
@login_required
def supplier(request, supplier_id):
    try:
        supplier_obj = Supplier.objects.select_related('subcategory').get(id=supplier_id)
    except Supplier.DoesNotExist:
        raise Http404("Fornecedor não encontrado")

    reviews = supplier_obj.reviews.select_related('user').all()
    average = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, "suppliers/supplier.html", {
        'supplier': supplier_obj,
        'reviews': reviews,
        'average': round(average, 1),
        'count': reviews.count()
    })


# Handles the creation or update of supplier evaluations with mandatory feedback validation.
@login_required
def rate_supplier(request, supplier_id):
    supplier_obj = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        rating = request.POST.get('nota')
        comment = request.POST.get('comentario')

        if not rating or not comment:
            messages.error(request, "A nota e o comentário são obrigatórios para a avaliação.")
            return render(request, 'suppliers/rate_supplier.html', {'supplier': supplier_obj})

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


# Removes the current user's evaluation from a specific supplier's profile.
@login_required
def delete_review(request, supplier_id):
    supplier_obj = get_object_or_404(Supplier, id=supplier_id)
    Review.objects.filter(supplier=supplier_obj, user=request.user).delete()
    return redirect('supplier', supplier_id=supplier_obj.id)


# Manages administrative creation and listing of subcategories for supplier classification.
@login_required
def categories(request):
    if request.method == "POST":
        if not request.user.is_superuser:
            raise PermissionDenied

        subcategory_name = request.POST.get('nome')
        category_value = request.POST.get('categoria')

        if subcategory_name and category_value:
            try:
                Subcategory.objects.create(
                    name=subcategory_name,
                    category=category_value
                )
                return redirect('categories')
            except IntegrityError:
                messages.error(request, "Esta subcategoria já existe nesta categoria.")

    subcategories = Subcategory.objects.all().order_by('category', 'name')
    categories_list = Subcategory.CATEGORY_CHOICES

    return render(request, "suppliers/categories.html", {
        'subcategories': subcategories,
        'categories_list': categories_list
    })


# Restricts the removal of subcategory records to authorized administrative users.
@login_required
def delete_subcategory(request, sub_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    subcategory = get_object_or_404(Subcategory, id=sub_id)
    subcategory.delete()
    return redirect('categories')


# Processes the registration of new suppliers with permission-guarded form handling.
@login_required
def create_supplier(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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
            except Exception:
                messages.error(request, "Erro ao cadastrar fornecedor.")
        else:
            messages.error(request, "Preencha os campos obrigatórios.")

    subcategories = Subcategory.objects.all().order_by('name')
    categories_list = Subcategory.CATEGORY_CHOICES
    return render(request, "suppliers/create_supplier.html", {
        'subcategories': subcategories,
        'categories_list': categories_list
    })


# Manages administrative updates to supplier details and classification metadata.
@login_required
def edit_supplier(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied

    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        description = request.POST.get('description')
        subcategory_id = request.POST.get('subcategory')

        if email and subcategory_id:
            try:
                sub = get_object_or_404(Subcategory, id=subcategory_id)
                supplier.location = location
                supplier.phone = phone
                supplier.email = email
                supplier.description = description
                supplier.subcategory = sub
                supplier.save()
                return redirect('suppliers')
            except Exception:
                messages.error(request, "Erro ao atualizar fornecedor.")
        else:
            messages.error(request, "Dados obrigatórios ausentes.")

    subcategories = Subcategory.objects.all().order_by('name')
    categories_list = Subcategory.CATEGORY_CHOICES
    return render(request, "suppliers/create_supplier.html", {
        'supplier': supplier,
        'subcategories': subcategories,
        'categories_list': categories_list
    })


# Executes the permanent removal of supplier records, restricted to superusers.
@login_required
def delete_supplier(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied

    try:
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
    except Exception:
        messages.error(request, "Erro ao remover fornecedor.")

    return redirect('suppliers')
