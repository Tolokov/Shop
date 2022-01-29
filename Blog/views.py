from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import ListView, DetailView, FormView

from Blog.models import News, Comment, User
from Blog.forms import AddCommentForm
from Blog.utils import DataMixin


class BlogListView(ListView):
    """Отображение списка всех статей с добавленной пагинацией"""
    model = News
    template_name = 'pages/blog.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = News.objects.filter(draft=False).select_related('creator')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Подсветка активной страницы"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новостной блог'
        context['blog_selected'] = 'active'
        return context


class SearchResultsListView(BlogListView):

    def get_queryset(self):
        """Получение поискового запроса на странице с новостями и возвращение результата"""
        user_search_request = self.request.GET.get('s')
        request = self.get_results_filter(user_search_request)
        return request

    @staticmethod
    def get_results_filter(request):
        """Формирование ответа"""
        objects = News.objects.filter()
        result = objects.filter(
            Q(title__icontains=request) |
            Q(description__icontains=request)
        ).select_related('creator')
        return result


class BlogDetailView(FormView, DetailView, DataMixin):
    model = News
    template_name = 'pages/blog-single.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'single_post'
    queryset = News.objects.filter(draft=False).select_related('creator')
    form_class = AddCommentForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object).select_related('creator')
        context['count'] = context['comments'].__len__()
        context = self.check_next_and_prev_pages(context)
        return context

    def post(self, request, **kwargs):
        """Сохранение комментариев к новостям"""
        form = AddCommentForm(request.POST)

        if form.is_valid():
            news = News.objects.get(id=kwargs['pk'])
            creator = User.objects.get(id=self.request.user.id)
            form = form.cleaned_data
            parent = None
            if request.POST.get('parent', None):
                parent = Comment.objects.get(id=int(request.POST.get('parent')))

            comment = Comment(text=form['text'], parent=parent, news=news, creator=creator)
            comment.save()

        return redirect(news.get_absolute_url(), permanent=True)
