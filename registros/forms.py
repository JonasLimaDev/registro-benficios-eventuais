from django import forms
from datetime import date
from registros.models import Bairro, Beneficio,Orgao,TipoEntrega
from registros.validation import *

class FormBeneficiado(forms.Form):

    nome = forms.CharField(label='Nome do Beneficiado', max_length=200)
    nome.widget.attrs = {'class':'form-control','placeholder':nome.label}

    cpf = forms.CharField(label='CPF', max_length=11,required=False)
    cpf.widget.attrs = {'class':'form-control','placeholder':cpf.label}
    
    rg = forms.CharField(label="RG",max_length=20,required=False)
    rg.widget.attrs = {'class':'form-control','placeholder':rg.label}

    data_nascimento = forms.DateField(label="Data de Nascimento",required=False)
    data_nascimento.widget = forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': data_nascimento.label,
                       'type': 'date',
                       'value':'data_nascimento'
                       })
    

    contato = forms.CharField(label='Número Para Contato', max_length=200,help_text="Exemplo: Nº 2937, Lote 22.",required=False)
    contato.widget.attrs = {'class':'form-control','placeholder':contato.label}
    
    endereco = forms.CharField(label='Endereço', max_length=200, required=False)
    endereco.widget.attrs = {'class':'form-control','placeholder':endereco.label}
    
    numero = forms.CharField(label='Número', max_length=200,help_text="Exemplo: Nº 2937, Lote 22.",required=False)
    numero.widget.attrs = {'class':'form-control','placeholder':endereco.label}
    
    bairro = forms.ModelChoiceField(label='Bairro',queryset=Bairro.objects.all())
    bairro.widget.attrs = {'class':'form-control','placeholder':bairro.label}



    complemento = forms.CharField(label='Complemento', max_length=200,required=False)
    complemento.widget.attrs = {'class':'form-control','placeholder':complemento.label}

    def clean(self):
        nome = self.cleaned_data["nome"]
        cpf = self.cleaned_data["cpf"]
        rg = self.cleaned_data["rg"]
        data_nascimento = self.cleaned_data["data_nascimento"]
        contato = self.cleaned_data["contato"]
        endereco = self.cleaned_data["endereco"]
        numero = self.cleaned_data["numero"]
        bairro = self.cleaned_data["bairro"]
        complemento = self.cleaned_data["complemento"]
        lista_erros = {}
        if nome == 'zé':
            self.add_error('nome', "aí não zé")
        if cpf != "":
            validar_cpf(cpf,lista_erros)
        beneficiado_existe(cpf,lista_erros)
        if lista_erros is not None:
            for erro  in lista_erros:
                mensagem = lista_erros[erro]
                self.add_error(erro, mensagem)

        return self.cleaned_data  




class FormRegistro(forms.Form):
    status = (('1','Entregue ao Usuário'),('2','Entregue no Orgão'), ('3','Orgão Externo'))
    data_entrega = forms.DateField(label="Data da Entrega")
    data_entrega.widget = forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       'value':'data_entrega'
                       })

    tipo_beneficio = forms.ModelChoiceField(label="Tipo de benefício",required=True,queryset=Beneficio.objects.all())
    tipo_beneficio.widget.attrs = {'class':'form-control','placeholder':tipo_beneficio.label}

    orgao_responsavel = forms.ModelChoiceField(label="Orgão Responsável",required=True,queryset=Orgao.objects.all())
    orgao_responsavel.widget.attrs = {'class':'form-control','placeholder':orgao_responsavel.label}
    
    quantidade = forms.IntegerField(label='Quantidade',required=True,min_value=1)
    quantidade.widget.attrs = {'class':'form-control','placeholder':quantidade.label,'min':1,'default':1}

    status = forms.ChoiceField(label="Situação de Entrega",required=True,choices=status)
    status = forms.ModelChoiceField(label="Tipo de Entrega",required=True,queryset=TipoEntrega.objects.all())
    
    status.widget.attrs = {'class':'form-control','placeholder':status.label}
    def clean(self):
        quantidade = self.cleaned_data['quantidade']
        data_entrega = self.cleaned_data['data_entrega']
        data_atual = date.today()

        if quantidade == 0:
            self.add_error('quantidade',"Não podemos registrar 0 entregas")
        if data_entrega > data_atual:
            self.add_error('data_entrega',"Não podemos registrar entregas do futuro")
        

    #status = models.CharField(max_length=1,choices=STATUS_REGISTRO, null=False,blank=False)

    #beneficiado = models.ForeignKey("Beneficiado",on_delete=models.PROTECT,null=True)

    