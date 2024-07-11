import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import re

# Se modificar esses escopos, delete o arquivo token.json
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Faz a autenticação e retorna o serviço da API do Google Drive"""
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário, e é
    # criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Se não houver (ou for inválido) o arquivo token.json, o usuário deve fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Salva as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def sanitize_filename(filename):
    """Remove caracteres inválidos do nome do arquivo"""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_specific_photos(service, folder_id, file_names, local_folder):
    """Baixa fotos específicas de uma pasta do Google Drive"""
    os.makedirs(local_folder, exist_ok=True)
    
    list_new_name_images = []
    downloaded_count = 0
    
    for file_name in file_names:
        query = f"'{folder_id}' in parents and name='{file_name}' and mimeType contains 'image/'"
        results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print(f'Nenhuma foto encontrada com o nome: {file_name}')
        else:
            for item in items:
                print(f"Baixando {item['name']}...")
                sanitized_name = sanitize_filename(item['name'])

                list_new_name_images.append(sanitize_filename)
                
                request = service.files().get_media(fileId=item['id'])
                file_path = os.path.join(local_folder, sanitized_name)
                with io.FileIO(file_path, 'wb') as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                        print(f"Progresso do download {int(status.progress() * 100)}%")
                
                downloaded_count += 1
    
    print(f"\nTotal de fotos baixadas: {downloaded_count}")
    return list_new_name_images


def start_download_images(file_names: list):
    folder_id = '1tY0nf5JzeScSieaa4DX8GDjAQ_i59xms'  # Substitua pelo ID da pasta
    local_folder = 'downloads'
    
    service = authenticate()
    list_new_name_images = download_specific_photos(service, folder_id, file_names, local_folder)
    print("Downloads concluídos!")
    print(f'Lista de imagens: {list_new_name_images}')
    return list_new_name_images