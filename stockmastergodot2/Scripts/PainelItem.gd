extends Button
class_name PainelItem

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd

var formulario : FormularioItem
var dic : Dictionary

func _ready() -> void:
	pressed.connect(pressionado)

func pressionado():
	formulario.selecionaItem(dic, foto_produto.texture)

func setup(imagem: Texture, f : FormularioItem, dicionario : Dictionary):
	label_nome.text = dicionario['nome']
	label_qtd.text = "Restante: " + str(dicionario['quantidade'])
	foto_produto.texture = imagem
	formulario = f
	dic = dicionario
