extends MarginContainer
class_name ListaCompras

@onready var total: Label = $VBoxContainer/Label
const ITEMA_VENDA_2 = preload("res://PackedScenes/ItemaVenda2.tscn")
@onready var v_box_container: VBoxContainer = $VBoxContainer/ScrollContainer/VBoxContainer
@onready var http_request: HTTPRequest = $HTTPRequest

var carrinho : Array[ItemListaVenda] = []

func adicionarItem(t : ImageTexture, d : Dictionary):
	var instancia : ItemListaVenda = ITEMA_VENDA_2.instantiate()
	v_box_container.add_child(instancia)
	instancia.setup(t, d, self as ListaCompras)
	carrinho.append(instancia)
	atualizarTotal()

func atualizarTotal():
	var ptotal : float = 0
	for p in carrinho:
		ptotal += p.qtd * p.dic['preco']
	total.text = "R$" + str(ptotal)

func removerItem(i : ItemListaVenda):
	carrinho.erase(i)
	atualizarTotal()

#FINALIZAR A COMPRA
func _on_button_pressed() -> void:
	pass # Replace with function body.
