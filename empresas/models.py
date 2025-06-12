import uuid
from django.db import models
from django.conf import settings
from django.db.models import Count, Avg, Sum # Importe aqui para uso no método

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

class ResumoGerencial(Empresa):
    class Meta:
        proxy = True
        verbose_name = 'Resumo Gerencial'
        verbose_name_plural = 'Resumos Gerenciais'

    @classmethod
    def get_estatisticas(cls):
        from users.models import User
        from django.db.models import Count, Avg, Sum # Assegure-se que estão importados

        total_gestores = User.objects.filter(is_gestor=True).count()
        total_usuarios = User.objects.filter(is_gestor=False, is_superuser=False).count()

        # Adicione o tratamento para valores None
        # Use __iexact para ignorar maiúsculas/minúsculas no filtro
        verde_stats_raw = Empresa.objects.filter(modalidade_tarifaria__iexact='Verde').aggregate(
            media_consumo_ponta=Avg('consumo_ponta_kwh'),
            media_consumo_fora_ponta=Avg('consumo_fora_ponta_kwh'),
            media_valor_fatura=Avg('valor_medio_fatura')
        )
        verde_stats = {k: v if v is not None else 0 for k, v in verde_stats_raw.items()}

        azul_stats_raw = Empresa.objects.filter(modalidade_tarifaria__iexact='Azul').aggregate(
            media_consumo_ponta=Avg('consumo_ponta_kwh'),
            media_consumo_fora_ponta=Avg('consumo_fora_ponta_kwh'),
            media_valor_fatura=Avg('valor_medio_fatura')
        )
        azul_stats = {k: v if v is not None else 0 for k, v in azul_stats_raw.items()}

        estatisticas = {
            'total_empresas': Empresa.objects.count(),
            'total_usuarios': total_usuarios,
            'total_gestores': total_gestores,
            'media_usuarios_por_gestor': total_usuarios / max(1, total_gestores),
            'verde_stats': verde_stats,
            'azul_stats': azul_stats,
            'top5_valor_fatura': Empresa.objects.order_by('-valor_medio_fatura')[:5],
            'top5_consumo_ponta': Empresa.objects.order_by('-consumo_ponta_kwh')[:5],
            'top5_consumo_fora_ponta': Empresa.objects.order_by('-consumo_fora_ponta_kwh')[:5],
        }

        return estatisticas