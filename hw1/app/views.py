from django.views import View, generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Context
from django.shortcuts import get_object_or_404

class IndexView(generic.ListView):
    model = Context  # Specify the model for the ListView
    template_name = "app/index.html"
    context_object_name = "latest_context_list"


class AddContextView(View):
    def post(self, request):
        new_context = Context(
            Context_text=request.POST["context_text"],
            Created_date    =timezone.now(),
        )
        new_context.save()
        return HttpResponseRedirect(reverse("app:index"))
    
class DeleteContextView(View):
    def post(self, requet, context_id):
        context = get_object_or_404(Context, id=context_id)
        #context = get_object_or_404(Context, id=request.POST["id"])
        context.Delete_date = timezone.now()
        context.save()
        return HttpResponseRedirect(reverse('app:index'))

class EditContextView(View):
    def post(self, request, context_id):
        context = get_object_or_404(Context, id=context_id)
        context.Context_text = request.POST['context_text']
        context.save()
        return HttpResponseRedirect(reverse('app:index'))