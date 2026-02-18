from django.shortcuts import render, get_object_or_404, redirect
from .models import Auto, Preferito, Ordine, RichiestaInfo
from accounts.models import Cliente
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import AcquistoForm, AutoForm, FiltriCatalogoForm,FotoAutoFormSet, RichiestaInfoForm
from django.contrib import messages
from .utils import ordina

# Create your views here.

def home(request):
    return render(request, 'concessionario_app/home.html')


def catalogo(request):
    form = FiltriCatalogoForm(request.GET or None)
    auto=Auto.objects.filter(disponibilita=True)

    auto_filtrate=auto
    

    if form.is_valid():
        if form.cleaned_data.get('marca'):
            auto_filtrate = auto_filtrate.filter(marca__icontains=form.cleaned_data['marca'])

        if form.cleaned_data.get('categoria'):
            auto_filtrate = auto_filtrate.filter(categoria=form.cleaned_data['categoria'])

        if form.cleaned_data.get('alimentazione'):
            auto_filtrate = auto_filtrate.filter(alimentazione=form.cleaned_data['alimentazione'])
            
        if form.cleaned_data.get('condizioni'):
            auto_filtrate = auto_filtrate.filter(condizioni=form.cleaned_data['condizioni'])
            
        if form.cleaned_data.get('prezzo_min'):
            auto_filtrate = auto_filtrate.filter(prezzo__gte=form.cleaned_data['prezzo_min'])
            
        if form.cleaned_data.get('prezzo_max'):
            auto_filtrate = auto_filtrate.filter(prezzo__lte=form.cleaned_data['prezzo_max'])
    
    current_order = request.GET.get("order", "recent")
    nuove, order_label, next_order = ordina(auto_filtrate, current_order)          

    preferite = (auto.annotate(num_preferiti=Count('preferito')).filter(num_preferiti__gt=0).order_by('-num_preferiti')[:10])


    preferiti_ids=[]
    if request.user.is_authenticated and hasattr(request.user, 'cliente'):
        preferiti_ids = Preferito.objects.filter(cliente=request.user.cliente).values_list('auto_id', flat=True)
    context = {'form': form, 'preferite': preferite, 'nuove': nuove, 'preferiti_ids': preferiti_ids, 'order_label': order_label, 'next_order':next_order}

    return render(request, 'concessionario_app/catalogo.html', context)

def dettaglio_auto(request, pk):
    auto = get_object_or_404(Auto, pk=pk)
    fields = auto._meta.fields
    excludes = ['id', 'created_by', 'prezzo', 'video', 'descrizione', 'marca', 'modello']
    specs = [
        f for f in auto._meta.fields
        if f.name not in excludes
    ]

    is_preferito = False
    if request.user.is_authenticated and hasattr(request.user, 'cliente'):
        is_preferito = Preferito.objects.filter(cliente=request.user.cliente, auto=auto).exists()

    if request.method == 'POST':
        form = RichiestaInfoForm(request.POST)
        if form.is_valid():
            richiesta = form.save(commit=False)
            richiesta.auto = auto
            richiesta.save()

            messages.success(request, "Richiesta inviata con successo!")
            return redirect('dettaglio_auto', pk=auto.pk)
        else:
            messages.error(request, "Errore durante l'invio")
    else:
        form = RichiestaInfoForm(initial={
            'messaggio': f"Sono interessato all'auto {auto}"
        })

        context = {
            'auto': auto,
            'fields': fields,
            'is_preferito': is_preferito,
            'form': form,
            'specs': specs,
        }
    return render(request, 'concessionario_app/dettaglio_auto.html', context)

@login_required(login_url='/accounts/login/')
def toggle_preferito(request, pk):
    if not hasattr(request.user, 'cliente'):
        return redirect('catalogo')

    auto = get_object_or_404(Auto, pk=pk)
    cliente = request.user.cliente
    preferito, creato = Preferito.objects.get_or_create(cliente=cliente, auto=auto)
    
    if not creato:
        preferito.delete()

    return redirect(request.META.get('HTTP_REFERER', 'catalogo'))


@login_required(login_url='/accounts/login/')
def i_miei_preferiti(request):
    cliente = request.user.cliente
    preferiti = Preferito.objects.filter(cliente=cliente)
    
    return render(request, 'concessionario_app/preferiti.html', {'preferiti': preferiti})


