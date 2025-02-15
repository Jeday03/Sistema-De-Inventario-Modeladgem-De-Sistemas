extends VBoxContainer

const PAINEL_DE_ITEM = preload("res://PackedScenes/PainelDeItem.tscn")
@onready var http_request: HTTPRequest = $HTTPRequest

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var erro = http_request.request("http://127.0.0.1:5000/itens", [], HTTPClient.METHOD_GET)
	if erro != OK:
		printerr("Não foi possível fazer httprequest")


func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var response_text = body.get_string_from_utf8()
		var response_json = JSON.parse_string(response_text)
		print(typeof(response_json))
		for item in response_json:
			var image = Image.new()
			print(typeof(item['imagem']))
			#TEM ALGO ERRADO COM ESSA CONVERSÃO DE BASE64 PRA UTF8 E DPS PRA IMAGEM
			var error = image.load_png_from_buffer(Marshalls.base64_to_utf8(item['imagem']).to_utf8_buffer())
			if error == OK:
				var texture = ImageTexture.create_from_image(image)
				instanciar(texture, item['nome'], item['quantidade'])
			else:
				printerr("DEU RUIM")

func instanciar(textura : ImageTexture, nome : StringName, qtd : int):
	var instancia : PainelItem = PAINEL_DE_ITEM.instantiate()
	instancia.setup(textura, nome, qtd)
	add_child(instancia)
