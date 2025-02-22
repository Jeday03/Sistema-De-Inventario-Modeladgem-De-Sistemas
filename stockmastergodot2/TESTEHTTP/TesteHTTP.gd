extends Node2D

@onready var http_request: HTTPRequest = $HTTPRequest

func _ready() -> void:
	var json = {
		"valor1": 123,
		"valor2": 132
	}
	var body = JSON.stringify(json)
	var header = [] #Se for json, troca pra ["Content-Type: application/json"]
	http_request.request("url", header, HTTPClient.METHOD_GET, body)

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	print(body)
