import pytest
from django.utils import timezone
from gastos.models import Tarefa


@pytest.mark.django_db
def test_criar_tarefa():
    """Testa a criação de uma tarefa com campos obrigatórios."""
    tarefa = Tarefa.objects.create(
        titulo="Estudar para a prova",
        prioridade="urgente",
        categoria="Faculdade",
        data_prazo=timezone.now().date(),
    )
    assert tarefa.pk is not None
    assert tarefa.titulo == "Estudar para a prova"
    assert tarefa.prioridade == "urgente"
    assert tarefa.categoria == "Faculdade"
    assert tarefa.concluida is False


@pytest.mark.django_db
def test_str_tarefa():
    """Testa a representação em string de uma tarefa."""
    tarefa = Tarefa(titulo="Entregar relatório", prioridade="pode_esperar")
    assert "Entregar relatório" in str(tarefa)
    assert "Pode Esperar" in str(tarefa)


@pytest.mark.django_db
def test_listagem_tarefas():
    """Testa a listagem de tarefas cadastradas."""
    Tarefa.objects.create(titulo="Ler livro", prioridade="sem_urgencia", categoria="Estudo")
    Tarefa.objects.create(titulo="Reunião de equipe", prioridade="urgente", categoria="Trabalho")

    tarefas = Tarefa.objects.all()
    assert tarefas.count() == 2


@pytest.mark.django_db
def test_tarefa_concluida_padrao_false():
    """Testa que uma tarefa nova começa como não concluída."""
    tarefa = Tarefa.objects.create(titulo="Nova tarefa", prioridade="sem_urgencia", categoria="Pessoal")
    assert tarefa.concluida is False


@pytest.mark.django_db
def test_categoria_livre():
    """Testa que a categoria aceita valor livre digitado pelo usuário."""
    tarefa = Tarefa.objects.create(titulo="Reunião", prioridade="urgente", categoria="Minha Categoria Personalizada")
    assert tarefa.categoria == "Minha Categoria Personalizada"


@pytest.mark.django_db
def test_remocao_tarefa():
    """Testa que uma tarefa pode ser removida corretamente."""
    tarefa = Tarefa.objects.create(titulo="Deletar depois", prioridade="sem_urgencia", categoria="Outros")
    pk = tarefa.pk
    tarefa.delete()
    assert Tarefa.objects.filter(pk=pk).count() == 0
