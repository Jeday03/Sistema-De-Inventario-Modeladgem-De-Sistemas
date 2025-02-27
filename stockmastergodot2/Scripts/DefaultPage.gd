extends Control

const TELA_INICIAL : PackedScene = preload("res://Scenes/TelaInicial.tscn")
const LISTA_ITENS : PackedScene = preload("res://Scenes/ListaItens.tscn")
const TELA_VENDAS : PackedScene = preload("res://Scenes/TelaVendas.tscn")
const CADASTRO_FUNCIONARIO : PackedScene = preload("res://Scenes/CadastroFuncionario.tscn")
const LISTA_ALERTA : PackedScene = preload("res://Scenes/ListaAlerta.tscn")

@onready var main_frame: MarginContainer = $MainFrame/MarginContainer
var telaAtual : Control

#ALERT: Aqui, ele pede toda informação que fez antes. Talvez seja interessante manter...
func instanciar(cena : PackedScene):
	if telaAtual:
		telaAtual.queue_free()
	telaAtual = cena.instantiate() as Control
	main_frame.add_child(telaAtual)

func _on_estoque_button_pressed() -> void:
	instanciar(LISTA_ITENS)

func _on_logout_button_pressed() -> void:
	get_tree().change_scene_to_packed(TELA_INICIAL)

func _on_cadastro_button_pressed() -> void:
	instanciar(CADASTRO_FUNCIONARIO)

func _on_vendas_button_pressed() -> void:
	instanciar(TELA_VENDAS)

func _on_pedidos_button_pressed() -> void:
	instanciar(LISTA_ALERTA	)
