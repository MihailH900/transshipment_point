import json
def text_button(label, color, payload=""): 
	return{
	"action": { 
		"type": "text", 
		"payload": json.dumps(payload),
		"label": label 
	},
	"color": color
}
def location_button(payload=""): 
	return { 
	"action":{ 
		"type": "location",
		"payload": json.dumps(payload)
	}
}
def link_button(link, label, payload=""): 
	return { 
	"action":{ 
	"type": "open_link",
	"payload": json.dumps(payload), 
	"label": label
	}
}
