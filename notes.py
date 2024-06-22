import requests

# URL для скачивания файла
url = "https://drive.usercontent.google.com/download"

# Параметры запроса
params = {
    "id": "1IGENwFzLm8bBEboISadYSNEdxbnjz1fH",
    "confirm": "t"
}

# Отправка GET-запроса
response = requests.get(url, params=params)

# Проверка успешности запроса
if response.status_code == 200:
    # Сохранение полученного файла
    with open('settings.reg', 'wb') as f:
        f.write(response.content)
    print('Файл успешно скачан.')
else:
    print('Произошла ошибка при скачивании файла.')



"""
Здесь я планировал реализовать скачивание через API Google, но решил что проще скопировать ссылку по странице
"""
# import google.auth
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaIoBaseDownload
#
#
# def download_file(real_file_id):
#   """Downloads a file
#   Args:
#       real_file_id: ID of the file to download
#   Returns : IO object with location.
#
#   Load pre-authorized user credentials from the environment.
#   TODO(developer) - See https://developers.google.com/identity
#   for guides on implementing OAuth2 for the application.
#   """
#   creds, _ = google.auth.default()
#
#   try:
#     # create drive api client
#     service = build("drive", "v3", credentials=creds)
#
#     file_id = real_file_id
#
#     # pylint: disable=maybe-no-member
#     request = service.files().get_media(fileId=file_id)
#     file = io.BytesIO()
#     downloader = MediaIoBaseDownload(file, request)
#     done = False
#     while done is False:
#       status, done = downloader.next_chunk()
#       print(f"Download {int(status.progress() * 100)}.")
#
#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     file = None
#
#   return file.getvalue()


# if __name__ == "__main__":
#   download_file(real_file_id="1IGENwFzLm8bBEboISadYSNEdxbnjz1fH")