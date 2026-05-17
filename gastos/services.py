"""Serviço de integração com a BrasilAPI para consulta de feriados nacionais."""

import urllib.request
import json
from datetime import date


BRASILAPI_URL = "https://brasilapi.com.br/api/feriados/v1/{ano}"


def buscar_feriados(ano: int) -> list[dict]:
    url = BRASILAPI_URL.format(ano=ano)
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data if isinstance(data, list) else []
    except Exception:
        return []


def verificar_feriado(data_alvo: date) -> dict | None:
    feriados = buscar_feriados(data_alvo.year)
    data_str = data_alvo.strftime("%Y-%m-%d")
    for feriado in feriados:
        if feriado.get("date") == data_str:
            return feriado
    return None


def verificar_feriados_em_tarefas(tarefas) -> dict[int, dict]:
    anos_necessarios: set[int] = set()
    for tarefa in tarefas:
        if tarefa.data_prazo:
            anos_necessarios.add(tarefa.data_prazo.year)

    cache_feriados: dict[int, list[dict]] = {}
    for ano in anos_necessarios:
        cache_feriados[ano] = buscar_feriados(ano)

    alertas: dict[int, dict] = {}
    for tarefa in tarefas:
        if tarefa.data_prazo:
            feriados_do_ano = cache_feriados.get(tarefa.data_prazo.year, [])
            data_str = tarefa.data_prazo.strftime("%Y-%m-%d")
            for feriado in feriados_do_ano:
                if feriado.get("date") == data_str:
                    alertas[tarefa.pk] = feriado
                    break

    return alertas