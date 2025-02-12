# Sistema-De-Inventario-Modelagem-De-Sistemas

Atualmente, o repositório se encontra com a branch "Prototipos" atualizada. Esta branch contém o início de HTML, CSS e JavaScript que servirão de base para a criação do site de gerenciamento de estoque.

## Atualizações do Front-End

- Primeiro, justificar aqui a troca de nomes: o login virou index porque index é o primeiro arquivo a ser exibido na tela do usuário.
- Segundo, fiz algumas mudanças nos estilos de algumas coisas e mudei bastante a página de login. Ainda vou ter que mexer um pouco nas coisas na página de gerenciamento (antigo index), mas é pouca coisa.
- Sobre o JavaScript, definitivamente não vou mexer mais nisso, então caso já queira começar a mexer, pode (EU ACHO).
- Além disso, como dá para ver, coloquei em pastas separadas os arquivos CSS e JS. Futuramente, penso em um jeito de separar ainda mais.
- Não sei se melhora ou atrapalha, mas eu adcionei uma pasta e separei esse arquivo gerenciamento em varios arquivos css menores caso não fique daora deixei o arquivo ai pra poder colocar de volta caso precise.

## Explicação do Gerenciamento.html

A ideia do gerenciamento.html é gerar uma tela onde tem o nome do projeto e uma sidebar com alguns botões para o usuário apertar. Eles são divididos em estoque, vendas, cadastro, pedidos e logout (sair). Assim que qualquer botão for pressionado (fora o de sair), a parte que até então contém apenas o background vai ter alguma coisa. Acontece uma animação rápida e dela aparece uma das telas: pedidos, vendas, cadastro, estoque.

As funcionalidades dos botões vão funcionar assim:

- **Logout**: uma função de sair simples que inclusive já está "implementada". Ela já redireciona para o login quando aperta o botão de sair.
- **Estoque**: Adicionar produtos ao estoque.
- **Pedidos**: Realizar pedidos.
- **Cadastro**: Realizar cadastro.
- **Vendas**: Realizar vendas.