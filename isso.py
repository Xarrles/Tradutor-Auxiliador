# Verifying the file type of the uploaded file to understand how it can be opened.
import magic

file_path = "/mnt/data/lucas"
file_type = magic.from_file(file_path, mime=True)
file_type
