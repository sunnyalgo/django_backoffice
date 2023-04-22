import importlib
from core import tasks as tasks_settings

registered_tasks = {}

for full_path in tasks_settings.ALLOWED_TASKS:
    if not registered_tasks.get(full_path):
        package_name, module_name = full_path.rsplit('.', 1)
        package = importlib.import_module(f'tasks.{package_name}')
        module = getattr(package, module_name)
        registered_tasks[full_path] = module

