from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from suppliers.models import Supplier, Review, Subcategory


@login_required
def home(request):
    total_suppliers = Supplier.objects.count()

    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    total_reviews_count = Review.objects.count()

    categories_metrics = []
    for val, label in Subcategory.CATEGORY_CHOICES:
        count = Supplier.objects.filter(subcategory__category=val).count()
        categories_metrics.append({'name': label, 'count': count})

    top_suppliers = Supplier.objects.annotate(
        average_rating=Avg('reviews__rating')
    ).filter(average_rating__gt=0).order_by('-average_rating')[:6]

    return render(request, "core/home.html", {
        'total_suppliers': total_suppliers,
        'avg_rating': avg_rating,
        'total_reviews_count': total_reviews_count,
        'categories_metrics': categories_metrics,
        'top_suppliers': top_suppliers,
    })


@login_required
def users(request):
    if request.user.is_superuser:
        usuarios = User.objects.all().order_by('username')
    else:
        usuarios = User.objects.filter(id=request.user.id)

    return render(request, "core/users.html", {
        "usuarios": usuarios
    })


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para excluir usuários.")
        return redirect('users')

    user_to_delete = get_object_or_404(User, id=user_id)

    if user_to_delete == request.user:
        messages.error(request, "Você não pode excluir sua própria conta por aqui.")
    else:
        user_to_delete.delete()
        messages.success(request, "Usuário removido com sucesso.")

    return redirect('users')
