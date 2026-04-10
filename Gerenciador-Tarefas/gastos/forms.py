"""Formulários do app de tarefas."""

from django import forms

from .models import Tarefa


class TarefaForm(forms.ModelForm):
    """Formulário para criação e edição de tarefas."""

    # Categoria como campo de texto livre; sugestões fornecidas via datalist no template
    categoria = forms.CharField(
        label="Categoria",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Estudo, Trabalho, Faculdade...",
                "list": "sugestoes-categoria",
            }
        ),
    )

    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "prioridade", "categoria", "data_prazo", "concluida"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: Estudar para a prova..."}
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Detalhes da tarefa (opcional)",
                }
            ),
            # prioridade é renderizado manualmente no template como botões visuais;
            # o HiddenInput aqui garante que o Django não renderize um widget padrão
            # duplicado, enquanto o valor ainda é enviado pelo radio manual do template.
            "prioridade": forms.HiddenInput(),
            "data_prazo": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "concluida": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get("titulo", "").strip()
        if not titulo:
            raise forms.ValidationError("O título não pode estar vazio.")
        return titulo

    def clean_categoria(self):
        categoria = self.cleaned_data.get("categoria", "").strip()
        if not categoria:
            raise forms.ValidationError("A categoria não pode estar vazia.")
        return categoria

    def clean_prioridade(self):
        prioridade = self.cleaned_data.get("prioridade", "").strip()
        valores_validos = ["urgente", "pode_esperar", "sem_urgencia"]
        if prioridade not in valores_validos:
            raise forms.ValidationError("Selecione uma prioridade válida.")
        return prioridade
