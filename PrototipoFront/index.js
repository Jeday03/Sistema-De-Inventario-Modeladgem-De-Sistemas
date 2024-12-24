document.addEventListener('DOMContentLoaded', (event) => {
    // Isso aqui ta mais pra teste mesmo não sei se vai acabr ficando isso mesmo
    function abrirRecurso(url) {
        window.location.href = url;
    }

    //Funções pra poder acessar outras janelas no Sistema

    document.getElementById('Estoque').addEventListener('click', () => {
        abrirRecurso('Estoque.html');
    });

    document.getElementById('Vendas').addEventListener('click', () => {
        abrirRecurso('Vendas.html');
    });

    document.getElementById('Cadastro').addEventListener('click', () => {
        abrirRecurso('Cadastro.html');
    });

    document.getElementById('Pedidos').addEventListener('click', () => {
        abrirRecurso('Pedidos.html');
    });
});