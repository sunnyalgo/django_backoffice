import importlib
import traceback
from functools import wraps
from utils.django_models.dynamic_import import get_model_class


def monitoring_pipeline_task(task_path, model_class_ref):
    def decorator(func):
        ## TODO: auto injecting task function in ALLOWED_TASKS on function definition
        # tasks_module = importlib.import_module('core.tasks')
        # tasks_module.register_task(task_path, func)

        @wraps(func)
        def wrapper(model_instance_pk, task_arguments, *function_args, **function_kwargs):
            # create monitoring object
            Monitoring = get_model_class('tasks_pipeline.Monitoring')
            monitoring_object = Monitoring.objects.create(model_class_ref=model_class_ref,
                                                          model_instance_pk=model_instance_pk,
                                                          task_path=task_path,
                                                          task_arguments=', '.join(task_arguments),
                                                          status='new')

            # get model instance object from pk arguments
            try:
                ModelClass = get_model_class(model_class_ref)
                model_instance = ModelClass.objects.get(pk=model_instance_pk)
            except Exception:
                monitoring_object.status = 'failed'
                monitoring_object.failed_reason = traceback.format_exc()
                monitoring_object.save(update_fields=['status', 'failed_reason'])
                raise

            # execute pipeline task
            try:
                function_kwargs.update({'task_path': task_path,
                                        'model_instance': model_instance,
                                        'model_class_ref': model_class_ref})
                response = func(model_instance_pk, task_arguments, *function_args, **function_kwargs)
            # save failed status
            except Exception:
                monitoring_object.status = 'failed'
                monitoring_object.failed_reason = traceback.format_exc()
                monitoring_object.save(update_fields=['status', 'failed_reason'])
                raise
            # save success status
            else:
                monitoring_object.status = 'success'
                monitoring_object.save(update_fields=['status'])

            return response

        return wrapper

    return decorator
