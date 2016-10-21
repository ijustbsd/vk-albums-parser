vk-albums-parser
===
Скрипт позволяет сохранять фотографии из групп ВК и комментарии к ним в формате JSON

Для работы требуется модуль [vk_api](https://github.com/python273/vk_api)

Пример вывода
---
```json
[
	{
		"url": "https://vk.com/photo-30666517_314212212",
		"comments": {
			"count": 1,
			"items": [
				{
					"text": "Когда Линусу Торвальдсу скучно, он роняет Сервер Пентагона и Белого Дома. При помощи всё того же уличного банкомата (с) Лурк",
					"user": "https://vk.com/id37911510"
				}
			]
		},
		"likes": {
			"count": 17,
			"users": [
				"https://vk.com/id51371703",
				"https://vk.com/id12781845",
				"https://vk.com/id2713792",
				"https://vk.com/id28447781",
				"https://vk.com/id164216885",
				"https://vk.com/id35732904",
				"https://vk.com/id4270794",
				"https://vk.com/id99640344",
				"https://vk.com/id111391893",
				"https://vk.com/id87401066",
				"https://vk.com/id211029686",
				"https://vk.com/id53366978",
				"https://vk.com/id139566830",
				"https://vk.com/id26204882",
				"https://vk.com/id144256989",
				"https://vk.com/id37131193",
				"https://vk.com/id880893"
			]
		},
		"src": "https://cs7059.vk.me/c540102/v540102973/6faf/0iNQTVHay8Y.jpg"
	}
]
```
