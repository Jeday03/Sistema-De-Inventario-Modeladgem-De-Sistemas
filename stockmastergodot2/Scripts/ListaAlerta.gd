extends Control

const NOTIFICACAO = preload("res://PackedScenes/Notificacao.tscn")
@onready var notificacoes_container: VBoxContainer = $VBoxContainer/ScrollContainer/NotificacoesContainer
@onready var http_request: HTTPRequest = $VBoxContainer/ScrollContainer/NotificacoesContainer/HTTPRequest

func _ready() -> void:
	# Fazer a requisição HTTP para obter as informações de estoque
	#var erro = http_request.request("http://127.0.0.1:5000/estoque_faltando", ["Content-Type: application/json"], HTTPClient.METHOD_GET)
	#if erro != OK:
	#    printerr("Não foi possível fazer a requisição HTTP")
	
	# Adicionar notificações de teste
	adicionar_notificacoes_teste()

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		limpar_lista()
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
				printerr("Erro ao carregar a imagem")
				continue
			var texture : ImageTexture = ImageTexture.new()
			@warning_ignore("static_called_on_instance")
			texture.create_from_image(image)
			criar_notificacao(item['nome'], texture)

func limpar_lista():
	for c in notificacoes_container.get_children():
		c.queue_free()

func criar_notificacao(nome: String, textura: Texture):
	var notificacao = NOTIFICACAO.instantiate()
	notificacoes_container.add_child(notificacao)
	notificacao.set_alert(nome, textura)
	notificacao.get_node("MarginContainer/HBoxContainer/VBoxContainer2/Button").connect("pressed", Callable(self, "_on_notificacao_removida").bind([notificacao]))

func _on_notificacao_removida(notificacao):
	notificacao.queue_free()

func adicionar_notificacoes_teste():
	var nomes = ["Item 1", "Item 2", "Item 3", "Item 4"]
	for nome in nomes:
		var image = Image.new()
		@warning_ignore("static_called_on_instance")
		image.create(64, 64, false, Image.FORMAT_RGBA8)
		image.fill(Color(1, 0, 0))  # Preencher a imagem com a cor vermelha
		var texture = ImageTexture.new()
		@warning_ignore("static_called_on_instance")
		texture.create_from_image(image)
		criar_notificacao(nome, texture)
