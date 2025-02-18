extends Control

@onready var campo_nome: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoNome
@onready var campo_cpf: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoCPF
@onready var campo_cel: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoCel
@onready var campo_email: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoEmail
@onready var option_button: OptionButton = $HBoxContainer/MarginContainer2/Formulario/OptionButton
@onready var campo_senha: LineEdit = $HBoxContainer/MarginContainer2/Formulario/CampoSenha
@onready var http_request: HTTPRequest = $HTTPRequest

func _on_cadastrar_pressed() -> void:
	var json = {
		"nome": campo_nome.text,
		"cpf": campo_cpf.text,
		"celular": campo_cel.text,
		"email": campo_email.text,
		"funcao": option_button.get_item_text(option_button.selected),
		"senha": campo_senha.text
	}
	http_request.request("url", [], HTTPClient.METHOD_POST, json)
