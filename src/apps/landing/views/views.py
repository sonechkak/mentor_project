import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView

from landing.forms import MainInfForm, AboutMeForm, ContentForm, ProductForm
from landing.models import MainInf, AboutMe, Product, Content
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.core.permissions import IsSuperuserStaffAdmin


class SaveMainInfTextView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            # Изменение полей модели
            main_inf = MainInf.objects.first()
            main_inf.title = data['title']
            main_inf.text = data['text']
            main_inf.full_clean()
            main_inf.save()

            return JsonResponse({'success': True})

        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': e.message_dict})

        except MainInf.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'MainInf not found'})

        except Exception as e:
            # Перехватываем все другие ошибки и выводим
            return JsonResponse({'success': False, 'error': str(e)})

class SaveMainInfImgView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        if request.FILES:
            image = request.FILES.get('image')
            if image:
                # Сохранение изображения
                main_inf = MainInf.objects.first()
                main_inf.image = image

                try:
                    main_inf.full_clean()  # Валидируем модель, включая изображение
                    main_inf.save()
                    return JsonResponse({'success': True})
                except ValidationError as e:
                    return JsonResponse({'success': False, 'errors': e.message_dict})
            else:
                return JsonResponse({'success': False, 'errors': 'No image uploaded'})
        return JsonResponse({'success': False, 'errors': 'Invalid request'})

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin для проверки прав администратора.
    """
    def test_func(self):
        return IsSuperuserStaffAdmin().has_permission(self.request, self)

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем первый(единственный) экземпляр MainInf
        main_inf = MainInf.objects.first()

        # Получаем все записи из AboutMe
        about_me_list = AboutMe.objects.all()

        # Получаем все записи из Product
        product_list = Product.objects.all()

        # Получаем все записи из Content
        content_list = Content.objects.all()

        context['main_inf'] = main_inf
        context['about_me_list'] = about_me_list
        context['product_list'] = product_list
        context['content_list'] = content_list

        return context

# MainInf: Редактирование полей
class MainInfEditView(AdminRequiredMixin, FormView):
    template_name = 'landing/maininf_edit.html'
    form_class = MainInfForm
    success_url = reverse_lazy('landing:home')

    def get_form(self, *args, **kwargs):
        main_inf = MainInf.objects.first()
        return self.form_class(instance=main_inf, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# AboutMe: Создание, редактирование, удаление
class AboutMeCreate(AdminRequiredMixin, CreateView):
    model = AboutMe
    form_class = AboutMeForm
    template_name = 'landing/about_me_form.html'
    success_url = reverse_lazy('landing:home')


class AboutMeUpdate(AdminRequiredMixin, UpdateView):
    model = AboutMe
    form_class = AboutMeForm
    template_name = 'landing/about_me_form.html'
    success_url = reverse_lazy('landing:home')


class AboutMeDelete(AdminRequiredMixin, DeleteView):
    model = AboutMe
    template_name = 'landing/confirm_delete.html'
    success_url = reverse_lazy('landing:home')


# Content: Создание, редактирование, удаление
class ContentCreate(AdminRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'landing/content_form.html'
    success_url = reverse_lazy('landing:home')


class ContentUpdate(AdminRequiredMixin, UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'landing/content_form.html'
    success_url = reverse_lazy('landing:home')


class ContentDelete(AdminRequiredMixin, DeleteView):
    model = Content
    template_name = 'landing/confirm_delete.html'
    success_url = reverse_lazy('landing:home')


# Product: Создание, редактирование, удаление
class ProductCreate(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'landing/product_form.html'
    success_url = reverse_lazy('landing:home')


class ProductUpdate(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'landing/product_form.html'
    success_url = reverse_lazy('landing:home')


class ProductDelete(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'landing/confirm_delete.html'
    success_url = reverse_lazy('landing:home')
