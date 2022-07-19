from django.shortcuts import render

from proj.celery import debug_task

# Create your views here.
def test_celery(request):
    debug_task.delay()
    print('test_celery')
    return render(request, 'core/test_celery.html')