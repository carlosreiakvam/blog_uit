from flask import Blueprint, current_app, request, send_from_directory
from flask_ckeditor import upload_fail, upload_success, url_for
from models.vedlegg import Vedlegg
import os
import uuid

router = Blueprint('vedlegg', __name__, url_prefix="/vedlegg")


@router.route('/upload', methods=['POST'])
def upload():
    upload_dir = current_app.config.get("UPLOAD_DIR")
    f = request.files.get('upload')
    filename, extension = os.path.splitext(f.filename)
    if extension not in ['.jpg', '.gif', '.png', '.jpeg']:
        return upload_fail(message='Image only!')
    file_uuid = uuid.uuid4().hex
    vedlegg = Vedlegg(vedlegg_id=file_uuid, vedlegg_navn=f.filename)
    vedlegg.insert()
    f.save(os.path.join(upload_dir, file_uuid))
    url = url_for('vedlegg.uploaded_files', file_uuid=file_uuid)
    return upload_success(url=url)


@router.route('/<file_uuid>')
def uploaded_files(file_uuid):
    upload_dir = current_app.config.get("UPLOAD_DIR")
    vedlegg = Vedlegg.get_by_id(file_uuid)
    return send_from_directory(upload_dir, file_uuid, attachment_filename=vedlegg.vedlegg_navn)
