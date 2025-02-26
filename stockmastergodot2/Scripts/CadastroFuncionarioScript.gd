extends Control
class_name CadastroFuncionario

@onready var http_request_2: HTTPRequest = $HTTPRequest2
@onready var lista_de_funcionários: VBoxContainer = $HBoxContainer/MarginContainer/ScrollContainer/ListaFuncionario
const PAINEL_FUNCIONARIO = preload("res://PackedScenes/PainelFuncionario.tscn")
@onready var pageText: LineEdit = $HBoxContainer/MarginContainer/VBoxContainer/HBoxContainer/LineEdit

var pagAtual : int = 1:
	set(value):
		if value > 0:
			pagAtual = value
			pageText.text = str(value)
			var url = "http://127.0.0.1:5000/funcionarios?page=" + str(pagAtual) 
			http_request_2.request(url, [], HTTPClient.METHOD_GET)

func _ready() -> void:
	var url = "http://127.0.0.1:5000/funcionarios?page=" + str(pagAtual) 
	http_request_2.request(url, [], HTTPClient.METHOD_GET)

func _on_http_request_2_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		return
	var response_text = body.get_string_from_utf8()
	var response_json = JSON.parse_string(response_text)
	for funcionario in response_json:
		var image = Image.new()
		var bytes : PackedByteArray = Marshalls.base64_to_raw(funcionario['imagem'])
		var error : Error = FAILED
		match funcionario['extensao']:
			".png":
				error = image.load_png_from_buffer(bytes)
			".jpg":
				error = image.load_jpg_from_buffer(bytes)
		
		if error != OK:
			printerr("DEU MERDA")
			continue
		var texture : ImageTexture = ImageTexture.create_from_image(image)
		instanciar(texture, funcionario)

func instanciar(t : ImageTexture, funcionario : Dictionary):
	var novo : PainelFuncionario = PAINEL_FUNCIONARIO.instantiate()
	lista_de_funcionários.add_child(novo)
	novo.pai = self as CadastroFuncionario
	novo.setup(t, funcionario)

@onready var campo_nome: LineEdit = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/CampoNome
@onready var campo_cpf: LineEdit = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/CampoCPF
@onready var campo_cel: LineEdit = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/CampoCel
@onready var campo_email: LineEdit = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/CampoEmail
@onready var option_button: OptionButton = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/OptionButton
@onready var campo_senha: LineEdit = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/CampoSenha
@onready var http_request: HTTPRequest = $HTTPRequest

@onready var accept_dialog: AcceptDialog = $AcceptDialog
@onready var erro: AcceptDialog = $Erro
@onready var confirmation_dialog: ConfirmationDialog = $ConfirmationDialog

var idFuncionario : int = -1

var funcaoAtual : Callable

func _on_cadastrar_pressed() -> void:
	funcaoAtual = Callable(self, "cadastrar")
	confirmation_dialog.dialog_text = "Deseja CADASTRAR o usuário " + campo_nome.text + "?"
	confirmation_dialog.visible = true

func cadastrar():
	var json = {
		"nome": campo_nome.text,
		"cpf": campo_cpf.text,
		"celular": campo_cel.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text,
	}
	var body = JSON.stringify(json)
	var error = http_request.request("http://127.0.0.1:5000/funcionarios", ["Content-Type: application/json"], HTTPClient.METHOD_POST, body)
	if error != OK:
		erro.visible = true

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		accept_dialog.visible = true
		campo_nome.text = ""
		campo_cel.text = ""
		campo_email.text = ""
		campo_senha.text = ""
		campo_cpf.text = ""
		idFuncionario = -1
	else:
		erro.visible = true

var listaFuncao := ["Administrador", "Gerente", "Caixa/Repositor"]

func carregarFuncionario(textura : ImageTexture, funcionario : Dictionary):
	campo_nome.text = funcionario['nome']
	campo_cel.text = funcionario['celular']
	campo_email.text = funcionario['email']
	campo_cpf.text = funcionario['cpf']
	idFuncionario = funcionario['id']
	option_button.select(listaFuncao.find(funcionario['funcao']))

func _on_editar_pressed() -> void:
	funcaoAtual = Callable(self, "editarFuncionario")
	confirmation_dialog.dialog_text = "Deseja EDITAR o usuário " + campo_nome.text + "?"
	confirmation_dialog.visible = true

func editarFuncionario():
	var json = {
		"nome": campo_nome.text,
		"cpf": campo_cpf.text,
		"celular": campo_cel.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text,
		"id": idFuncionario
	}
	var body = JSON.stringify(json)
	var error = http_request.request("http://127.0.0.1:5000/funcionarios", ["Content-Type: application/json"], HTTPClient.METHOD_PUT, body)
	if error != OK:
		erro.visible = true

func _on_remover_pressed() -> void:
	funcaoAtual = Callable(self, "remover")
	confirmation_dialog.dialog_text = "Deseja REMOVER o usuário " + campo_nome.text + "?"
	confirmation_dialog.visible = true

func remover():
	var json = {
		"nome": campo_nome.text,
		"celular": campo_cel.text,
		"cpf": campo_cpf.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text,
		"id": idFuncionario
	}
	var body = JSON.stringify(json)
	http_request.request("http://127.0.0.1:5000/remover_funcionario", ["Content-Type: application/json"], HTTPClient.METHOD_DELETE, body)


func _on_confirmation_dialog_confirmed() -> void:
	funcaoAtual.call()

func _on_pag_anterior_pressed() -> void:
	pagAtual -= 1

func _on_pag_posterior_pressed() -> void:
	pagAtual += 1

func _on_line_edit_text_submitted(new_text: String) -> void:
	var n : int = int(pageText.text)
	if n == 0:
		n = 1
	pagAtual = n
