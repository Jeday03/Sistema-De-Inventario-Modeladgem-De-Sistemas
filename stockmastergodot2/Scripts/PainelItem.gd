extends Button
class_name PainelItem

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd

var formulario : FormularioItem
var id : int

func _ready() -> void:
	pressed.connect(pressionado)

func pressionado():
	formulario
	pass

func setup(nome: String, imagem: Texture, qtd : int, f : FormularioItem, _id : int):
	label_nome.text = nome
	label_qtd.text = "Restante: " + str(qtd)
	foto_produto.texture = imagem
	formulario = f
	id = _id
