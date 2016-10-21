# -*- coding: utf-8 -*-
import sys
import json
import vk_api

LIKES = 1  # Нужно ли записывать людей, которые лайнкули фото
LOGIN = 'login'
PASSWORD = 'password'
GROUP_URL = 'tproger'  # Короткий url или id группы

def authorization():
	vk_session = vk_api.VkApi(LOGIN, PASSWORD)
	try:
		vk_session.authorization()
	except vk_api.AuthorizationError as error_msg:
		print(error_msg)
		return
	return vk_session.get_api()


def choose_album():
	group_id = vk.groups.getById(group_id=GROUP_URL)[0]['id']
	albums = vk.photos.getAlbums(owner_id=-group_id)
	print('Выберите нужный альбом:')
	for i in range(albums['count']):
		print('%d. %s' % (i, albums['items'][i]['title']))
	return albums['items'][int(input('Введите номер альбома: '))]['id'], group_id


def get_photos_data(album_id, owner_id):
	photos = vk.photos.get(owner_id=-owner_id, album_id=album_id)
	print('Найдено фотографий: %d' % photos['count'])
	photos_count = input('Сколько фотографий загрузить (по умолчанию все): ') or photos['count']
	photos_ids = []
	photos_src = []
	if int(photos_count) < 1001:
		for i in range(int(photos_count)):
			photos_ids.append(photos['items'][i]['id'])
			photos_src.append(photos['items'][i]['photo_604'])
	else:
		offset = 0
		while int(photos_count) > offset:
			for i in range(min(1000, int(photos_count) - offset)):
				photos_ids.append(photos['items'][i]['id'])
				photos_src.append(photos['items'][i]['photo_604'])
			offset += 1000
			photos = vk.photos.get(owner_id=-owner_id, album_id=album_id, offset=offset)
	return photos_ids, photos_src


def get_url(owner_id, photo_id):
	return 'https://vk.com/photo%s_%s' % (-owner_id, photo_id)


def get_likes(owner_id, photo_id):
	likes = vk.likes.getList(type='photo', owner_id=-owner_id, item_id=photo_id, count=1000)
	users = []
	if likes['count'] < 1001:
		for i in range(likes['count']):
			users.append('https://vk.com/id' + str(likes['items'][i]))
	else:
		offset = 0
		while likes['count'] > offset:
			for i in range(min(1000, likes['count'] - offset)):
				users.append('https://vk.com/id' + str(likes['items'][i]))
			offset += 1000
			likes = vk.likes.getList(type='photo', owner_id=-owner_id, item_id=photo_id, offset=offset, count=1000)
	return {'count': likes['count'], 'users': users}


def get_comments(owner_id, photo_id):
	comments = vk.photos.getComments(owner_id=-owner_id, photo_id=photo_id, count=100)
	comments_count = int(comments['count'])
	items = {}
	if int(comments_count) < 101:
		for i in range(int(comments_count)):
			items[i] = {
				'user': 'https://vk.com/id' + str(comments['items'][i]['from_id']),
				'text': comments['items'][i]['text']
			}
	else:
		offset = 0
		while int(comments_count) > offset:
			for i in range(min(100, int(comments_count) - offset)):
				items[i] = {
					'user': 'https://vk.com/id' + str(comments['items'][i]['from_id']),
					'text': comments['items'][i]['text']
				}
			offset += 100
			comments = vk.photos.getComments(owner_id=-owner_id, photo_id=photo_id, offset=offset, count=100)
	return {'count': comments_count, 'items': items}


def main():
	global vk
	vk = authorization()
	album_id, owner_id = choose_album()
	photos_ids, photos_src = get_photos_data(album_id, owner_id)
	result = []
	for i in range(len(photos_ids)):
		url = get_url(owner_id, photos_ids[i])
		src = photos_src[i]
		likes = get_likes(owner_id, photos_ids[i]) if LIKES else {}
		comments = get_comments(owner_id, photos_ids[i])
		result.append({
			'url': url,
			'src': src,
			'likes': likes,
			'comments': comments
		})
		sys.stdout.write('\rФото обработано: %i из %i' % (i + 1, len(photos_ids)))
	file = open('photos.json', 'w', encoding='utf8')
	json.dump(result, file, ensure_ascii=False, indent=4)
	file.close()

if __name__ == '__main__':
	main()
