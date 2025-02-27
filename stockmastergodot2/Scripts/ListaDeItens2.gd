extends VBoxContainer
class_name listaItem

const PAINEL_DE_ITEM = preload("res://PackedScenes/PainelDeItem.tscn")
@onready var http_request: HTTPRequest = $"../HTTPRequest"
@onready var line_edit: LineEdit = $"../../LineEdit"
@onready var formulario: FormularioItem = %MarginContainer2
@onready var line_edit_scroll = $HBoxContainer/MarginContainer/VBoxContainer/HBoxContainer/LineEdit

var pagAtual : int = 1:
	set(value):
		if value > 0:
			pagAtual = value
			var aux = str(value)
			print(aux)
			$HBoxContainer/MarginContainer/VBoxContainer/HBoxContainer/LineEdit.text = aux
		var erro = http_request.request("http://127.0.0.1:5000/item?page=" + str(value) + "&prefix=" + line_edit.text, [], HTTPClient.METHOD_GET)
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
			print(item['extensao'])
			match item['extensao']:
				".png":
					erro = image.load_png_from_buffer(bytes)
				".jpg":
					erro = image.load_jpg_from_buffer(bytes)
			
			if erro != OK:
				printerr("DEU MERDA3")
				continue
			var texture : ImageTexture = ImageTexture.create_from_image(image)
			instanciar(texture, item)

func instanciar(textura : ImageTexture, f : Dictionary):
	var qtdCerta = round(f['quantidade'])
	var instancia : PainelItem = PAINEL_DE_ITEM.instantiate()
	add_child(instancia)
	instancia.setup(textura, formulario, f)

func _on_pag_anterior_pressed() -> void:
	pagAtual -= 1

func _on_pag_posterior_pressed() -> void:
	pagAtual += 1


func _on_line_edit_text_submitted(new_text: String) -> void:
	var n : int = int(line_edit_scroll.text)
	if n <= 0:
		n = 1
	pagAtual = n
