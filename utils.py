# import aiohttp
# import json
# from flask import current_app
# import requests


# def send_message_requests(data):
#     headers = {
#         "Content-type": "application/json",
#         "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
#     }
#     url = "https://graph.facebook.com/v16.0/112932385092173/messages"
#
#     response = requests.post(url, data=data, headers=headers)
#     print(response)


# async def send_message(data):
#     headers = {
#         "Content-type": "application/json",
#         "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
#     }
#
#     async with aiohttp.ClientSession() as session:
#         url = "https://graph.facebook.com/v16.0/112932385092173/messages"
#         try:
#             async with session.post(url, data=data, headers=headers) as response:
#                 if response.status == 200:
#                     print("Status:", response.status)
#                     print("Content-type:", response.headers["content-type"])
#
#                     html = await response.text()
#                     print("Body:", html)
#                 else:
#                     print(response.status)
#                     print(response)
#         except aiohttp.ClientConnectorError as e:
#             print("Connection Error", str(e))
#
#
# def get_text_message_input(recipient, text):
#     return json.dumps(
#         {
#             "messaging_product": "whatsapp",
#             "to": recipient,
#             "type": "text",
#             "text": {"body": text},
#         }
#     )
