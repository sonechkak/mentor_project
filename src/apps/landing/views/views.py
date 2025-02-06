from django.views.generic import TemplateView

from landing.models import MainInf, AboutMe, Product, Content


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

        # Получаем все записи из ModelC
        content_list = Content.objects.all()

        context['main_inf'] = main_inf
        context['about_me_list'] = about_me_list
        context['product_list'] = product_list
        context['content_list'] = content_list

        return context