from functools import lru_cache
from django.apps import apps

@lru_cache(maxsize=300)
def get_model_class(model_class_ref):
    """>>> get_model_class('my_app_module.MyModelClass')
       MyModelClass
    """
    app_name, model_name = model_class_ref.split('.')
    app_config = apps.get_app_config(app_name)
    return app_config.get_model(model_name)
