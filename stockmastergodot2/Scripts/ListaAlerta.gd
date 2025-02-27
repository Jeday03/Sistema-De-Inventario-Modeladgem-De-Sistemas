extends Control

const NOTIFICACAO = preload("res://PackedScenes/Notificacao.tscn")
@onready var notificacoes_container: VBoxContainer = $VBoxContainer/ScrollContainer/NotificacoesContainer
@onready var http_request: HTTPRequest = $VBoxContainer/ScrollContainer/NotificacoesContainer/HTTPRequest
