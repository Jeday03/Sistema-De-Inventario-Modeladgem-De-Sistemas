document.querySelector('.formLogin').addEventListener('submit', logar);

function logar(event) {
    event.preventDefault(); //ignora envio, remover qnd for possivel validar
    var login = document.getElementById("email").value;
    var senha = document.getElementById("password").value;

    if (login && senha) {
        alert("sucesso");
        location.href = "gerenciamento.html";
    } else {
        alert("Por favor, preencha todos os campos!");
    }
}