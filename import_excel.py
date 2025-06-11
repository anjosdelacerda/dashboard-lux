import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from users.models import User
from empresas.models import Empresa

excel_path = 'data/Simulação_Projeto_Interno_25.xlsx'

df = pd.read_excel(
    excel_path,
    sheet_name='Dados',
    header=1,
    usecols='B:V',
    dtype=str
)
df = df.fillna('')

df = df.rename(columns={
    'Empresa': 'Empresa_usuario',
    'Empresa.1': 'Empresa_empresa'
})

cols = list(df.columns)
if 'Empresa_usuario' not in cols or 'Empresa_empresa' not in cols:
    raise ValueError(f"Colunas 'Empresa_usuario' ou 'Empresa_empresa' não encontradas. Colunas disponíveis: {cols}")

empresas = {}
for idx, row in df.iterrows():
    empresa_nome = row['Empresa_empresa']
    empresa, created = Empresa.objects.get_or_create(
        empresa=empresa_nome,
        defaults={
            'endereco_rua': row['Endereço - Rua'],
            'endereco_numero': row['Endereço - Numero'],
            'endereco_estado': row['Endereço - Estado'],
            'endereco_cidade': row['Endereço - Cidade'],
            'endereco_cep': row['Endereço - CEP'],
            'razao_social': row['Razão Social'],
            'cnpj': row['CNPJ'],
            'distribuidora': row['Distribuidora'],
            'modalidade_tarifaria': row['Modalidade Tarifária'],
            'consumo_ponta_kwh': row['Consumo Ponta (kWh)'] or None,
            'consumo_fora_ponta_kwh': row['Consumo Fora Ponta (kWh)'] or None,
            'valor_medio_fatura': row['Valor Médio da Fatura (R$)'] or None,
        }
    )
    empresas[empresa.empresa] = empresa

for idx, row in df.iterrows():
    empresa_nome_usuario = row['Empresa_usuario']
    empresa_usuario = empresas.get(empresa_nome_usuario)
    email = row['e-mail']
    if not email:
        continue
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'identificador': row['Identificador'],
            'first_name': row['Nome'],
            'cargo': row['Cargo'],
            'empresa': empresa_usuario,
            'telefone': row['Telefone'],
            'is_gestor': False
        }
    )

for idx, row in df.iterrows():
    empresa_nome = row['Empresa_empresa']
    gestor_nome = row['Gestor Responsável (LUX)']
    empresa = empresas.get(empresa_nome)
    if empresa and gestor_nome:
        gestor = User.objects.filter(first_name=gestor_nome).first()
        if gestor:
            empresa.gestor_responsavel_fk = gestor
            empresa.save()
            gestor.is_gestor = True
            gestor.save()

print("Importação concluída com sucesso!")
