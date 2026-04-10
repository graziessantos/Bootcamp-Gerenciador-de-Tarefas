"""Migration inicial — cria a tabela Tarefa."""

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tarefa",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=200, verbose_name="Título")),
                (
                    "descricao",
                    models.TextField(blank=True, default="", verbose_name="Descrição"),
                ),
                (
                    "prioridade",
                    models.CharField(
                        choices=[
                            ("urgente", "🔴 Urgente"),
                            ("pode_esperar", "🟡 Pode Esperar"),
                            ("sem_urgencia", "🟢 Sem Urgência"),
                        ],
                        default="sem_urgencia",
                        max_length=20,
                        verbose_name="Prioridade",
                    ),
                ),
                (
                    "categoria",
                    models.CharField(
                        default="Geral",
                        help_text="Ex: Estudo, Trabalho, Faculdade, Escola, Pessoal...",
                        max_length=100,
                        verbose_name="Categoria",
                    ),
                ),
                (
                    "data_prazo",
                    models.DateField(blank=True, null=True, verbose_name="Data Prazo"),
                ),
                (
                    "concluida",
                    models.BooleanField(default=False, verbose_name="Concluída"),
                ),
                (
                    "criado_em",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
            ],
            options={
                "verbose_name": "Tarefa",
                "verbose_name_plural": "Tarefas",
                "ordering": ["concluida", "prioridade", "-criado_em"],
            },
        ),
    ]
