extends Control
class_name CadastroFuncionario

@onready var http_request_2: HTTPRequest = $HTTPRequest2
@onready var lista_de_funcionários: VBoxContainer = $HBoxContainer/MarginContainer/VBoxContainer/ScrollContainer/ListaFuncionario
const PAINEL_FUNCIONARIO = preload("res://PackedScenes/PainelFuncionario.tscn")
@onready var pageText: LineEdit = $HBoxContainer/MarginContainer/VBoxContainer/HBoxContainer/LineEdit

@onready var file_dialog: FileDialog = $FileDialog

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
	for c in lista_de_funcionários.get_children():
		c.queue_free()
	for funcionario in response_json:
		image = Image.new()
		var bytes : PackedByteArray = Marshalls.base64_to_raw(funcionario['imagem'])
		var error : Error = FAILED
		match funcionario['extensao']:
			".png":
				error = image.load_png_from_buffer(bytes)
			".jpg":
				error = image.load_jpg_from_buffer(bytes)
		
		if error != 0:
			printerr("DEU MERDA2")
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

var image : Image
@onready var fotoFuncionario: TextureRect = $HBoxContainer/MarginContainer2/ScrollContainer/Formulario/FotoFuncionario
var imageType : String


func _on_cadastrar_pressed() -> void:
	funcaoAtual = Callable(self, "cadastrar")
	confirmation_dialog.dialog_text = "Deseja CADASTRAR o usuário " + campo_nome.text + "?"
	confirmation_dialog.visible = true
	accept_dialog.dialog_text = "Usuário criado"

func cadastrar():
	var imagemComprimida : PackedByteArray
	match imageType:
		".png":
			imagemComprimida = image.save_png_to_buffer()
		".jpg":
			imagemComprimida = image.save_jpg_to_buffer()
		"null":
			printerr("Imagem inválida. Recarregue novamente")
			return
	var imagemBase64 = Marshalls.raw_to_base64(imagemComprimida)
	var json = {
		"nome": campo_nome.text,
		"cpf": campo_cpf.text,
		"celular": campo_cel.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text,
		"imagem": imagemBase64,
		"extensao": imageType
	}
	var body = JSON.stringify(json)
	var thisError = http_request.request("http://127.0.0.1:5000/funcionarios", ["Content-Type: application/json"], HTTPClient.METHOD_POST, body)
	print(thisError, " Cadastro")
	if thisError != 0:
		print("Entrou aq")
		erro.visible = true

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200 or response_code == 201:
		accept_dialog.visible = true
		campo_nome.text = ""
		campo_cel.text = ""
		campo_email.text = ""
		campo_senha.text = ""
		campo_cpf.text = ""
		idFuncionario = -1
		pagAtual = pagAtual
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
	accept_dialog.dialog_text = "Usuário editado"

func editarFuncionario():
	var imagemComprimida : PackedByteArray
	match imageType:
		".png":
			imagemComprimida = image.save_png_to_buffer()
		".jpg":
			imagemComprimida = image.save_jpg_to_buffer()
		"null":
			printerr("Imagem inválida. Recarregue novamente")
			return
	var imagemBase64 = Marshalls.raw_to_base64(imagemComprimida)
	var json = {
		"nome": campo_nome.text,
		"cpf": campo_cpf.text,
		"celular": campo_cel.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text,
		"id": idFuncionario,
		"imagem": imagemBase64
	}
	var body = JSON.stringify(json)
	var thiserror = http_request.request("http://127.0.0.1:5000/funcionarios", ["Content-Type: application/json"], HTTPClient.METHOD_PUT, body)
	if thiserror != 0:
		erro.visible = true

func _on_remover_pressed() -> void:
	funcaoAtual = Callable(self, "remover")
	confirmation_dialog.dialog_text = "Deseja REMOVER o usuário " + campo_nome.text + "?"
	confirmation_dialog.visible = true
	accept_dialog.dialog_text = "Usuário removido"

func remover():
	var json = {
		"id": idFuncionario
	}
	var body = JSON.stringify(json)
	http_request.request("http://127.0.0.1:5000/funcionarios", ["Content-Type: application/json"], HTTPClient.METHOD_DELETE, body)

func _on_confirmation_dialog_confirmed() -> void:
	funcaoAtual.call()

func _on_pag_anterior_pressed() -> void:
	pagAtual -= 1

func _on_pag_posterior_pressed() -> void:
	pagAtual += 1

func _on_line_edit_text_submitted(new_text: String) -> void:
	var n : int = int(pageText.text)
	if n <= 0:
		n = 1
	pagAtual = n

func _on_button_imagem_pressed() -> void:
	file_dialog.visible = true

func _on_file_dialog_file_selected(path: String) -> void:
	image = Image.load_from_file(path)
	if not image:
		erro.visible = true
		return
	var texture = ImageTexture.create_from_image(image)
	fotoFuncionario.texture = texture
	imageType = "." + path.get_extension()
