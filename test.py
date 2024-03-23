import requests
import json
import easygui
from PIL import Image
import os
from io import BytesIO

link = str(input("Enter the link your Immich, inluding the protocol and the / at the end: "))
apikey = str(input("Enter the API key: "))
path = str(input("Enter the path where you want to save the images, including the / at the end: "))
def GetPersons():
  url = link+"api/person"


  payload = {}
  headers = {
    'Accept': 'application/json',
    'x-api-key': apikey
  }


  response = requests.request("GET", url, headers=headers, data=payload)


  return json.loads(response.text)

print(GetPersons())


def GetUUID(liste , personne):
  for i in liste["people"]:
    if i["name"] == personne:
      return i["id"]
  return "Rien trouvé"

def GetAssetsfromperson(id):
  url = link + id + "/assets"


  payload = {}
  headers = {
    'Accept': 'application/json',
    'x-api-key': apikey
  }


  response = requests.request("GET", url, headers=headers, data=payload)


  liste = json.loads(response.text)
  res = []
  for i in liste:
    res.append((i["id"],(i["originalFileName"].split(".")[1])))
  return res


def GetAsset(id):
  url = link + "api/download/asset/"+id

  payload = {}
  headers = {
      'Accept': 'application/octet-stream',
      'x-api-key': apikey
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  # Convert bytes to image
  image = Image.open(BytesIO(response.content))
  return image



dictionnarecomplexe = GetPersons()
noms = []
for i in dictionnarecomplexe["people"]:
  noms.append(i["name"])

choice = easygui.choicebox("Choisissez une personne", choices=noms)
Idchoisi = GetUUID(dictionnarecomplexe, choice)
liste = GetAssetsfromperson(Idchoisi)
print(liste)

folder_path = path + choice + "/"

# Créez le nouveau dossier
os.makedirs(folder_path, exist_ok=True)
longueur = len(liste)
compteur = 0

for i in liste:
  compteur += 1
  image = GetAsset(i[0])
  image.save(folder_path + i[0] + "." + i[1])
  print(compteur,'/',longueur)


