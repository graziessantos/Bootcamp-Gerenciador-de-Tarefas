"""Views do app de tarefas."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TarefaForm
from .models import PRIORIDADES, Tarefa
from .services import verificar_feriados_em_tarefas


def index(request):
    """Lista todas as tarefas com filtro por prioridade."""
    tarefas = Tarefa.objects.all()

    # Filtro por prioridade (opcional)
    prioridade_filtro = request.GET.get("prioridade", "")
    if prioridade_filtro:
        tarefas = tarefas.filter(prioridade=prioridade_filtro)

    # Contagem por prioridade
    resumo = []
    for cod, nome in PRIORIDADES:
        contagem = Tarefa.objects.filter(prioridade=cod).count()
        resumo.append({"cod": cod, "nome": nome, "contagem": contagem})

    total = Tarefa.objects.count()
    pendentes = Tarefa.objects.filter(concluida=False).count()
    alertas_feriado = verificar_feriados_em_tarefas(tarefas)

    context = {
        "tarefas": tarefas,
        "total": total,
        "pendentes": pendentes,
        "resumo": resumo,
        "prioridades": PRIORIDADES,
        "prioridade_filtro": prioridade_filtro,
        "mes_atual": timezone.now().strftime("%B de %Y"),
        "alertas_feriado": alertas_feriado,
    }
    return render(request, "gastos/index.html", context)


def adicionar(request):
    """Adiciona uma nova tarefa."""
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa adicionada com sucesso!")
            return redirect("gastos:index")
    else:
        form = TarefaForm(initial={"data_prazo": timezone.now().date()})

    return render(request, "gastos/tarefa_form.html", {"form": form, "titulo": "Adicionar Tarefa"})


def editar(request, pk):
    """Edita uma tarefa existente."""
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, "Tarefa atualizada com sucesso!")
            return redirect("gastos:index")
    else:
        form = TarefaForm(instance=tarefa)

    return render(request, "gastos/tarefa_form.html", {"form": form, "titulo": "Editar Tarefa"})


def excluir(request, pk):
    """Exclui uma tarefa."""
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        tarefa.delete()
        messages.success(request, "Tarefa removida com sucesso!")
        return redirect("gastos:index")

    return render(request, "gastos/confirmar_exclusao.html", {"tarefa": tarefa})
