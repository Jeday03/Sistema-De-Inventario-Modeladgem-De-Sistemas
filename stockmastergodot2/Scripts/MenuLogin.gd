extends CanvasLayer

@onready var http_request: HTTPRequest = $HTTPRequest
@onready var usuario: LineEdit = $VBoxContainer/LineEdit
@onready var senha: LineEdit = $VBoxContainer/LineEdit2

@onready var texture_rect: TextureRect = $TextureRect

func _on_button_pressed() -> void:
	var erro = http_request.request("http://127.0.0.1:5000/get_image", [], HTTPClient.METHOD_GET)
	if erro == OK:
		print("Deu certo, enviou a request")
	'''
	var body = JSON.stringify({"usuario": usuario.text, "senha": senha.text})
	var headers = ["Content-Type: application/json"]
	var error = http_request.request("http://127.0.0.1:5000/login", headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		printerr("Algo deu errado. Tente novamente")
		return
	'''

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	print("Response code: ", response_code)
	if response_code == 200:
		var image = Image.new()
		print(typeof(body))
		var error = image.load_png_from_buffer(body)
		if error == OK:
			var texture = ImageTexture.create_from_image(image)
			texture_rect.texture = texture
		else:
			printerr("Erro ao carregar a imagem")
	else:
		printerr("Falha na solicitação: ", response_code)
	'''
	var json = body.get_string_from_utf8()
	if not json:
		return
	print(json)
	var data = JSON.parse_string(json)
	print(data)
	'''
