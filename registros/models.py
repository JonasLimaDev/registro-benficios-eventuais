from django.db import models

from django.contrib.auth.models import User
from datetime import datetime


class Bairro(models.Model):
    nome_bairro = models.CharField(max_length=60,null=False,blank=False)
    
    def __str__(self):
        return self.nome_bairro


class Beneficio(models.Model):
    beneficio = models.CharField(max_length=125,null=False,blank=False)
    tipo_beneficio = models.CharField(max_length=125,null=False,blank=False, default="Beneficio Eventual")
    
    def __str__(self):
        return self.beneficio


class Orgao(models.Model):
    nome = models.CharField(max_length=125,null=False,blank=False)
    resposavel = models.CharField(max_length=200,null=False,blank=False)

    def __str__(self):
        return self.nome


class Beneficiado(models.Model):
    nome_beneficiado = models.CharField(max_length=150,null=False,blank=False)
    cpf = models.CharField(max_length=11,null=True,blank=True)
    rg = models.CharField(max_length=20,null=True,blank=True)
    data_nascimento = models.DateField(null=True,blank=True)
    
    contato = models.CharField(max_length=11,null=True,blank=True)
    
    endereco = models.CharField(max_length=200,null=True,blank=True)
    numero_residencia = models.CharField(max_length=15,null=True,blank=True)
    bairro = models.ForeignKey("Bairro", on_delete=models.PROTECT)
    complemento = models.CharField(max_length=200,null=True,blank=True)

    # nome_beneficiado, cpf, rg, data_nascimento, contato, endereco, numero_residencia, bairro, complemento
    def __str__(self):
        return self.nome_beneficiado


class TipoEntrega(models.Model):
    entrega = models.CharField(max_length=125,null=False,blank=False,unique=True)
    def __str__(self):
        return self.entrega


class Registro(models.Model):

    status = models.ForeignKey("TipoEntrega", on_delete=models.PROTECT)
    data_entrega = models.DateField()
    tipo_beneficio = models.ForeignKey("Beneficio", on_delete=models.PROTECT)
    quantidade = models.IntegerField(null=False, blank=False,default=1) 

    beneficiado = models.ForeignKey("Beneficiado",on_delete=models.PROTECT,null=True)

    orgao_responsavel = models.ForeignKey("Orgao",on_delete=models.PROTECT,null=True)
    data_registro = models.DateField(null=False, blank=False,default=datetime.now)
    responsavel_registro = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # status, data_entrega, tipo_beneficio, quantidade, beneficiado, orgao_responsavel
    def __str__(self):
        return self.beneficiado.nome_beneficiado
