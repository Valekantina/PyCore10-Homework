from pathlib import Path
import re
import sys
import shutil

folders = ['IMAGES', 'VIDEO', 'DOCUMENTS', 'AUDIO', 'ARCHIVES']

# creating main folders
images = []
video = []
documents = []
audio = []
archives = []
other = []

# creating folders for extensions
known_ext = []
unknown_ext = []

# creating all extensions
# V2 added extensions .csv, .eml and .gif
IMAGE_EXT = ['JPEG', 'PNG', 'JPG', 'SVG', 'GIF']
VIDEO_EXT = ['AVI', 'MP4', 'MOV', 'MKV']
DOC_EXT = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'CSV', 'EML']
AUDIO_EXT = ['MP3', 'OGG', 'WAV', 'AMR']
ARCHIVE_EXT = ['ZIP', 'GZ', 'TAR']


def check(folder: Path) -> None:
    # creating new directories
    for element in folders:
        new_folder = folder / element
        new_folder.mkdir(exist_ok=True, parents=True)
    return None


# creating the rule for renaming a file in case it was named in cyrillic
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

# creating a function to get the file extentions and create folders from extensions in uppercase


def get_ext(name: str) -> str:
    return Path(name).suffix[1:].upper()

# creating normalize function that will replace cyrillic letters with latin and replace all symbols that are not in latin with "_"
# at the end returns the name of the file in correct format
# V2 added suffix to the renamed file to avoid files being renamed incorrectly


def normalize(name: str) -> str:
    path = Path(name)
    new_name = path.stem
    new_name = name.translate(TRANS)
    new_name = re.sub(r"\W", "_", new_name)
    return new_name + path.suffix

# creating a function that will check the archived files
# V2 added a path to archive and it unpacks it now


def archive_check(folder: Path) -> None:
    for file in folder(folder_to_sort / 'ARCHIVES').iterdir():
        folder_for_file = folder(
            folder_to_sort / 'ARCHIVES' / normalize(file.name.replace(file.suffix, '')))
        folder_for_file.mkdir(exist_ok=True, parents=True)
# unpacking the archive
        try:
            shutil.unpack_archive(str(file.resolve()),
                                  str(folder_for_file.resolve()))
        except shutil.ReadError:
            print(f'The file {file} is not an archive!')
            folder_for_file.rmdir()
            continue
    return None


def sort(folder: Path) -> None:
    # checking files according to their extensions and adding them to the appropriate folder
    # corrected the output for files, as they seem to renamed the files incorrectly
    for element in folder.iterdir():
        if element.is_dir() and element not in folders:
            sort(element)
        else:
            for file in folder.iterdir():
                if file.suffix[1:].upper() in IMAGE_EXT:
                    images_folder = Path('images')
                    file.replace(folder_to_sort / images_folder / file.name)

                if file.suffix[1:].upper() in VIDEO_EXT:
                    video_folder = Path('VIDEO')
                    file.replace(folder_to_sort / video_folder / file.name)

                if file.suffix[1:].upper() in DOC_EXT:
                    document_folder = Path('DOCUMENTS')
                    file.replace(folder_to_sort / document_folder / file.name)

                if file.suffix[1:].upper() in AUDIO_EXT:
                    audio_folder = Path('AUDIO')
                    file.replace(folder_to_sort / audio_folder / file.name)

                if file.suffix[1:].upper() in ARCHIVE_EXT:
                    archive_folder = Path('ARCHIVES')
                    file.replace(folder_to_sort / archive_folder / file.name)
                else:
                    normalize(file.name)
                    if not file.is_dir():
                        unknown_ext.append(file.suffix)
    return None

# creating function to delete empty folders
# V2 added a path for empty folder


def empty_folder(folder: Path) -> None:
    for element in folder.iterdir():
        if element.is_dir():
            if element.name not in folders:
                empty_folder(element)
                try:
                    element.rmdir()
                except:
                    print(
                        f'Folder {element} is not empty and cannot be deleted')
                    continue
    return None


# defining what the system should process sorting/cleaning
# V2 corrected the arguments as per mentors comments
def clean_folder(known_ext=known_ext,
                 unknown_ext=unknown_ext,
                 images=images,
                 video=video,
                 documents=documents,
                 audio=audio,
                 archives=archives):
    # checking if the arguments were provided correctly
    if len(sys.argv) != 2:
        print(f'Please specify the directory you wish to clean')
        quit()
    global folder_to_sort
    folder_to_sort = Path(sys.argv[1])
    if not Path(folder_to_sort).is_dir():
        print(f'The directory you provided is not a folder. Please provide a correct directory.')
        quit()

    check(folder_to_sort)
    sort(folder_to_sort)
    archive_check(folder_to_sort)
    empty_folder(folder_to_sort)
# outputting the results of the sort and providing a list of all files and extensions that were in the folder
    known_ext = list(set(known_ext))
    print(f'All known extensions: {known_ext}')
    unknown_ext = list(set(unknown_ext))
    print(f'All unknown extensions: {unknown_ext}')
    images = list(set(images))
    print(f'List of all images files: {images}')
    video = list(set(video))
    print(f'List of all video files: {video}')
    documents = list(set(documents))
    print(f'List of all documents files: {documents}')
    audio = list(set(audio))
    print(f'List of all audio files: {audio}')
    archives = list(set(archives))
    print(f'List of all archive files: {archives}')


# making sure the code will only run when sort.py file is executed as a script

if __name__ == '__main__':
    clean_folder(known_ext=known_ext,
                 unknown_ext=unknown_ext,
                 images=images,
                 video=video,
                 documents=documents,
                 audio=audio,
                 archives=archives)
