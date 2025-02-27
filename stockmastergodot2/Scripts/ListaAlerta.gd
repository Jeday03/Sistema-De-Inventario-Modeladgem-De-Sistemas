extends Control
class_name ListaAlerta

const NOTIFICACAO = preload("res://PackedScenes/Notificacao.tscn")
@onready var notificacoes_container: VBoxContainer = $VBoxContainer/ScrollContainer/NotificacoesContainer
@onready var http_request: HTTPRequest = $VBoxContainer/ScrollContainer/HTTPRequest
@onready var http_request2: HTTPRequest = $HTTPRequest

func _ready() -> void:
	http_request.request("http://127.0.0.1:5000/notificacao", [], HTTPClient.METHOD_GET)

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if not (response_code == 200 or response_code == 201):
		return
	for c in notificacoes_container.get_children():
		c.queue_free()
	var response_text = body.get_string_from_utf8()
	var response_json = JSON.parse_string(response_text)
	for i in response_json:
		var image = Image.new()
		var bytes : PackedByteArray = Marshalls.base64_to_raw(i['imagem'])
		var error : Error = FAILED
		match i['extensao']:
			".png":
				error = image.load_png_from_buffer(bytes)
			".jpg":
				error = image.load_jpg_from_buffer(bytes)
		
		if error != 0:
			printerr("DEU MERDA2")
			continue
		var texture : ImageTexture = ImageTexture.create_from_image(image)
		instanciar(texture, i['mensagem'], i['id'])

func instanciar(textura : ImageTexture, nomeItem : String, id : int):
	var instancia : Notificacao = NOTIFICACAO.instantiate()
	notificacoes_container.add_child(instancia)
	instancia.set_alert(nomeItem, textura, id, self)

func deletar(id : int):
	var json = {
		'id': id
	}
	var body = JSON.stringify(json)
	http_request2.request("http://127.0.0.1:5000/notificacao", [], HTTPClient.METHOD_DELETE)

func segundoRequestCompletado(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	http_request.request("http://127.0.0.1:5000/notificacao", [], HTTPClient.METHOD_GET)
