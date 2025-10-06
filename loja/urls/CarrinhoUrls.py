from django.urls import path
from loja.views.CarrinhoView import create_carrinhoitem_view
urlpatterns = [
    path("<int:produto_id>", create_carrinhoitem_view, name='create_carrinhoitem'),
]