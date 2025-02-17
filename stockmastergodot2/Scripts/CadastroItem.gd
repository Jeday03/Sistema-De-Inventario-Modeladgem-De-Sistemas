extends Control

@onready var file_dialog: FileDialog = $FileDialog
@onready var texture_rect: TextureRect = $VBoxContainer/TextureRect
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var nome: LineEdit = $VBoxContainer/LineEdit
@onready var qtd: LineEdit = $VBoxContainer/LineEdit2

var image : Image = null
var imageType : String = "null"

func _ready() -> void:
	file_dialog.current_dir = '/'

func _on_button_pressed() -> void:
	file_dialog.visible = true

func _on_file_dialog_file_selected(path: String) -> void:
	image = Image.load_from_file(path)
	if not image:
		printerr("Imagem incorreta. Envie uma imagem melhor")
		return
	var texture = ImageTexture.create_from_image(image)
	texture_rect.texture = texture
	imageType = path.get_extension()

func _on_button_2_pressed() -> void:
	var imagemComprimida : PackedByteArray
	match imageType:
		"png":
			imagemComprimida = image.save_png_to_buffer()
		"jpg":
			imagemComprimida = image.save_jpg_to_buffer()
		"null":
			printerr("Imagem inválida. Recarregue novamente")
			return
	var imagemBase64 = Marshalls.raw_to_base64(imagemComprimida)
	var json = JSON.stringify({
		"nome": nome.text,
		"quantidade": float(qtd.text),
		"imagem": imagemBase64,
		"extensao": imageType
	})
	var header = ["Content-Type: application/json"]
	http_request.request("http://127.0.0.1:5000/add_item", header, HTTPClient.METHOD_POST, json)
	
	texture_rect.texture = null
	imageType = "null"
	image = null
	nome.text = ""
	qtd.text = ""
