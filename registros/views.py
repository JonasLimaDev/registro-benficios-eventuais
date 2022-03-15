from django.shortcuts import render, redirect
from registros.forms import FormBeneficiado,FormRegistro
from registros.models import Beneficiado
from .entidades.registros import RegistroIndividual,RegistroIndividualQuantitativos
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from registros.services import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
# Create your views here.
# some_app/views.py


class HomeView(TemplateView):
    template_name = "base.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class RegistrosFiltroView(TemplateView):
    
    template_name = "registros/registro_por_beneficiado.html"
    
    def get(self, request, *args, **kwargs):
        lista_beneficiados = Beneficiado.objects.all()
        self.id = self.get_pk_key(request)
        if self.id:
            baneficiado = get_object_or_404(Beneficiado, id=self.id)
            registro = RegistroIndividual(baneficiado)
            return render(request,self.template_name,{'registro':registro,'lista_beneficiados':lista_beneficiados})
    
        else:
            return render(request,self.template_name,{'lista_beneficiados':lista_beneficiados})
       
    
    def post(self,request , **kwargs):
        
        lista_beneficiados = Beneficiado.objects.all()
        baneficiado = Beneficiado.objects.get(nome_beneficiado=request.POST['beneficiado'])
        registro = RegistroIndividual(baneficiado)
        return render(request,self.template_name,{'registro':registro,'lista_beneficiados':lista_beneficiados})
    
    def get_pk_key(self,reuest, **kwargs):
        try:
            return self.kwargs['pk']
        except:
            return None


class RegistrarView(TemplateView):
    form_class = FormBeneficiado
    form2_class = FormRegistro
    template_name = "registros/formularios/registro_completo.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form2 = self.form2_class()

        return render(request,self.template_name,{'form':form,'form2':form2})
    
    
    def post(self, request, *args, **kwargs):
        form_beneficiado = self.form_class(request.POST)
        form_beneficio = self.form2_class(request.POST)
        if form_beneficiado.is_valid():
            if form_beneficio.is_valid():
                beneficiado_novo = salvar_dados_beneficiado(form_beneficiado)
                registro_bd = salvar_dados_registro(form_beneficio,beneficiado_novo)
                registro_bd.responsavel_registro=self.request.user
                registro_bd.save()
                return redirect("registros_filtro",beneficiado_novo.id)
        
        return render(request,self.template_name,{'form':form_beneficiado,'form2':form_beneficio})


class BeneficiadoDadoslView(TemplateView):
    
    template_name = "registros/dados_beneficiado.html"

    def get(self, request, *args, **kwargs):
        beneficiado = get_object_or_404(Beneficiado, id=self.kwargs['pk'])
        idade_beneficiado = calcula_idade(beneficiado.data_nascimento)
        return render(request,self.template_name,{'beneficiado':beneficiado,'idade_beneficiado':idade_beneficiado})


class BeneficiadoEditView(TemplateView):
    
    template_name = "registros/formlarios/editar_beneficiado.html"
    form_class = FormBeneficiado
    
    def get(self, request, *args, **kwargs):
        beneficiado = get_object_or_404(Beneficiado, id=self.kwargs['pk'])
        form = self.form_class(initial={'nome':beneficiado.nome_beneficiado, 'cpf':beneficiado.cpf, 'rg':beneficiado.rg,
        'data_nascimento':beneficiado.data_nascimento, 'contato':beneficiado.contato, 'endereco':beneficiado.endereco,
        'numero':beneficiado.numero_residencia, 'bairro':beneficiado.bairro, 'complemento':beneficiado.complemento} )
        return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        form  = self.form_class(request.POST)
        if form.is_valid():
            beneficiado = get_object_or_404(Beneficiado, id=self.kwargs['pk'])
            beneficiado_update = alterar_dados_beneficiado(form,beneficiado)
            return redirect("registros_filtro",beneficiado_update.id)

        return render(request,self.template_name,{'form':form})



class AdicionarRegistroView(TemplateView):
    
    template_name = "registros/formularios/adicionar_registro.html"
    form_class = FormRegistro
    
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        beneficiado = get_object_or_404(Beneficiado, id=self.kwargs['pk'])
        form_beneficio = self.form_class()
        
        return render(request,self.template_name,{'form':form_beneficio,'beneficiado':beneficiado})

    def post(self, request, *args, **kwargs):
        form_beneficio  = self.form_class(request.POST)            
        if form_beneficio.is_valid():
            beneficiado_bd = get_object_or_404(Beneficiado, id=self.kwargs['pk'])
            registro_bd = salvar_dados_registro(form_beneficio,beneficiado_bd)
            registro_bd.responsavel_registro=self.request.user
            registro_bd.save()
            return redirect("registros_filtro",beneficiado_bd.id)
            
        return render(request,self.template_name,{'form':form_beneficio})


class TodosRegistrosView(TemplateView):
    
    template_name = "registros/todos_beneficiados.html"
    
 
    def get(self, request, *args, **kwargs):
        lista_beneficiados = Beneficiado.objects.all()
        todos_beneficiados = []
        for beneficiado in lista_beneficiados:
            todos_beneficiados.append(RegistroIndividualQuantitativos(beneficiado))
        return render(request,self.template_name,{'todos_beneficiados':todos_beneficiados})


class CriarUsusarioView(TemplateView):
    template_name = "usuarios/cadastro_usuario_form.html"
    form_class_usuario = UserCreationForm

    def get(self, request, *args, **kwargs):
        formUsuario =  self.form_class_usuario()
        return render(request,self.template_name,{'formUsuario':formUsuario})

    def post(self,request, *args, **kwargs):
        formUsuario = self.form_class_usuario(request.POST)
        
        if formUsuario.is_valid():
            print(formUsuario.cleaned_data['username'])
            formUsuario.save()
            user = User.objects.get(username= formUsuario.cleaned_data['username'])
            user.is_active = False
            user.save()
            sucesso=True
            return render(request,self.template_name,{'formUsuario':formUsuario,'sucesso':sucesso})
        return render(request,self.template_name,{'formUsuario':formUsuario})

class LoginView(TemplateView):
    template_name = "usuarios/login_usuario_form.html"
    form_class_logar = AuthenticationForm
    def get(self, request, *args, **kwargs):
        formUsuario =  self.form_class_logar()
        return render(request,self.template_name,{'form_login':formUsuario})

    def post(self,request, *args, **kwargs):
        
        pagina_destino = self.request.GET['next'] if 'next' in self.request.GET else 'home' 

        nome_usuario = request.POST["username"]
        senha = request.POST["password"]
        usuario = User.objects.all().filter(username=nome_usuario)
        if not usuario:
            messages.error(request, 'Usuario Não Cadastrado')
            return redirect('logar')
        elif not usuario[0].is_active:
            messages.error(request,'Usuario Cadastrado, Mas Não Autorizado')
            return redirect('logar')
        else:
            usuario = authenticate(request,username=nome_usuario, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect(pagina_destino)
        else:
            messages.error(request,'Senha Incorreta')
            return redirect('logar')
        


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('home')
