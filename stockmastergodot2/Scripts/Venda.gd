extends Control
class_name Venda

@onready var line_edit: LineEdit = $VBoxContainer/LineEdit
@onready var spin_box: SpinBox = $VBoxContainer/SpinBox
@onready var lista_alerta: ListaAlerta = null

func _ready() -> void:
	
	lista_alerta = get_node("/root/ListaAlerta")

func _on_button_pressed() -> void:
	var item_id = line_edit.text.to_int()
	var quantidade_vendida = spin_box.value

	
	var item = obter_item_por_id(item_id)
	if item:
		item.quantidade -= quantidade_vendida
		if item.quantidade < 10:
			lista_alerta.adicionar_notificacao(item.nome, item_id)

func obter_item_por_id(item_id: int) -> Dictionary:
	
	var itens = [
		{"id": 1, "nome": "Produto A", "quantidade": 20},
		{"id": 2, "nome": "Produto B", "quantidade": 15}
	]
	for item in itens:
		if item["id"] == item_id:
			return item
	return {}  
