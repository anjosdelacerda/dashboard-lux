import uuid
from django.db import models
from django.conf import settings

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.CharField(max_length=150, unique=True)
    endereco_rua = models.CharField(max_length=150)
    endereco_numero = models.CharField(max_length=150)
    endereco_estado = models.CharField(max_length=150)
    endereco_cidade = models.CharField(max_length=150)
    endereco_cep = models.CharField(max_length=150)
    razao_social = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=30, unique=True)
    distribuidora = models.CharField(max_length=150)
    modalidade_tarifaria = models.CharField(max_length=20)
    consumo_ponta_kwh = models.FloatField(null=True, blank=True)
    consumo_fora_ponta_kwh = models.FloatField(null=True, blank=True)
    valor_medio_fatura = models.FloatField(null=True, blank=True)

    gestor_responsavel_fk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empresas_geridas',
        db_column='gestor_responsavel_id'
    )

    def __str__(self):
        return self.empresa

    @property
    def colaboradores(self):
        return self.usuarios.all()
