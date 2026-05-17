"""Testes de integração — WorldTimeAPI Horário de Brasília."""

import json
from unittest.mock import MagicMock, patch

from gastos.services import buscar_horario_brasilia, formatar_horario


def _mock_urlopen(dados: dict):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(dados).encode("utf-8")
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    return mock_response


DADOS_MOCK = {
    "datetime": "2026-05-17T14:35:10.123456-03:00",
    "timezone": "America/Sao_Paulo",
    "utc_offset": "-03:00",
}


class TestBuscarHorarioBrasilia:
    @patch("urllib.request.urlopen")
    def test_retorna_dict_com_dados(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(DADOS_MOCK)
        resultado = buscar_horario_brasilia()
        assert isinstance(resultado, dict)
        assert "datetime" in resultado

    @patch("urllib.request.urlopen")
    def test_retorna_none_em_caso_de_erro(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Timeout")
        resultado = buscar_horario_brasilia()
        assert resultado is None

    @patch("urllib.request.urlopen")
    def test_url_contem_sao_paulo(self, mock_urlopen):
        mock_urlopen.return_value = _mock_urlopen(DADOS_MOCK)
        buscar_horario_brasilia()
        chamada_url = mock_urlopen.call_args[0][0]
        assert "Sao_Paulo" in chamada_url


class TestFormatarHorario:
    def test_formata_horario_corretamente(self):
        resultado = formatar_horario(DADOS_MOCK)
        assert resultado == "17/05/2026 às 14:35"

    def test_retorna_indisponivel_se_none(self):
        resultado = formatar_horario(None)
        assert resultado == "Horário indisponível"

    def test_retorna_indisponivel_se_sem_datetime(self):
        resultado = formatar_horario({"timezone": "America/Sao_Paulo"})
        assert resultado == "Horário indisponível"
