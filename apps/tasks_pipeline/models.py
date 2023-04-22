from django.db import models
from django.utils import timezone
from utils.django_models.field_choices import create_choices_tuple

pipeline_task_status = ('new', 'running', 'success', 'failed')


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    path = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_arguments(self):
        args = self.arguments.all().values_list('argument', flat=True)
        return tuple(args)


class TaskArgument(models.Model):
    argument = models.CharField(max_length=100)
    task = models.ForeignKey('tasks_pipeline.Task', related_name='arguments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task.name}: {self.argument}'


class Pipeline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class PipelineTask(models.Model):
    pipeline = models.ForeignKey('tasks_pipeline.Pipeline', on_delete=models.CASCADE, related_name='tasks')
    task = models.ForeignKey('tasks_pipeline.Task', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)

    def __str__(self):
        return f'{self.pipeline.name}: {self.task.name}'


class Monitoring(models.Model):
    model_class_ref = models.CharField(max_length=255)
    model_instance_pk = models.IntegerField()
    task_path = models.CharField(max_length=300)
    task_arguments = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='new', choices=create_choices_tuple(pipeline_task_status))
    failed_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)

    def __str__(self):
        return f'Task execution ({self.task_path}): for model ({self.model_class_ref}, {self.model_instance_pk})'
