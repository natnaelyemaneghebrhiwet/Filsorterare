import os
import shutil
import typer
from typing import List, Optional

app = typer.Typer()

def display_contents(folder_path: str) -> List[str]:
    """
    Visa innehållet i en mapp och returnera en lista av filer och mappar.
    """
    contents = os.listdir(folder_path)
    return contents

def sort_files(source_folder: str, destination_folders: dict):
    """
    Sortera filer från en källmapp till olika målmappar baserat på deras filtyper.
    """
    # Skapa målmappar om de inte redan finns
    for folder in destination_folders.values():
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Gå igenom varje fil i källmappen och flytta den till rätt målmapp
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        if os.path.isfile(source_path):
            _, file_extension = os.path.splitext(file_name)
            if file_extension.lower() in destination_folders:
                destination_folder = destination_folders[file_extension.lower()]
                destination_path = os.path.join(destination_folder, file_name)
                shutil.move(source_path, destination_path)

@app.command()
def sort_files_interactive():
    """
    Interaktivt gränssnitt för att välja och sortera filer från en källmapp.
    """
    current_directory = os.getcwd()
    source_folder = current_directory
    while True:
        typer.clear()
        typer.echo("Innehållet i mappen:")
        contents = display_contents(source_folder)
        for item in contents:
            typer.echo(f"- {item}")

        typer.echo("\nNavigera till en mapp genom att skriva dess namn.")
        typer.echo("Ange en mapp och tryck på Enter för att fortsätta, eller tryck på Enter för att sortera.")

        folder_choice = typer.prompt("Mapp: ", default="")

        if folder_choice == "":
            break

        new_folder_path = os.path.join(source_folder, folder_choice)
        if os.path.isdir(new_folder_path):
            source_folder = new_folder_path
        else:
            typer.echo("Ogiltig mapp!")

    # Definiera målmappar för olika filtyper
    destination_folders = {
        ".jpg": "bilder",
        ".jpeg": "bilder",
        ".png": "bilder",
        ".pdf": "PDF",
        ".mp4": "video",
        ".mp3": "music",
        ".doc": "dokument",
        ".docx": "dokument"
        # Lägg till fler filtyper och motsvarande målmappar här
    }

    typer.confirm("Sortera filer?", abort=True)
    sort_files(source_folder, destination_folders)
    typer.echo("Filerna har sorterats.")

if __name__ == "__main__":
    app()
