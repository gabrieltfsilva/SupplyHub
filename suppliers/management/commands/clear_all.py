from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from suppliers.models import Subcategory, Supplier, Review

class Command(BaseCommand):
    help = 'Limpa todos os dados, preservando apenas o usuário gabriel.'

    def handle(self, *args, **kwargs):
        # Avaliações
        Review.objects.all().delete()

        # Fornecedores
        Supplier.objects.all().delete()

        # Subcategorias
        Subcategory.objects.all().delete()

        # Usuários
        User.objects.exclude(username='gabriel').delete()

        self.stdout.write(self.style.SUCCESS("Banco limpo."))
        