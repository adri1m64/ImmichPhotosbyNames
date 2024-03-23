import requests
import json
from PIL import Image
import os
from io import BytesIO

link = "Enter the link your Immich, inluding the protocol and the / at the end: "
apikey = "Enter the API key: "
path = "Enter the path where you want to save the images, including the / at the end: "
person = "Enter the name of the person you want to download the images from: "



def GetPersons():
  """Get the list of persons in Immich
  Returns:
      dict -- The list of persons"""
  url = link+"api/person"


  payload = {}
  headers = {
    'Accept': 'application/json',
    'x-api-key': apikey
  }


  response = requests.request("GET", url, headers=headers, data=payload)


  return json.loads(response.text)



def GetUUID(liste , personne):
  """Get the UUID of the asked person
  Arguments:
      liste {dict} -- The list of persons
      personne {str} -- The name of the person
      Returns:
      str -- The UUID of the person"""
  for i in liste["people"]:
    if i["name"] == personne:
      return i["id"]
  return "Rien trouvé"

def GetAssetsfromperson(id):
  """Get the assets of a person
  Arguments:
      id {str} -- The UUID of the person
      Returns:
      list -- The list of assets of the person, with the ID and the extension of the file"""
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

Idchoisi = GetUUID(dictionnarecomplexe, person)
liste = GetAssetsfromperson(Idchoisi)

folder_path = path + person + "/"

# Créez le nouveau dossier
os.makedirs(folder_path, exist_ok=True)
longueur = len(liste)
compteur = 0

for i in liste:
  compteur += 1
  image = GetAsset(i[0])
  image.save(folder_path + i[0] + "." + i[1])
  print(compteur,'/',longueur)