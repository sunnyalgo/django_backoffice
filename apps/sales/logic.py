from functools import lru_cache
from django.utils import timezone
from utils.django_models.dynamic_import import get_model_class


# OrderedProduct model methods with lru cache
@lru_cache(maxsize=1)
def calculate_total_price(price, quantity):
    return price * quantity


@lru_cache(maxsize=1)
def calculate_total_weight(weight, quantity):
    return weight * quantity


@lru_cache(maxsize=1)
def calculate_total_seller_commission(total_price, seller_commission_tax):
    return total_price * (seller_commission_tax / 100)


# Order model methods
def define_order_code(customer_type_name):
    prefix = f'ORD-{customer_type_name[:3]}'.upper()
    code = timezone.now().strftime('%y%m%d-%H%M%S-%f')[:19]
    return f'{prefix}-{code}'


def calculate_order_total_price(order_model):
    return sum([ordered_product.total_price() for ordered_product in order_model.ordered_products.all()])


def calculate_order_total_weight(order_model):
    return sum([ordered_product.total_weight() for ordered_product in order_model.ordered_products.all()])


def calculate_order_total_seller_commission(order_model):
    return sum([ordered_product.total_seller_commission() for ordered_product in order_model.ordered_products.all()])


def get_pipeline_details(order_model):
    pipeline = {}
    PipelineTask = get_model_class('tasks_pipeline.PipelineTask')

    pipeline_tasks_id = order_model.ordered_products.all().values_list(
        'product__product_type__pipeline__tasks', flat=True)
    pipeline_tasks = PipelineTask.objects.filter(id__in=pipeline_tasks_id)

    for pipeline_task in pipeline_tasks:
        task_path = pipeline_task.task.path
        task_arguments = list(pipeline_task.task.arguments.all().values_list('argument', flat=True))
        pipeline[task_path] = pipeline.get(task_path, [])
        pipeline[task_path] += task_arguments

    return pipeline
