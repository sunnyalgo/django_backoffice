import os
import pdfkit
from django.conf import settings
from django.template import loader
from celery import shared_task
from utils.django_models.dynamic_import import get_model_class
from apps.tasks_pipeline.logic import monitoring_pipeline_task


@shared_task
@monitoring_pipeline_task('packing_slip.create_pdf_file', 'sales.Order')
def create_pdf_file(model_instance_pk, task_arguments, *args, **kwargs):
    # define pdf path
    order_model = kwargs['model_instance']
    pdf_file_name = f'{order_model.code}.pdf'
    pdf_path = settings.PACKING_SLIP_ROOT / pdf_file_name

    # remove to recreate file
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # generate html content
    content_html = loader.render_to_string(template_name='packing_slip/packing_slip.html',
                                           context={'order': order_model,
                                                    'sheet_name': 'Delivery',
                                                    'add_first_aid_video': 'add_first_aid_video' in task_arguments},
                                           request=None)
    if 'generate_royalties_sheet' in task_arguments:
        content_html += loader.render_to_string(template_name='packing_slip/packing_slip.html',
                                                context={'order': order_model,
                                                         'sheet_name': 'Royalties Payment',
                                                         'add_first_aid_video': 'add_first_aid_video' in task_arguments},
                                                request=None)

    # create pdf file
    pdfkit.from_string(content_html, str(pdf_path))

    # save pdf path on model
    order_model.packing_slip_file = f'{settings.PACKING_SLIP_FOLDER}/{pdf_file_name}'
    order_model.save()
