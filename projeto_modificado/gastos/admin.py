"""Configuração do admin para o app de tarefas."""

from django.contrib import admin

from .models import Tarefa


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "prioridade", "categoria", "data_prazo", "concluida", "criado_em"]
    list_filter = ["prioridade", "concluida", "categoria"]
    search_fields = ["titulo", "descricao", "categoria"]
    date_hierarchy = "data_prazo"
