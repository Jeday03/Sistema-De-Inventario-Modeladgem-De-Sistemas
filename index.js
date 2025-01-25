document.addEventListener('DOMContentLoaded', (event) => {
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

    // Eventos para os botões
    document.getElementById('Estoque').addEventListener('click', () => {
        mostrarConteudo('conteudoEstoque');
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
});
