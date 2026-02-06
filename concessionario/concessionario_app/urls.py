from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('<int:pk>/dettaglio_auto/', views.dettaglio_auto, name='dettaglio_auto'),
    path('<int:pk>/toggle_preferito/', views.toggle_preferito, name='toggle_preferito'),
    path('preferiti/', views.i_miei_preferiti, name='preferiti'),
    path('<int:pk>/acquista/', views.acquista_auto, name='acquista_auto'),
    path('ordini/', views.i_miei_ordini, name='ordini'),
    path('dashboard/', views.dashboard_vendite, name='dashboard_vendite'),
    path('crea_annuncio/', views.crea_annuncio, name='crea_annuncio'),
    path('<int:pk>/modifica_annuncio/', views.modifica_annuncio, name='modifica_annuncio'),
    path('<int:pk>/elimina_annuncio/', views.elimina_annuncio, name='elimina_annuncio'),
    path('dashboard/richieste/', views.richieste_info_dashboard, name='richieste_info_dashboard'),
    path('dashboard/richieste/<int:pk>/gestita/', views.segna_richiesta_gestita, name='segna_richiesta_gestita'
),

]