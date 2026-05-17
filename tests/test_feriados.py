"""Testes de integração — BrasilAPI Feriados Nacionais."""

import json
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from gastos.models import Tarefa
from gastos.services import buscar_feriados, verificar_feriado, verificar_feriados_em_tarefas

FERIADOS_2025_MOCK = [
    {"date": "2025-01-01", "name": "Confraternização Mundial", "type": "national"},
    {"date": "2025-04-18", "name": "Sexta-Feira Santa", "type": "national"},
    {"date": "2025-04-21", "name": "Tiradentes", "type": "national"},
    {"date": "2025-05-01", "name": "Dia do Trabalhador", "type": "national"},
    {"date": "2025-09-07", "name": "Independência do Brasil", "type": "national"},
    {"date": "2025-10-12", "name": "Nossa Senhora Aparecida", "type": "national"},
    {"date": "2025-11-02", "name": "Finados", "type": "national"},
    {"date": "2025-11-15", "name": "Proclamação da República", "type": "national"},
    {"date": "2025-12-25", "name": "Natal", "type": "national"},
]


def _mock_urlopen(feriados: list[dict]):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(feriados).encode("utf-8")
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    return mock_response


class TestBuscarFeriados:
    @patch("urllib.request.urlopen")
    def test_retorna_lista_de_feriados(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        resultado = buscar_feriados(2025)
        assert isinstance(resultado, list)
        assert len(resultado) == 9

    @patch("urllib.request.urlopen")
    def test_feriados_possuem_campos_obrigatorios(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        feriados = buscar_feriados(2025)
        for f in feriados:
            assert "date" in f
            assert "name" in f
            assert "type" in f

    @patch("urllib.request.urlopen")
    def test_retorna_lista_vazia_em_caso_de_erro_de_rede(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Timeout")
        resultado = buscar_feriados(2025)
        assert resultado == []

    @patch("urllib.request.urlopen")
    def test_url_contem_ano_correto(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen([])
        buscar_feriados(2026)
        chamada_url = mock_urlopen.call_args[0][0]
        assert "2026" in chamada_url


class TestVerificarFeriado:
    @patch("urllib.request.urlopen")
    def test_detecta_natal_como_feriado(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        resultado = verificar_feriado(date(2025, 12, 25))
        assert resultado is not None
        assert resultado["name"] == "Natal"

    @patch("urllib.request.urlopen")
    def test_dia_comum_nao_e_feriado(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        resultado = verificar_feriado(date(2025, 6, 15))
        assert resultado is None

    @patch("urllib.request.urlopen")
    def test_independencia_e_feriado(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        resultado = verificar_feriado(date(2025, 9, 7))
        assert resultado is not None
        assert "Independência" in resultado["name"]


@pytest.mark.django_db
class TestVerificarFeriadosEmTarefas:
    @patch("urllib.request.urlopen")
    def test_tarefa_com_prazo_em_feriado_gera_alerta(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        tarefa = Tarefa.objects.create(
            titulo="Entregar relatório", prioridade="urgente",
            categoria="Trabalho", data_prazo=date(2025, 12, 25),
        )
        alertas = verificar_feriados_em_tarefas(Tarefa.objects.all())
        assert tarefa.pk in alertas
        assert alertas[tarefa.pk]["name"] == "Natal"

    @patch("urllib.request.urlopen")
    def test_tarefa_com_prazo_normal_nao_gera_alerta(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        tarefa = Tarefa.objects.create(
            titulo="Estudar Python", prioridade="sem_urgencia",
            categoria="Estudo", data_prazo=date(2025, 6, 15),
        )
        alertas = verificar_feriados_em_tarefas(Tarefa.objects.all())
        assert tarefa.pk not in alertas

    @patch("urllib.request.urlopen")
    def test_tarefa_sem_prazo_ignorada(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        tarefa = Tarefa.objects.create(
            titulo="Revisar documentos", prioridade="pode_esperar",
            categoria="Pessoal", data_prazo=None,
        )
        alertas = verificar_feriados_em_tarefas(Tarefa.objects.all())
        assert tarefa.pk not in alertas

    @patch("urllib.request.urlopen")
    def test_multiplas_tarefas_feriado_e_dia_comum(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(FERIADOS_2025_MOCK)
        t_feriado = Tarefa.objects.create(
            titulo="Tarefa no feriado", prioridade="urgente",
            categoria="Trabalho", data_prazo=date(2025, 5, 1),
        )
        t_normal = Tarefa.objects.create(
            titulo="Tarefa normal", prioridade="sem_urgencia",
            categoria="Pessoal", data_prazo=date(2025, 5, 10),
        )
        alertas = verificar_feriados_em_tarefas(Tarefa.objects.all())
        assert t_feriado.pk in alertas
        assert t_normal.pk not in alertas
        
