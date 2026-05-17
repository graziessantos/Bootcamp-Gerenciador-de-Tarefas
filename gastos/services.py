"""Serviço de integração com a WorldTimeAPI para exibir horário de Brasília."""

import urllib.request
import json


WORLDTIME_URL = "https://timeapi.io/api/time/current/zone?timeZone=America/Sao_Paulo"


def buscar_horario_brasilia() -> dict | None:
    """
    Busca o horário atual de Brasília via WorldTimeAPI.
    Retorna dict com os dados ou None em caso de erro.
    """
    try:
        with urllib.request.urlopen(WORLDTIME_URL, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None


def formatar_horario(dados: dict | None) -> str:
    """Formata o horário retornado pela API para exibição."""
    if not dados:
        return "Horário indisponível"
    datetime_str = dados.get("datetime", "")
    if not datetime_str:
        return "Horário indisponível"
    # Ex: "2026-05-17T14:35:10.123456-03:00" → "17/05/2026 às 14:35"
    data, hora = datetime_str[:10], datetime_str[11:16]
    ano, mes, dia = data.split("-")
    return f"{dia}/{mes}/{ano} às {hora}"
