from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView

from Blog.models import News, Comment, User
from Blog.forms import AddCommentForm


class BlogListView(ListView):
    model = News
    template_name = 'pages/blog.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(draft=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новостной блог'
        context['blog_selected'] = 'active'
        context['headline'] = ('Latest From our Blog', 'Читать дальше...')
        return context


class BlogDetailView(FormView, DetailView):
    model = News
    template_name = 'pages/blog-single.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'single_post'
    queryset = News.objects.filter(draft=False)
    form_class = AddCommentForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object)
        context['count'] = context['comments'].count()
        context['responses'] = 'Отзывов'
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(BlogDetailView, self).form_valid(form)

    def post(self, request, **kwargs):
        form = AddCommentForm(request.POST)
        news = News.objects.get(id=kwargs['pk'])
        creator = User.objects.get(id=self.request.user.id)
        if form.is_valid():
            form = form.cleaned_data
            if request.POST.get('parent', None):
                parent = Comment.objects.get(id=int(request.POST.get('parent')))
            else:
                parent = None
            comment = Comment(
                text=form['text'],
                parent=parent,
                news=news,
                creator=creator,
            )
            comment.save()

        return redirect(news.get_absolute_url())
