from .models import Beneficiado

def beneficiado_existe(cpf_beneficiado,lista_erros):
    beneficiado_bd = Beneficiado.objects.filter(cpf=cpf_beneficiado)
    print(beneficiado_bd)
    if beneficiado_bd:
        lista_erros["cpf"]="Beneficiado com este CPF já existe"
    return lista_erros


def gerar_digito(sequencia,peso_inicial):
    soma=0
    digito_verificador = 0
    for digito in sequencia:
        soma += int(digito)*peso_inicial
        peso_inicial+=1
    if soma % 11 != 10:
        digito_verificador = soma % 11
    return str(digito_verificador)


def validar_cpf(cpf,lista_erros):
    if len(cpf) == 11:
        digitos_cpf = cpf[9:11]
        digito_verificador1 = gerar_digito(cpf[0:9],1)
        sequencia = cpf[0:9]+digito_verificador1 
        digito_verificador2 = gerar_digito(sequencia,0)
        resultado = digito_verificador1+digito_verificador2
        if digitos_cpf != resultado:
            lista_erros['cpf'] = "CPF inválido verifique os dígitos e tente novamente"
    else:
        lista_erros['cpf'] = "CPF incompleto informe todos os 11 dígitos"


