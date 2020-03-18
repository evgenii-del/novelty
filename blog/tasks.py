from novelty.celery import app
from blog.utils import func
from blog.models import Rate


@app.task
def change_cours():
    rates = func()
    for rate in rates:
        if Rate.objects.filter(name=rate['name']).exists():
            r = Rate.objects.filter(name=rate['name'])
            r.update(cours=rate['NBU'])
        else:
            r = Rate(name=rate['name'], cours=rate['NBU'])
            r.save()
