extends Control

const TELA_INICIAL : PackedScene = preload("res://Scenes/TelaInicial.tscn")
const LISTA_ITENS : PackedScene = preload("res://Scenes/ListaItens.tscn")
@onready var main_frame: HBoxContainer = $MainFrame
var telaAtual : Control

func instanciar(cena : PackedScene):
	if telaAtual:
		telaAtual.queue_free()
	telaAtual = cena.instantiate() as Control
	main_frame.add_child(telaAtual)

func _on_estoque_button_pressed() -> void:
	instanciar(LISTA_ITENS)
	pass # Replace with function body.


func _on_logout_button_pressed() -> void:
	get_tree().change_scene_to_packed(TELA_INICIAL)
