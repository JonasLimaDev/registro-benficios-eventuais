from registros.models import Registro


class RegistroIndividual():
    
    def __init__(self,Beneficiado):
        self.id = Beneficiado.id
        self.nome = Beneficiado.nome_beneficiado
        self.endereco = Beneficiado.endereco
        self.bairro = Beneficiado.bairro
        self.registros = self.beneficios(Beneficiado)

    def beneficios(self,Beneficiado):
        registros = Registro.objects.filter(beneficiado=Beneficiado).all().order_by('-data_entrega')
        return registros


class RegistroIndividualQuantitativos():
    
    def __init__(self,Beneficiado):
        self.id = Beneficiado.id
        self.nome = Beneficiado.nome_beneficiado
        self.bairro = Beneficiado.bairro
        self.total = self.total_entregas(Beneficiado)
        self.ultima_entrega = self.beneficios(Beneficiado)[0].data_entrega
        
    def beneficios(self,Beneficiado):
        registros = Registro.objects.filter(beneficiado=Beneficiado).all().order_by('-data_entrega')
        return registros

    def total_entregas(self,Beneficiado):
        registros = Registro.objects.filter(beneficiado=Beneficiado).all()
        total = 0;
        for registro in registros:
            total += registro.quantidade
        return total

