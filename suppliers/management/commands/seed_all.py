import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from suppliers.models import Subcategory, Supplier, Review

class Command(BaseCommand):
    help = 'Gera dados de teste: Usuários, Subcategorias, Fornecedores e Reviews.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando geração de dados...")

        # Usuários
        user_names = ['Fulano', 'Sicrano', 'Beltrano']
        test_users = []
        for name in user_names:
            pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            u, created = User.objects.get_or_create(
                username=name.lower(),
                defaults={'email': f'{name.lower()}@supplyhub.com'}
            )
            if created:
                u.set_password(pwd)
                u.save()
            test_users.append(u)

        # Subcategorias
        data_map = {
            'equipamentos': ['Sensores', 'Controladores', 'Motores', 'Displays'],
            'softwares': ['Licenças', 'Sistemas Operacionais', 'Gestão', 'Banco de Dados'],
            'servicos': ['Manutenção', 'Consultoria', 'Limpeza'],
            'logistica': ['Transporte', 'Armazenagem', 'Despacho'],
            'materiais': ['Elétrica', 'Hidráulica', 'Construção', 'Escritório'],
            'diversos': ['Produtos Químicos', 'Brindes Corporativos'],
        }

        all_subs = []
        for cat, names in data_map.items():
            for name in names:
                sub, _ = Subcategory.objects.get_or_create(category=cat, name=name)
                all_subs.append(sub)

        # Fornecedores
        suppliers_list = [
            "VoltTech Automação", "Engenharia Global", "Brasil Log", "SoftSolutions",
            "Minas Materiais", "ServicePlus", "TechGears", "ElectroFlux", "Itabirito Tech"
        ]
        
        created_suppliers = []
        for name in suppliers_list:
            s, _ = Supplier.objects.get_or_create(
                name=name,
                defaults={
                    'location': random.choice(['Itabirito, MG', 'Belo Horizonte, MG', 'São Paulo, SP']),
                    'phone': f'31 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}',
                    'email': f'contato@{name.lower().replace(" ", "")}.com.br',
                    'subcategory': random.choice(all_subs)
                }
            )
            created_suppliers.append(s)

        # Avaliações
        comments = ["Excelente fornecedor!", "Entrega no prazo.", "Boa qualidade.", "Preço justo."]
        
        for s in created_suppliers:
            num_evaluators = random.randint(0, len(test_users))
            evaluators = random.sample(test_users, k=num_evaluators)
            
            for u in evaluators:
                Review.objects.get_or_create(
                    supplier=s,
                    user=u,
                    defaults={
                        'rating': random.randint(3, 5),
                        'comment': random.choice(comments)
                    }
                )

        self.stdout.write(self.style.SUCCESS("Dados gerados."))
        