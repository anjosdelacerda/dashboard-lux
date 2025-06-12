import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from empresas.models import Empresa

class IdentificadorChoices(models.TextChoices):
    CLIENTE = 'Cliente', 'Cliente'
    COLABORADOR_LUX = 'Colaborador Lux', 'Colaborador Lux'

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identificador = models.CharField(max_length=20, choices=IdentificadorChoices.choices)
    cargo = models.CharField(max_length=150, blank=True, null=True)
    empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_gestor = models.BooleanField(default=False)

    @staticmethod
    def generate_unique_username():
        return f"user_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def generate_random_password():
        return uuid.uuid4().hex

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_unique_username()
        if not self.password:
            generated_password = self.generate_random_password()
            self.password = make_password(generated_password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.first_name or self.username

    
    
