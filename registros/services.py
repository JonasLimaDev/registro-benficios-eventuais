
from registros.models import Beneficiado, Registro
from datetime import date

def salvar_dados_beneficiado(form):
    """Pega os dados do formulário de beneficiado e salva no banco de dados"""

    form_nome = form.cleaned_data["nome"]
    form_cpf = form.cleaned_data["cpf"] if form.cleaned_data["cpf"] != "" else None
    form_rg = form.cleaned_data["rg"] if form.cleaned_data["rg"] != "" else None
    form_data_nascimento = form.cleaned_data["data_nascimento"] if form.cleaned_data["data_nascimento"] != "" else None
    form_contato = form.cleaned_data["contato"] if form.cleaned_data["contato"] != "" else None
    form_endereco = form.cleaned_data["endereco"] if form.cleaned_data["endereco"] != "" else None
    form_numero = form.cleaned_data["numero"] if form.cleaned_data["numero"] != "" else None
    form_bairro = form.cleaned_data["bairro"]
    form_complemento = form.cleaned_data["complemento"] if form.cleaned_data["complemento"] != "" else None
    
    beneficiado = Beneficiado.objects.create(nome_beneficiado=form_nome,cpf=form_cpf,rg=form_rg,
        data_nascimento=form_data_nascimento,contato=form_contato, endereco=form_endereco, numero_residencia=form_numero, bairro=form_bairro, complemento=form_complemento)
    beneficiado.save()

    return beneficiado

def alterar_dados_beneficiado(form,beneficiado_bd):
    """Pega os dados do formulário de beneficiado e atualiza para o beneficiado passado no parâmetro"""
    beneficiado_bd.nome_beneficiado = form.cleaned_data["nome"]
    beneficiado_bd.cpf = form.cleaned_data["cpf"] if form.cleaned_data["cpf"] != "" else None
    beneficiado_bd.rg = form.cleaned_data["rg"] if form.cleaned_data["rg"] != "" else None
    beneficiado_bd.data_nascimento = form.cleaned_data["data_nascimento"] if form.cleaned_data["data_nascimento"] != "" else None
    beneficiado_bd.contato = form.cleaned_data["contato"] if form.cleaned_data["contato"] != "" else None
    beneficiado_bd.endereco = form.cleaned_data["endereco"] if form.cleaned_data["endereco"] != "" else None
    beneficiado_bd.numero_residencia = form.cleaned_data["numero"] if form.cleaned_data["numero"] != "" else None
    beneficiado_bd.bairro = form.cleaned_data["bairro"]
    beneficiado_bd.complemento = form.cleaned_data["complemento"] if form.cleaned_data["complemento"] != "" else None

    beneficiado_bd.save(force_update=True)
    
    return beneficiado_bd


def salvar_dados_registro(form,beneficiado_bd):
    """Pega os dados do formulário de registro e salva no banco de dados"""
    
    form_status = form.cleaned_data["status"]
    form_data_entrega = form.cleaned_data["data_entrega"]
    form_tipo_beneficio = form.cleaned_data["tipo_beneficio"]
    form_quantidade = form.cleaned_data["quantidade"]
    form_orgao_responsavel = form.cleaned_data["orgao_responsavel"]
    
    registro = Registro.objects.create(status=form_status, data_entrega=form_data_entrega, tipo_beneficio=form_tipo_beneficio,
        quantidade=form_quantidade, beneficiado=beneficiado_bd, orgao_responsavel=form_orgao_responsavel)
    registro.save()
    return registro

def calcula_idade(data_nascimento):
    if data_nascimento  is not None:
        data_atual = date.today()
        idade = int((data_atual-data_nascimento).days / 365.25)
    else:
        idade = None
    return idade

