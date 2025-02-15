extends Panel
class_name PainelItem

@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd

func setup(textura : ImageTexture, nome : StringName, qtd : int) -> void:
	foto_produto.texture = textura
	label_nome.text = nome
	label_qtd.text = "Qtd: " + str(qtd)
