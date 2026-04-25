from django import template

register = template.Library()

@register.simple_tag
def get_category_config(category_name):
    default_config = {
        'icon': 'bi-tag',
        'color': '#E11D48',
        'bg': '#E11D4826',
    }

    if not category_name:
        return default_config
        
    name = str(category_name).lower().strip()
    
    configs = {
        'diversos': {
            'icon': 'bi-layers',
            'color': '#64748B',
            'bg': '#64748B26',
        },
        'equipamentos': {
            'icon': 'bi-mouse2',
            'color': '#22C55E',
            'bg': '#22C55E26',
        },
        'logística': {
            'icon': 'bi-truck',
            'color': '#A78BFA',
            'bg': '#A78BFA26',
        },
        'materiais': {
            'icon': 'bi-box',
            'color': '#F59E0B',
            'bg': '#F59E0B26',
        },
        'serviços': {
            'icon': 'bi-tools',
            'color': '#257AFA',
            'bg': '#257AFA26',
        },
        'softwares': {
            'icon': 'bi-code-slash',
            'color': '#38BDF8',
            'bg': '#38BDF826',
        },
    }
    
    return configs.get(name, default_config)
