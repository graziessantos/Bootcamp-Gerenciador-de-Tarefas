"""Modelos do app de tarefas."""

from django.db import models

PRIORIDADES = [
    ("urgente", "🔴 Urgente"),
    ("pode_esperar", "🟡 Pode Esperar"),
    ("sem_urgencia", "🟢 Sem Urgência"),
]


class Tarefa(models.Model):
    """Representa uma tarefa pessoal ou profissional."""

    titulo = models.CharField("Título", max_length=200)
    descricao = models.TextField("Descrição", blank=True, default="")
    prioridade = models.CharField(
        "Prioridade",
        max_length=20,
        choices=PRIORIDADES,
        default="sem_urgencia",
    )
    categoria = models.CharField(
        "Categoria",
        max_length=100,
        default="Geral",
        help_text="Ex: Estudo, Trabalho, Faculdade, Escola, Pessoal...",
    )
    data_prazo = models.DateField("Data Prazo", null=True, blank=True)
    concluida = models.BooleanField("Concluída", default=False)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        ordering = ["concluida", "prioridade", "-criado_em"]
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def __str__(self):
        return f"{self.titulo} [{self.get_prioridade_display()}]"

    def get_prioridade_label(self):
        return dict(PRIORIDADES).get(self.prioridade, self.prioridade)
