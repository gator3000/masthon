import requests

# Remplacez par votre token d'authentification
user_token = '3lDSRDJRMsxh-W0uuHKhi30BgBYs3B39M-ugn2fd9Ok'

# URL de l'API
url = 'https://mastodon.social/api/v1/media'

# Chemin vers votre fichier image
file_path = 'masthon.png'

# Description de l'image (facultatif)
description = 'test upload'

# Focal point (facultatif, exemple de valeurs)
focus = '-0.69,0.42'

# Ouvrir le fichier image en mode binaire
with open(file_path, 'rb') as file:
    # Préparer les données du formulaire
    files = {
        'file': (file_path, file, 'image/png')
    }

    # Ajouter des paramètres supplémentaires si nécessaire
    data = {
        'description': description
    }

    # Envoyer la requête POST
    headers = {
        'Authorization': f'Bearer {user_token}'
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    # Vérifier la réponse
    if response.status_code == 200:
        print('Image uploadée avec succès!')
        print(response.json())
    else:
        print(f'Erreur lors de l\'upload: {response.status_code}')
        print(response.text)
