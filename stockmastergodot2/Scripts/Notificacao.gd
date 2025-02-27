extends Panel

@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/Label
@onready var foto_produto: TextureRect = $MarginContainer/HBoxContainer/TextureRect

func set_alert(nome: String, imagem: Texture):
    label_nome.text = "ALERTA: O " + nome + " possui menos de 10 unidades."
    foto_produto.texture = imagem