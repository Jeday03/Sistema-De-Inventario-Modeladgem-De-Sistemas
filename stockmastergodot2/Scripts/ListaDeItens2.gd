extends VBoxContainer

const PAINEL_DE_ITEM = preload("res://PackedScenes/PainelDeItem.tscn")
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var timer: Timer = $Timer
@onready var line_edit: LineEdit = $"../../LineEdit"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var erro = http_request.request("http://127.0.0.1:5000/itens", [], HTTPClient.METHOD_GET)
	if erro != OK:
		printerr("Não foi possível fazer httprequest")

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		for c in get_children():
			c.queue_free()
		var response_text = body.get_string_from_utf8()
		var response_json = JSON.parse_string(response_text)
		for item in response_json:
			var image : Image = Image.new()
			var bytes : PackedByteArray = Marshalls.base64_to_raw(item['imagem'])
			var erro : Error = FAILED
			match item['extensao']:
				".png":
					erro = image.load_png_from_buffer(bytes)
				".jpg":
					erro = image.load_jpg_from_buffer(bytes)
			
			if erro != OK:
				printerr("DEU MERDA")
				continue
			var texture : ImageTexture = ImageTexture.create_from_image(image)
			instanciar(texture, item['nome'], item['quantidade'])

func instanciar(textura : ImageTexture, nome : StringName, qtd : float):
	var qtdCerta = round(qtd)
	var instancia : PainelItem = PAINEL_DE_ITEM.instantiate()
	add_child(instancia)
	instancia.setup(textura, nome, qtdCerta)

func _on_line_edit_text_changed(new_text: String) -> void:
	timer.start()
	pass

func _on_timer_timeout() -> void:
	if not http_request:
		return
	http_request.cancel_request()
	var json = {
		"prefixo": line_edit.text
	}
	var body = JSON.stringify(json)
	var erro = http_request.request("http://127.0.0.1:5000/item", ["Content-Type: application/json"], HTTPClient.METHOD_GET, body)
	if erro != OK:
		printerr("Não foi possível fazer httprequest")
