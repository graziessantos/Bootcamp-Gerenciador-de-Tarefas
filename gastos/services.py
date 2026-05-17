"""Serviço de integração com a TimeAPI para exibir horário de Brasília."""

import json
import urllib.request

TIMEAPI_URL = "https://timeapi.io/api/time/current/zone?timeZone=America/Sao_Paulo"


def buscar_horario_brasilia() -> dict | None:
    """
    Busca o horário atual de Brasília via TimeAPI.io.
    Retorna dict com os dados ou None em caso de erro.
    """
    try:
        with urllib.request.urlopen(TIMEAPI_URL, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None


def formatar_horario(dados: dict | None) -> str:
    """Formata o horário retornado pela API para exibição."""
    if not dados:
        return "Horário indisponível"
    hora = dados.get("time", "")
    data = dados.get("date", "")
    if not hora or not data:
        return "Horário indisponível"
    # Ex: date = "05/17/2026", time = "14:35"
    partes = data.split("/")
    if len(partes) == 3:
        mes, dia, ano = partes
        data_formatada = f"{dia}/{mes}/{ano}"
    else:
        data_formatada = data
    hora_formatada = hora[:5]
    return f"{data_formatada} às {hora_formatada}"
