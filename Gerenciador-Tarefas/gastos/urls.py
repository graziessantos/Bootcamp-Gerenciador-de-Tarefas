"""URLs do app de gastos."""

from django.urls import path

from . import views

app_name = "gastos"

urlpatterns = [
    path("", views.index, name="index"),
    path("adicionar/", views.adicionar, name="adicionar"),
    path("editar/<int:pk>/", views.editar, name="editar"),
    path("excluir/<int:pk>/", views.excluir, name="excluir"),
]
