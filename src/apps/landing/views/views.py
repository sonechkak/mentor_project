import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from django.db import transaction

from landing.forms import AboutMeForm, ContentForm, ProductForm
from landing.models import MainInf, AboutMe, Product, Content
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.core.permissions import IsSuperuserStaffAdmin
from landing.forms import PointFormSet


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

class SaveMainInfLinkView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        field = data.get('field')
        new_link = data.get('link')

        if field not in ['telegram', 'discord', 'vk']:
            return JsonResponse({'success': False, 'error': 'Invalid field'})

        try:
            main_inf = MainInf.objects.first()
            if not main_inf:
                return JsonResponse({'success': False, 'error': 'MainInf not found'})

            setattr(main_inf, field, new_link)

            try:
                main_inf.full_clean()
                main_inf.save()
                return JsonResponse({'success': True})
            except ValidationError as e:
                return JsonResponse({'success': False, 'errors': e.message_dict})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


# AboutMe: Создание, редактирование, удаление
class AboutMeCreate(AdminRequiredMixin, CreateView):
    model = AboutMe
    form_class = AboutMeForm
    template_name = 'landing/includes/about_me_create.html'
    success_url = reverse_lazy('landing:home')


class AboutMeUpdate(AdminRequiredMixin, UpdateView):
    model = AboutMe
    form_class = AboutMeForm
    template_name = 'landing//includes/about_me_edit.html'  # Новый шаблон для редактирования
    success_url = reverse_lazy('landing:home')  # После редактирования перенаправление на главную

    def get_object(self, **kwargs):
        return get_object_or_404(AboutMe, id=self.kwargs['pk'])


class AboutMeDelete(AdminRequiredMixin, DeleteView):
    model = AboutMe
    template_name = 'landing/includes/confirm_delete.html'
    success_url = reverse_lazy('landing:home')


# Content: Создание, редактирование, удаление
class ContentCreate(AdminRequiredMixin, CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'landing/includes/content_create.html'
    success_url = reverse_lazy('landing:home')

    def form_valid(self, form):
        print('Form is valid, saving data...')
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Form is invalid, errors: ', form.errors)
        return super().form_invalid(form)


class ContentUpdate(AdminRequiredMixin, UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'landing/includes/content_edit.html'
    success_url = reverse_lazy('landing:home')


class ContentDelete(AdminRequiredMixin, DeleteView):
    model = Content
    template_name = 'landing/includes/confirm_delete.html'
    success_url = reverse_lazy('landing:home')


# Product: Создание, редактирование, удаление
class ProductCreate(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'landing/includes/product_create.html'
    success_url = reverse_lazy('landing:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['point_formset'] = PointFormSet(self.request.POST)
        else:
            context['point_formset'] = PointFormSet()

        # Сериализация пустой формы для передачи в шаблон
        empty_form = context['point_formset'].empty_form
        context['empty_point_form'] = empty_form.as_p()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        point_formset = context['point_formset']

        # Считаем количество заполненных форм
        valid_forms_count = 0
        for point_form in point_formset:
            if point_form.is_valid() and point_form.cleaned_data.get('text'):  # Проверяем, что текст пункта не пустой
                valid_forms_count += 1

        # Валидация: количество пунктов должно быть от 1 до 7
        if valid_forms_count < 1:
            form.add_error(None, 'Должен быть хотя бы один пункт.')
            return self.form_invalid(form)
        elif valid_forms_count > 7:
            form.add_error(None, 'Максимум 7 пунктов.')
            return self.form_invalid(form)

        if form.is_valid() and point_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()  # Сохраняем продукт
                print(self.object)
                point_formset.instance = self.object  # Присваиваем продукт пунктам
                print(point_formset)
                point_formset.save()  # Сохраняем пункты
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdate(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'landing/includes/product_create.html'  # Используем тот же шаблон, что и для создания
    success_url = reverse_lazy('landing:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['point_formset'] = PointFormSet(self.request.POST, instance=self.object)
        else:
            context['point_formset'] = PointFormSet(instance=self.object)

        # Сериализация пустой формы для передачи в шаблон
        empty_form = context['point_formset'].empty_form
        context['empty_point_form'] = empty_form.as_p()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        point_formset = context['point_formset']

        # Считаем количество заполненных форм
        valid_forms_count = 0
        for point_form in point_formset:
            if point_form.is_valid() and point_form.cleaned_data.get('text'):  # Проверяем, что текст пункта не пустой
                valid_forms_count += 1

        # Валидация: количество пунктов должно быть от 1 до 7
        if valid_forms_count < 1:
            form.add_error(None, 'Должен быть хотя бы один пункт.')
            return self.form_invalid(form)
        elif valid_forms_count > 7:
            form.add_error(None, 'Максимум 7 пунктов.')
            return self.form_invalid(form)

        if form.is_valid() and point_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()  # Сохраняем продукт
                point_formset.instance = self.object  # Присваиваем продукт пунктам
                point_formset.save()  # Сохраняем пункты
            return super().form_valid(form)
        else:
            return self.form_invalid(form)



class ProductDelete(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'landing/includes/confirm_delete.html'
    success_url = reverse_lazy('landing:home')
