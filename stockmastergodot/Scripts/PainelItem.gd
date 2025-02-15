extends ColorRect

@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelQtd

func _init(textura : Texture2D, nome : StringName, qtd : int) -> void:
	foto_produto.texture = textura
	label_nome.text = nome
	label_qtd.text = "Qtd: " + str(qtd)
