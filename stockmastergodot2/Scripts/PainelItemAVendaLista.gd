extends Button
class_name ItemNaListaDeVender

@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd

var lista : ListaCompras

func _ready() -> void:
	pressed.connect(pressionado)

func pressionado():
	lista.adicionarItem()

func setup(image : ImageTexture, nome : String, qtd : int, l : ListaCompras):
	if qtd <= 0:
		disabled = true
	label_nome.text = nome
	label_qtd.text = "Restante: " + str(qtd)
	foto_produto.texture = image
	lista = l
