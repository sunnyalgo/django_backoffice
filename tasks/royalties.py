from celery import shared_task
from utils.django_models.dynamic_import import get_model_class
from apps.tasks_pipeline.logic import monitoring_pipeline_task


@shared_task
@monitoring_pipeline_task('royalties.create_payment', 'sales.Order')
def create_payment(model_instance_pk, task_arguments, *args, **kwargs):
    RoyaltiesPayment = get_model_class('financial.RoyaltiesPayment')
    RoyaltiesPayment.objects.update_or_create(order_id=kwargs['model_instance'].pk,
                                              defaults={'status': 'new'})
