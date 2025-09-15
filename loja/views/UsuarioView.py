from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm

def list_usuario_view(request, id=None):
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
        'usuarios': usuarios
    }
    return render(request, template_name='usuario/usuario.html', context=context, status=200)


def edit_usuario_view(request):
    # Busca o objeto Usuario correspondente ao usuário logado
    usuario = get_object_or_404(Usuario, user=request.user)

    # Inicialização das variáveis de controle
    emailUnused = True
    message = None

    if request.method == 'POST':
        # Cria os formulários com os dados enviados no POST
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=request.user)

        # Verifica se o e-mail já está em uso por outro usuário
        verifyEmail = Usuario.objects.filter(
            user__email=request.POST['email']
        ).exclude(user__id=request.user.id).first()

        emailUnused = verifyEmail is None

        # Se os formulários são válidos e o e-mail não está sendo usado
        if usuarioForm.is_valid() and userForm.is_valid() and emailUnused:
            usuarioForm.save()
            userForm.save()
            message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
        else:
            # Se o e-mail já está em uso por outro usuário
            if not emailUnused:
                message = {'type': 'warning', 'text': 'E-mail já usado'}
            else:
                # Se o e-mail está livre mas há erros nos formulários
                message = {'type': 'danger', 'text': 'Dados inválidos'}
    else:
        # Se for GET, apenas exibe os formulários preenchidos com os dados atuais
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=request.user)
        # Nenhuma mensagem de erro/sucesso no primeiro carregamento (GET)

    # Contexto para o template
    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message
    }

    return render(request, template_name='usuario/usuario-edit.html', context=context, status=200)
