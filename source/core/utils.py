import magic


def validate_pdf(uploaded_file):
    supported_types = ['application/pdf',]
    mime_type = magic.from_buffer(uploaded_file.file.read(1024), mime=True)
    uploaded_file.file.seek(0)
    if mime_type not in supported_types:
        return False
    return True
