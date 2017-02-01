import magic


def validate_pdf(uploaded_file):
    """
    Verifica se o arquivo é um PDF
    """
    supported_types = ['application/pdf',]
    mime_type = magic.from_buffer(uploaded_file.file.read(1024), mime=True)
    uploaded_file.file.seek(0)
    if mime_type not in supported_types:
        return False
    return True


def check_student_user(user):
    return not any([user.is_superuser, user.is_staff])


def assign_attr_no_file(obj):
    """
    Atribui a uma string ao atributo responsavel pelo upload, caso ele não
    aponte para um arquivo
    """
    try:
        if not obj.lecture_note.upload.name:
            obj.lecture_note.upload.name = 'noFile'
    except:
        if not obj.upload.name:
            obj.upload.name = 'noFile'
    return obj
