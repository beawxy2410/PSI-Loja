from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Produto, Carrinho, CarrinhoItem
from datetime import datetime


# Função para adicionar um item ao carrinho
def create_carrinhoitem_view(request, produto_id=None):
    print('create_carrinhoitem_view')

    produto = get_object_or_404(Produto, pk=produto_id)
    if produto:
        print('produto:', produto.id)

    # Tenta pegar o carrinho da sessão ou cria um novo carrinho
    carrinho_id = request.session.get('carrinho_id')
    print('carrinho:', carrinho_id)

    carrinho = None
    if carrinho_id:
        # Se o carrinho já estiver na sessão, tentamos obter o carrinho
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        print(carrinho)
        if carrinho:
            print('carrinho1:', carrinho.id)

    hoje = datetime.today().date()

    # Verifica se precisa criar um novo carrinho
    if not carrinho or carrinho.criado_em.date() != hoje:
        # Se o carrinho não existir ou não for de hoje, cria um novo
        carrinho = Carrinho.objects.create()
        request.session['carrinho_id'] = carrinho.id
        print('novo carrinho:', carrinho.id)
    else:
        print('carrinho existente:', carrinho.id)

    # Verifica se o produto já existe no carrinho do usuário
    carrinho_item = CarrinhoItem.objects.filter(carrinho=carrinho, produto=produto).first()

    if carrinho_item:
        # Se o produto já estiver no carrinho, apenas aumenta a quantidade
        carrinho_item.quantidade += 1
        print('item de carrinho: Acrescentou 1 item do produto', carrinho_item.id)
    else:
        # Se o produto não estiver no carrinho, cria um novo item
        carrinho_item = CarrinhoItem.objects.create(
            carrinho=carrinho,
            produto=produto,
            quantidade=1,
            preco=produto.preco
        )
        print('item de carrinho: Acrescentou o produto', carrinho_item.id)

    carrinho_item.save()
    print('item de carrinho salvo:', carrinho_item.id)

    return redirect('/carrinho')
