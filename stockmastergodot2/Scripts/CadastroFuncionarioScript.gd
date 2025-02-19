extends Control

@onready var http_request_2: HTTPRequest = $HTTPRequest2
@onready var lista_de_funcionários: VBoxContainer = $"HBoxContainer/MarginContainer/ScrollContainer/Lista de funcionários"


func _ready() -> void:
	http_request_2.request("url", [], HTTPClient.METHOD_GET)

func _on_http_request_2_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		return
	var response_text = body.get_string_from_utf8()
	var response_json = JSON.parse_string(response_text)
	for funcionario in response_json:
		var image = Image.new()
		var bytes : PackedByteArray = Marshalls.base64_to_raw(funcionario['imagem'])
		var erro : Error = FAILED
		match funcionario['extensao']:
			".png":
				erro = image.load_png_from_buffer(bytes)
			".jpg":
				erro = image.load_jpg_from_buffer(bytes)
		
		if erro != OK:
			printerr("DEU MERDA")
			continue
		var texture : ImageTexture = ImageTexture.create_from_image(image)
		#CRIAR AQUI O OBJETO FUNCIONÁRIO


@onready var campo_nome: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoNome
@onready var campo_cpf: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoCPF
@onready var campo_cel: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoCel
@onready var campo_email: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoEmail
@onready var option_button: OptionButton = $HBoxContainer/MarginContainer2/Formulario/OptionButton
@onready var campo_senha: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoSenha
@onready var http_request: HTTPRequest = $HTTPRequest

@onready var accept_dialog: AcceptDialog = $AcceptDialog
@onready var erro: AcceptDialog = $Erro

func _on_cadastrar_pressed() -> void:
	var json = {
		"nome": campo_nome.text,
		"cpf": campo_cpf.text,
		"celular": campo_cel.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text
	}
	var body = JSON.stringify(json)
	var error = http_request.request("http://127.0.0.1:5000/cadastro_funcionario", [], HTTPClient.METHOD_POST, body)
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
	else:
		erro.visible = true
