from pathlib import Path
import boto3
from PIL import Image, ImageDraw

# Cliente AWS Rekognition
client = boto3.client("rekognition")


def get_path(file_name: str) -> str:
    """Obtém o caminho completo para a imagem na pasta 'imagem'."""
    return str(Path(__file__).parent / "imagem" / file_name)


def detect_celebrities(image_path: str):
    """Usa o AWS Rekognition para identificar celebridades na imagem."""
    with open(image_path, "rb") as img_file:
        response = client.recognize_celebrities(Image={"Bytes": img_file.read()})
    return response


def draw_boxes_celebrity(image_path: str, output_path: str, response: dict):
    """Desenha caixas ao redor das celebridades e desconhecidos na imagem."""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    width, height = image.size

    for celeb in response.get("CelebrityFaces", []):
        # Obtendo as coordenadas do bounding box
        box = celeb["Face"]["BoundingBox"]
        left = int(box["Left"] * width)
        top = int(box["Top"] * height)
        right = int((box["Left"] + box["Width"]) * width)
        bottom = int((box["Top"] + box["Height"]) * height)

        # Desenha o bounding box e o nome da celebridade
        draw.rectangle([left, top, right, bottom], outline="blue", width=3)
        draw.text((left, top - 10), celeb["Name"], fill="blue")

    for face in response.get("UnrecognizedFaces", []):
        # Obtendo as coordenadas do bounding box
        box = face["BoundingBox"]
        left = int(box["Left"] * width)
        top = int(box["Top"] * height)
        right = int((box["Left"] + box["Width"]) * width)
        bottom = int((box["Top"] + box["Height"]) * height)

        # Desenha o bounding box para rostos desconhecidos
        draw.rectangle([left, top, right, bottom], outline="red", width=3)
        draw.text((left, top - 10), "Desconhecido", fill="red")

    image.save(output_path)
    print(f"Imagem salva com resultados em: {output_path}")


if __name__ == "__main__":
    # Caminhos das imagens
    input_image_path = get_path("photo01.jpg")  # Nome da imagem de entrada
    output_image_path = get_path("resultado_celebridades.jpg")  # Nome da imagem de saída

    # Detectar celebridades na imagem
    response = detect_celebrities(input_image_path)

    # Processa a resposta do AWS Rekognition
    if response.get("CelebrityFaces") or response.get("UnrecognizedFaces"):
        print("Análise concluída:")
        for celeb in response.get("CelebrityFaces", []):
            print(f"Famoso identificado: {celeb['Name']} - Confiança: {celeb['MatchConfidence']:.2f}%")
        for face in response.get("UnrecognizedFaces", []):
            print(f"Rosto não identificado - Confiança: {face['Confidence']:.2f}%")

        # Desenhar as caixas e salvar a imagem processada
        draw_boxes_celebrity(input_image_path, output_image_path, response)
    else:
        print("Nenhum rosto reconhecido.")
