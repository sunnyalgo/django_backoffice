from celery import shared_task
from utils.django_models.dynamic_import import get_model_class
from apps.tasks_pipeline.logic import monitoring_pipeline_task


@shared_task
@monitoring_pipeline_task('messenger.send_email', 'sales.Order')
def send_email(model_instance_pk, task_arguments, *args, **kwargs):
    Order = get_model_class('sales.Order')
    ...
