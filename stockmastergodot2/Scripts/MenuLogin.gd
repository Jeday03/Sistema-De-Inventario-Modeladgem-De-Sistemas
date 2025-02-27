extends CanvasLayer

@onready var http_request: HTTPRequest = $HTTPRequest
@onready var usuario: LineEdit = $VBoxContainer/LineEdit
@onready var senha: LineEdit = $VBoxContainer/LineEdit2

@onready var texture_rect: TextureRect = $TextureRect
@onready var accept_dialog: AcceptDialog = $AcceptDialog

const DEFAULT_PAGE = preload("res://Scenes/DefaultPage.tscn")

func _on_button_pressed() -> void:
	var body = JSON.stringify({"email": usuario.text, "senha": senha.text})
	var headers = ["Content-Type: application/json"]
	var error = http_request.request("http://127.0.0.1:5000/login", headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		accept_dialog.visible = true
		return

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	var json_string = body.get_string_from_utf8()
	print(json_string)
	if not json_string:
		return
	var data : Dictionary = JSON.parse_string(json_string)
	if data.get("message", false):
		get_tree().change_scene_to_packed(DEFAULT_PAGE)
		'''
		match data['tipo_usuario']:
			"gerente":
				get_tree().change_scene_to_packed(DEFAULT_PAGE)
			"funcionario":
				pass
		'''
	else:
		accept_dialog.visible = true
		senha.text = ""
