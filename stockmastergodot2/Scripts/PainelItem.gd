extends Panel
class_name PainelItem

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd


func set_painel(nome: String, imagem: Texture, qtd : int):
	label_nome.text = nome
	label_qtd.text = "Restante: " + str(qtd)
	foto_produto.texture = imagem
