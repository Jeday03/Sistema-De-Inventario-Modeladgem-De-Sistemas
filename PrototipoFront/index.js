document.addEventListener('DOMContentLoaded', (event) => {
    let itemSelecionado = null;

    // Função para mostrar o conteúdo exclusivo
    function mostrarConteudo(id) {
        // Esconde todos os conteúdos
        var conteudos = document.querySelectorAll('.conteudo');
        conteudos.forEach(conteudo => {
            conteudo.classList.remove('mostrar');
        });
        
        // Mostra o conteúdo específico
        var conteudoExclusivo = document.getElementById(id);
        conteudoExclusivo.classList.add('mostrar');
    }

    // Função para gerar a lista de itens no estoque (vazia)
    function gerarListaEstoque() {
        var lista = document.getElementById('listaEstoque');
        lista.innerHTML = ''; 
    }

    // Função para adicionar itens à lista
    function adicionarItem() {
        const nomeProduto = document.getElementById('nomeProduto').value;
        const quantidadeProduto = document.getElementById('quantidadeProduto').value;

        if (nomeProduto && quantidadeProduto) {
            const lista = document.getElementById('listaEstoque');
            const listItem = document.createElement('li');
            listItem.textContent = `${nomeProduto}: ${quantidadeProduto}`;
            listItem.addEventListener('click', () => {
                if (itemSelecionado) {
                    itemSelecionado.classList.remove('selecionado');
                }
                itemSelecionado = listItem;
                listItem.classList.add('selecionado');
            });
            lista.appendChild(listItem);

            document.getElementById('nomeProduto').value = '';
            document.getElementById('quantidadeProduto').value = '';
        } else {
            alert('Por favor, preencha ambos os campos.');
        }
    }

    function removerItem() {
        console.log('Função removerItem chamada');
        if (itemSelecionado) {
            const lista = document.getElementById('listaEstoque');
            console.log('Item selecionado:', itemSelecionado.textContent);
            lista.removeChild(itemSelecionado);
            itemSelecionado = null;
        } else {
            alert('Por favor, selecione um item para remover.');
        }
    }


    // Eventos para os botões
    document.getElementById('Estoque').addEventListener('click', () => {
        mostrarConteudo('conteudoEstoque');
        gerarListaEstoque(); 
    });

    document.getElementById('Vendas').addEventListener('click', () => {
        mostrarConteudo('conteudoVendas');
    });

    document.getElementById('Cadastro').addEventListener('click', () => {
        mostrarConteudo('conteudoCadastro');
    });

    document.getElementById('Pedidos').addEventListener('click', () => {
        mostrarConteudo('conteudoPedidos');
    });

    // Evento para o botão Logout
    document.getElementById('Logout').addEventListener('click', () => {
        window.location.href = 'login.html';
    });

    // Evento para o botão Adicionar
    document.getElementById('adicionar').addEventListener('click', adicionarItem);

    document.getElementById('remover').addEventListener('click', removerItem);

});