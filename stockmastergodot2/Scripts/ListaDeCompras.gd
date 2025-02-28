extends MarginContainer
class_name ListaCompras

@onready var total: Label = $VBoxContainer/Label
const ITEMA_VENDA_2 = preload("res://PackedScenes/ItemaVenda2.tscn")
@onready var v_box_container: VBoxContainer = $VBoxContainer/ScrollContainer/VBoxContainer
@onready var http_request: HTTPRequest = $HTTPRequest
@onready var margin_container: MarginContainer = $"../MarginContainer"

var carrinho : Array[ItemListaVenda] = []
@onready var accept_dialog: AcceptDialog = $AcceptDialog

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
	var items = []
	for item in carrinho:
		items.append({
			"id": item.dic["id"],
			"quantidade": item.qtd
		})
	var json = {}
	json["items"] = items
	var body = JSON.stringify(json)
	http_request.request("http://127.0.0.1:5000/venda", ["Content-Type: application/json"], HTTPClient.METHOD_POST, body)

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	var response_text = body.get_string_from_utf8()
	var response_json = JSON.parse_string(response_text)
	accept_dialog.dialog_text = response_json['message']
	if response_json['message'] == "Venda realizada com sucesso!":
		for c in v_box_container.get_children():
			c.qtd = 0
	accept_dialog.visible = true
	margin_container.pagAtual = margin_container.pagAtual
