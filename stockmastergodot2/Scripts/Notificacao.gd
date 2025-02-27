extends Panel
class_name Notificacao

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/FotoProduto
var id : int
var pai : ListaAlerta

func set_alert(nome: String, imagem: ImageTexture, _id: int, _pai):
	label_nome.text = "ALERTA: O " + nome + " possui menos de 10 unidades."
	foto_produto.texture = imagem
	id = _id
	pai = _pai

func _on_button_pressed() -> void:
	pai.deletar(id)
