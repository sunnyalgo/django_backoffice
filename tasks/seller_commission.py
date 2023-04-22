from celery import shared_task
from utils.django_models.dynamic_import import get_model_class
from apps.tasks_pipeline.logic import monitoring_pipeline_task


@shared_task
@monitoring_pipeline_task('seller_commission.create_payment', 'sales.Order')
def create_payment(model_instance_pk, task_arguments, *args, **kwargs):
    SellerCommissionPayment = get_model_class('financial.SellerCommissionPayment')
    SellerCommissionPayment.objects.update_or_create(order_id=kwargs['model_instance'].pk,
                                                     defaults={'status': 'new'})
