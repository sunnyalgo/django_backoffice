import os
from celery import Celery
from kombu import Exchange, Queue
from core.tasks import ALLOWED_TASKS

# Set default configuration module name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# declare celery app
app = Celery('core')

# load configs from django settings
app.config_from_object('django.conf:settings')

# discovery tasks from django apps
app.autodiscover_tasks()

# disable results
app.conf.result_expires = 0
app.conf.task_ignore_result = True
app.conf.task_store_errors_even_if_ignored = False

### TODO: Customizing Celery Queues
# # define queues for bulting tasks in django apps
# app.conf.task_create_missing_queues = True
# app.conf.task_queues = [
#     Queue('pipeline_runner',
#           Exchange('pipeline_runner', type='direct'),
#           routing_key='pipeline_runner'),
# ]
#
# # define routes for bulting tasks in django apps
# app.conf.task_routes = {
#     'apps.tasks_pipeline.tasks.pipeline_runner': {'queue': 'pipeline_runner',
#                                                   'routing_key': 'pipeline_runner'}
# }
#
# # define queue routes for pipeline tasks at external modules
# for task_module in ALLOWED_TASKS:
#     # create custom queue
#     task_queue = Queue(task_module,
#                        Exchange(task_module, type='direct'),
#                        routing_key=task_module)
#     app.conf.task_queues.append(task_queue)
#
#     # assign custom queue to task
#     package_path = f'tasks.{task_module}'
#     app.conf.task_routes[package_path] = {'queue': task_module,
#                                           'routing_key': task_module}
