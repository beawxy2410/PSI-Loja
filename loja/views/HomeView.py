from django.shortcuts import render
from loja.models import Produto

def home_view(request):
    produto = request.GET.get("produto")
    produtos = Produto.objects.all()
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
    print(produto) # Conteúdo digitado pelo usuário
    print(produtos) # Produtos do banco de dados digitados pelo usuário
    context = {'produtos': produtos}
    return render(request, template_name='home/home.html', context=context, status=200)
    