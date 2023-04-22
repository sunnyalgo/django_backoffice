from celery import shared_task
from utils.django_models.dynamic_import import get_model_class
from tasks import registered_tasks


@shared_task
def pipeline_runner(model_class_ref, model_instance_pk):
    ModelClass = get_model_class(model_class_ref)
    model_instance = ModelClass.objects.get(pk=model_instance_pk)
    pipeline_details = model_instance.get_pipeline_details()

    for task_function_path, task_function_args in pipeline_details.items():
        try:
            task_function = registered_tasks.get(task_function_path)
            task_function.delay(model_class_ref=model_class_ref,
                                model_instance_pk=model_instance_pk,
                                task_path=task_function_path,
                                task_arguments=task_function_args)
        except Exception as exc:
            print(exc)
