extends Button
class_name ItemNaListaDeVender

@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd

var lista : ListaCompras
var dicionario : Dictionary

func _ready() -> void:
	pressed.connect(pressionado)

func pressionado():
	lista.adicionarItem(foto_produto.texture, dicionario)

func setup(image : ImageTexture, f : Dictionary, l : ListaCompras):
	if f['quantidade'] <= 0:
		disabled = true
	label_nome.text = f['nome']
	label_qtd.text = "Restante: " + str(f['quantidade'])
	foto_produto.texture = image
	lista = l
	dicionario = f
