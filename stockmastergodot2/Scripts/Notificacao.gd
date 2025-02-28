extends Panel
class_name Notificacao

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
var id : int
var pai : ListaAlerta

func set_alert(nome: String, _id: int, _pai):
	label_nome.text = "ALERTA: O " + nome + " acabou!"
	id = _id
	pai = _pai

func _on_button_pressed() -> void:
	pai.deletar(id)
