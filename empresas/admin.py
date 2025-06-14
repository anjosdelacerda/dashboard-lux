from django.contrib import admin
from .models import Empresa, ResumoGerencial
from users.models import User
from django.urls import path
from django.shortcuts import render
from django.db.models import Avg, Sum, Max

class FuncionariosInline(admin.TabularInline):
    model = User
    fields = ("username","first_name","email", "cargo", "identificador")
    extra = 0
    readonly_fields = fields
    can_delete = False
    show_change_link = True

class EmpresaAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ("empresa", "razao_social", "distribuidora", "modalidade_tarifaria", "gestor_nome")
    search_fields = ("empresa", "cnpj", "distribuidora")
    readonly_fields = ("id",)
    inlines = [FuncionariosInline]

    def gestor_nome(self, obj):
        return obj.gestor_responsavel_fk.get_full_name() if obj.gestor_responsavel_fk else "—"
    gestor_nome.short_description = "Gestor Responsável"

    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "gestor_responsavel_fk":
            kwargs["queryset"] = User.objects.filter(is_gestor=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Empresa, EmpresaAdmin)

@admin.register(ResumoGerencial)
class ResumoGerencialAdmin(admin.ModelAdmin):
    change_list_template = 'admin/resumo_gerencial_change_list.html'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        estatisticas = ResumoGerencial.get_estatisticas()
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label, 
            **estatisticas
        }
        return render(request, self.change_list_template, context)