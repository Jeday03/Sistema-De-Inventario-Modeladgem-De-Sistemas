extends CanvasLayer

@onready var http_request: HTTPRequest = $HTTPRequest
@onready var usuario: LineEdit = $VBoxContainer/LineEdit
@onready var senha: LineEdit = $VBoxContainer/LineEdit2

@onready var texture_rect: TextureRect = $TextureRect

func _on_button_pressed() -> void:
	var body = JSON.new().stringify({"usuario": usuario.text, "senha": senha.text})
	print(typeof(body))
	var headers = ["Content-Type: application/json"]
	var error = http_request.request("http://127.0.0.1:5000/login", headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		printerr("Algo deu errado. Tente novamente")
		return

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	var json = body.get_string_from_utf8()
	if not json:
		return
	print(json)
	var data = JSON.parse_string(json)
	print(data)
	


func _on_visibility_changed() -> void:
	pass # Replace with function body.
