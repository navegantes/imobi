from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cidade, Imovel, Visitas


@login_required(login_url="/auth/logar")
def home(request):
    preco_minimo = request.GET.get('preco_minimo')  # get noma definido na tag input
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo')

    cidades = Cidade.objects.all()

    if (preco_minimo or preco_maximo or cidade or tipo):
        # define valores padrão
        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = float('inf')
        if not tipo:
            tipo = ['A', 'C']
        if not cidade:
            cidade = cidades

        imoveis = Imovel.objects.filter(valor__gte=preco_minimo).filter(
            valor__lte=preco_maximo).filter(tipo_imovel__in=tipo).filter(cidade__in=cidade)
    else:
        imoveis = Imovel.objects.all()

    request_data = {
        'imoveis': imoveis,
        'cidades': cidades
    }

    # return HttpResponse(imoveis)
    return render(request, 'home.html', request_data)


def imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)
    sugestoes = Imovel.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    user_visitas = Visitas.objects.filter(usuario=request.user)
    # get_FOO_display
    status = Visitas.objects.filter(imovel_id=id)[0].get_status_display

    visitas_id_lista = [elem.imovel.id for elem in user_visitas]
    # print("\n\n", Visitas._meta.get_field('status').choices, "\n\n")

    data_render = {
        'imovel': imovel,
        'sugestoes': sugestoes,
        'id_visitas': visitas_id_lista,
        'status': status
    }
    return render(request, 'imovel.html', data_render)


def agendar_visitas(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')

    visitas = Visitas(
        imovel_id=id_imovel,
        usuario=usuario,
        dia=dia,
        horario=horario
    )

    visitas.save()

    return redirect('/agendamentos')


def agendamentos(request):
    visitas = Visitas.objects.filter(usuario=request.user)
    return render(request, "agendamentos.html", {'visitas': visitas})


def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = "C"
    visitas.save()

    return redirect('/agendamentos')


# def get_status(request, id):
#     user_visitas = Visitas.objects.filter(usuario=request.user)
#     imovel_status = Visitas.objects.filter(imovel_id=id)[0].status
#     status_choices = Visitas._meta.get_field('status').choices

#     return [tup_status[1] for tup_status in status_choices if tup_status[0] == imovel_status][0]
