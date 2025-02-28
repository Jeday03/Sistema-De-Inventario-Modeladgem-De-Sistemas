extends MarginContainer
class_name FormularioItem

@onready var lista: listaItem = $"../MarginContainer/VBoxContainer/ScrollContainer/VBoxContainer"

@onready var nome: LineEdit = $ScrollContainer/VBoxContainer/LineEdit
@onready var qtd: SpinBox = $ScrollContainer/VBoxContainer/SpinBox
@onready var file_dialog: FileDialog = $FileDialog
@onready var texture_rect: TextureRect = $ScrollContainer/VBoxContainer/TextureRect
@onready var erro: AcceptDialog = $AcceptDialog
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var preco: LineEdit = $ScrollContainer/VBoxContainer/LineEdit2

var idAtual : int
var image : Image
var imageType : String

func _on_select_image_button_pressed() -> void:
	file_dialog.visible = true

func _on_cadastrar_pressed() -> void:
	var imagemComprimida : PackedByteArray
	match imageType:
		".png":
			imagemComprimida = image.save_png_to_buffer()
		".jpg":
			imagemComprimida = image.save_jpg_to_buffer()
		"null":
			printerr("Imagem inválida. Recarregue novamente")
			return
	var imagemBase64 = Marshalls.raw_to_base64(imagemComprimida)
	var json = {
		"nome": nome.text,
		"quantidade": qtd.value,
		"imagem": imagemBase64,
		"extensao": imageType,
		"preco": float(preco.text)
	}
	var body : String = JSON.stringify(json)
	http_request.request("http://127.0.0.1:5000/item", ["Content-Type: application/json"], HTTPClient.METHOD_POST, body)

func _on_editar_pressed() -> void:
	var imagemComprimida : PackedByteArray
	match imageType:
		".png":
			imagemComprimida = image.save_png_to_buffer()
		".jpg":
			imagemComprimida = image.save_jpg_to_buffer()
		"null":
			printerr("Imagem inválida. Recarregue novamente")
			return
	var imagemBase64 = Marshalls.raw_to_base64(imagemComprimida)
	var json = {
		"id": idAtual,
		"nome": nome.text,
		"quantidade": qtd.value,
		"imagem": imagemBase64,
		"extensao": imageType,
		"preco": float(preco.text)
	}
	var body : String = JSON.stringify(json)
	http_request.request("http://127.0.0.1:5000/item", ["Content-Type: application/json"], HTTPClient.METHOD_PUT, body)

func _on_remover_pressed() -> void:
	var json = {
		"id": idAtual
	}
	var body := JSON.stringify(json)
	http_request.request("http://127.0.0.1:5000/item", ["Content-Type: application/json"], HTTPClient.METHOD_DELETE, body)

func _on_file_dialog_file_selected(path: String) -> void:
	image = Image.load_from_file(path)
	if not image:
		erro.visible = true
		return
	var texture := ImageTexture.create_from_image(image)
	texture_rect.texture = texture
	imageType = "." + path.get_extension()

func selecionaItem(d : Dictionary, textura : ImageTexture):
	nome.text = d['nome']
	qtd.value = int(d['quantidade'])
	texture_rect.texture = textura
	idAtual = d['id']


func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	lista.pagAtual = lista.pagAtual
