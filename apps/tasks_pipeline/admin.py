from django.conf import settings
from admin_site import admin
from utils.django_models.dynamic_import import get_model_class

from apps.tasks_pipeline.models import Task, TaskArgument, Pipeline, PipelineTask, Monitoring


# Task admin
class TaskArgumentInLineAdmin(admin.TabularInline):
    model = TaskArgument
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'arguments')
    search_fields = ('name', 'path')
    ordering = ('id',)
    inlines = [TaskArgumentInLineAdmin]

    def arguments(self, obj):
        return ', '.join(obj.get_arguments())


# Pipeline admin
class PipelineTaskInLineAdmin(admin.TabularInline):
    model = PipelineTask
    extra = 1


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'tasks')
    search_fields = ('name',)
    ordering = ('id',)

    inlines = [PipelineTaskInLineAdmin]

    def tasks(self, obj):
        names = obj.tasks.all().values_list('task__name', flat=True)
        ordered_names = [f'({index + 1}) {name}' for index, name in enumerate(names)]
        return ' -> '.join(list(ordered_names))


@admin.register(Monitoring)
class MonitoringAdmin(admin.ModelAdmin):
    list_display = ('status', 'model_object', 'model_instance', 'task_path', 'task_arguments',
                    'task_created_at', 'task_updated_at', 'task_failed_reason')
    list_filter = ('status', 'model_class_ref', 'task_path')
    ordering = ('-created_at',)
    search_fields = ('model_instance_pk', 'task_path', 'task_arguments', 'failed_reason')

    def model_object(self, obj):
        return f'{obj.model_class_ref} ({obj.model_instance_pk})'

    def model_instance(self, obj):
        try:
            ModelClass = get_model_class(obj.model_class_ref)
            return ModelClass.objects.get(pk=obj.model_instance_pk)
        except Exception:
            ...

    def task_created_at(self, obj):
        return obj.created_at.strftime(settings.DEFAULT_TIME_FORMAT)

    def task_updated_at(self, obj):
        return obj.updated_at.strftime(settings.DEFAULT_TIME_FORMAT)

    def task_failed_reason(self, obj):
        if obj.failed_reason:
            return obj.failed_reason[100:]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
