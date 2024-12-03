import boto3
import base64
import requests

# Configuração do cliente Rekognition
rekognition = boto3.client('rekognition', region_name='us-east-1')

# Caminho da imagem que será analisada
image_path = 'path_to_your_image.jpg'

# Leitura da imagem
with open(image_path, 'rb') as img_file:
    image_bytes = img_file.read()

# Identificação do famoso
response = rekognition.recognize_celebrities(Image={'Bytes': image_bytes})

# Extraindo informações do famoso
if response['CelebrityFaces']:
    celebrity = response['CelebrityFaces'][0]  # Considerando a primeira celebridade identificada
    name = celebrity['Name']
    print(f"Celebridade identificada: {name}")

    # Gerar uma imagem relacionada com a celebridade usando DALL-E
    dalle_api_url = "https://api.openai.com/v1/images/generations"
    api_key = "your_openai_api_key"  # Substitua pela sua chave API do OpenAI

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    prompt = f"A digital painting of {name} in a surreal and colorful art style"
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post(dalle_api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        dalle_result = response.json()
        image_url = dalle_result['data'][0]['url']
        print(f"Nova imagem gerada: {image_url}")
    else:
        print(f"Erro ao gerar imagem: {response.json()}")
else:
    print("Nenhuma celebridade foi identificada na imagem.")
