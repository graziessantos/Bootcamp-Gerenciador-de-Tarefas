"""Views do app de tarefas."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TarefaForm
from .models import PRIORIDADES, Tarefa
from .services import buscar_horario_brasilia, formatar_horario


def index(request):
    """Lista todas as tarefas com filtro por prioridade."""
    tarefas = Tarefa.objects.all()

    prioridade_filtro = request.GET.get("prioridade", "")
    if prioridade_filtro:
        tarefas = tarefas.filter(prioridade=prioridade_filtro)

    resumo = []
    for cod, nome in PRIORIDADES:
        contagem = Tarefa.objects.filter(prioridade=cod).count()
        resumo.append({"cod": cod, "nome": nome, "contagem": contagem})

    total = Tarefa.objects.count()
    pendentes = Tarefa.objects.filter(concluida=False).count()

    dados_horario = buscar_horario_brasilia()
    horario_brasilia = formatar_horario(dados_horario)

    context = {
        "tarefas": tarefas,
        "total": total,
        "pendentes": pendentes,
        "resumo": resumo,
        "prioridades": PRIORIDADES,
        "prioridade_filtro": prioridade_filtro,
        "mes_atual": timezone.now().strftime("%B de %Y"),
        "horario_brasilia": horario_brasilia,
    }
    return render(request, "gastos/index.html", context)
