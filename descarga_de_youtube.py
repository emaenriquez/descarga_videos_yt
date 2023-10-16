from pytube import YouTube
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#variable del excel

file_path = 'enlace_videos/enlace.xlsx'
sheet_name = 'Hoja1'
column_name = 'videos'

#credenciales google drive
directorio_credenciales = ''
id_folder = ''

def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_number=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

def subir_archivo(ruta_archivo,id_folder):
    credenciales = login()
    archivo = credenciales.CreateFile(({'parents': [{'kind':'dirverfilelink',\
                                                     'id':id_folder}]}))
    archivo['title'] = ruta_archivo.split('/')[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

def main():
    # leer los links del excel
    df = pd.read_excel(file_path,sheet_name=sheet_name)
    column_data = df[column_name]
    videos = column_data.values
    
    #decargar videos de youtube y subirlo a drive
    for link_video in videos:
        # descarga
        yt = YouTube(link_video)
        video = yt.streams.get_highest_resolution()
        video.download('./YT')
        #subir
        subir_archivo(f'YT/{video.title}.mp4',id_folder)

if __name__ == "__main__":
    main()