@login_required(login_url='/accounts/login/')
def acquista_auto(request, pk):
    if not hasattr(request.user, 'cliente'):
        messages.error(request, "Solo i clienti possono acquistare auto.")
        return redirect('catalogo')
    auto = get_object_or_404(Auto, pk=pk)
    cliente = request.user.cliente
    if request.method == 'POST':
        form = AcquistoForm(request.POST)
        if form.is_valid():
            if auto.disponibilita:
                Ordine.objects.create(
                    cliente = cliente,
                    auto = auto,
                    prezzo = auto.prezzo,
                    pagamento = form.cleaned_data['metodo_pagamento'],
                    indirizzo_consegna =form.cleaned_data['indirizzo_consegna'],
                )
                auto.disponibilita=False
                auto.save()

                messages.success(request, "Ordine effettuato con successo!")
                return redirect('dettaglio_auto', pk=pk)
            else:
                messages.error(request, "Spiacenti, l'auto non è disponibile.")
                return redirect('dettaglio_auto', pk=pk)

    else:
        form = AcquistoForm()
    return render(request, "concessionario_app/acquisto.html", {'form':form, 'auto':auto})


@login_required(login_url='/accounts/login/')
def i_miei_ordini(request):
    if not hasattr(request.user, 'cliente'):
        messages.error(request, 'Solo i clienti possono vedere gli ordini.')
        return redirect('catalogo')
    
    cliente = request.user.cliente
    ordini = Ordine.objects.filter(cliente=cliente).order_by('-data_acquisto')
    

    return render(request, 'concessionario_app/i_miei_ordini.html', {'ordini': ordini})


@login_required(login_url='/accounts/login/')
def dashboard_vendite(request):
    if not hasattr(request.user, 'venditore'):
        messages.error(request, "Solo i venditori possono accedere a questa sezione.")
        return redirect('catalogo')
    
    auto = Auto.objects.all()

    totale=auto.count()
    disponibili = auto.filter(disponibilita=True).count()
    vendute = auto.filter(disponibilita=False).count()
    non_gestite = RichiestaInfo.objects.filter(gestita=False).count()

    context={
        'auto': auto,
        'totale': totale,
        'disponibili': disponibili,
        'vendute': vendute,
        'non_gestite': non_gestite,
    }

    return render(request, 'concessionario_app/dashboard_vendite.html', context)


@login_required(login_url='/accounts/login/')
def crea_annuncio(request):
    if not hasattr(request.user, 'venditore'):
        messages.error(request, "Solo i venditori possono accedere a questa sezione.")
        return redirect('catalogo')
    
    if request.method == 'POST':
        form = AutoForm(request.POST, request.FILES)
        if form.is_valid():
            auto = form.save(commit=False)
            auto.created_by = request.user.venditore
            auto.save()
            
            formset = FotoAutoFormSet(request.POST, request.FILES, instance=auto)
            
            if formset.is_valid():
                formset.save()
                messages.success(request, "Annuncio creato con successo!")
                return redirect('dashboard_vendite')
            else:
                auto.delete()
    else:
        form = AutoForm()
        formset = FotoAutoFormSet()
    
    return render(request, 'concessionario_app/crea_annuncio.html', {'form': form, 'formset': formset})

@login_required(login_url='/accounts/login/')
def modifica_annuncio(request, pk):
    if not hasattr(request.user, 'venditore'):
        messages.error(request, "Solo i venditori possono accedere a questa sezione.")
        return redirect('catalogo')
    
    auto = get_object_or_404(Auto, pk=pk)

    if request.method == 'POST':
        form = AutoForm(request.POST, request.FILES, instance=auto)
        formset = FotoAutoFormSet(request.POST, request.FILES, instance=auto)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Annuncio modificato!")
            return redirect('dashboard_vendite')
    else:
        form = AutoForm(instance=auto)
        formset = FotoAutoFormSet(instance=auto)

    return render(request, 'concessionario_app/modifica_annuncio.html', {'form': form, 'formset': formset})

@login_required(login_url='/accounts/login/')
def elimina_annuncio(request, pk):
    if not hasattr(request.user, 'venditore'):
        messages.error(request, "Solo i venditori possono accedere a questa sezione.")
        return redirect('catalogo')
    
    auto = get_object_or_404(Auto, pk=pk)
    if request.method == 'POST':
        auto.delete()
        messages.success(request, "Annuncio eliminato!")
        return redirect('dashboard_vendite')
    return render(request, 'concessionario_app/elimina_annuncio.html', {'auto': auto})

@login_required(login_url='/accounts/login/')
def richieste_info_dashboard(request):
    if not hasattr(request.user, 'venditore'):
        messages.error(request, "Solo i venditori possono accedere a questa sezione.")
        return redirect('catalogo')
    
    richieste = RichiestaInfo.objects.all().order_by('-created_at')

    return render(
        request,
        'concessionario_app/richieste_info_dashboard.html',
        {'richieste': richieste}
    )

@login_required(login_url='/accounts/login/')
def segna_richiesta_gestita(request, pk):
    if not hasattr(request.user, 'venditore'):
        messages.error(request, "Accesso non autorizzato")
        return redirect('catalogo')

    richiesta = get_object_or_404(RichiestaInfo, pk=pk)
    richiesta.gestita = True
    richiesta.save()

    messages.success(request, "Richiesta segnata come gestita")
    return redirect('richieste_info_dashboard')
