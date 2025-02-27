extends Panel
class_name ItemListaVenda

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
@onready var label_qtd: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelResto
@onready var label_preco: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelPreco
@onready var line_edit: LineEdit = $MarginContainer/HBoxContainer/VBoxContainer2/LineEdit

var formulario : FormularioItem
var dic : Dictionary

var qtd : int = 1:
	set(value):
		qtd = value
		if qtd <= 0:
			queue_free()
		label_preco.text = "R$" + str(dic['preco'] * qtd)

func setup(imagem: Texture, f : FormularioItem, dicionario : Dictionary):
	label_nome.text = dicionario['nome']
	label_qtd.text = "Restante: " + str(dicionario['quantidade'])
	foto_produto.texture = imagem
	formulario = f
	dic = dicionario

func _on_line_edit_text_submitted(new_text: String) -> void:
	var n = int(new_text)
	if n == 0: n = 1
	qtd = n

func _on_decrease_pressed() -> void:
	qtd -= 1

func _on_increase_pressed() -> void:
	qtd += 1
