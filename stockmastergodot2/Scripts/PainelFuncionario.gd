extends Button
class_name PainelFuncionario

@onready var foto_funcionario: TextureRect = $MarginContainer/HBoxContainer/FotoFuncionario
@onready var label_nome: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelNome
@onready var label_function: Label = $MarginContainer/HBoxContainer/VBoxContainer/LabelFunction

var funcionario : Dictionary
var pai : CadastroFuncionario:
	set(value):
		if not value: return
		pai = value

func _ready() -> void:
	pressed.connect(apertou)

func apertou():
	if not pai:
		printerr("Deu ruim. Botão não tem pai")
		return
	pai.carregarFuncionario(foto_funcionario.texture, funcionario)

func setup(textura : ImageTexture, funcio : Dictionary):
	foto_funcionario.texture = textura
	label_nome.text = funcio['nome']
	label_function.text = funcio['funcao']
	self.funcionario = funcio
