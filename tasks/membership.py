from celery import shared_task
from utils.django_models.dynamic_import import get_model_class
from apps.tasks_pipeline.logic import monitoring_pipeline_task


@shared_task
@monitoring_pipeline_task('membership.subscription', 'sales.Order')
def subscription(model_instance_pk, task_arguments, *args, **kwargs):
    Order = get_model_class('sales.Order')
    ...
