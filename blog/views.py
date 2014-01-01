from django.views.generic import DetailView, ListView
from blog.models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from blog.forms import BookForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.response import SimpleTemplateResponse



def check_same_user_or_superuser(view):
    ''' 
        takes a detail view object and checks if the user is
        the same as the object's creator or if the
        user is a super user
    '''
    return view.request.user == view.get_object().creator or view.request.user.is_superuser

class AllowForCreatorForm(UpdateView):
    '''
        allows user to edit if he's the creator of the post
    '''
    def form_valid(self, form):
        if not check_same_user_or_superuser(self):
            return SimpleTemplateResponse('registration/not_permissioned.html', status=401)
        return super(AllowForCreatorForm, self).form_valid(form)

class DeleteForCreator(DeleteView):
    def delete(self, request, *args, **kwargs):
        if not check_same_user_or_superuser(self):
            return SimpleTemplateResponse('registration/not_permissioned.html', status=401)
        return super(DeleteForCreator, self).delete(request, *args, **kwargs)

class SavedUserForm(CreateView):
    '''adds the user to the form arguments'''
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(SavedUserForm, self).form_valid(form)    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SavedUserForm, self).dispatch(*args, **kwargs)

class BlogList(ListView):
    '''
        displays a list of all blog posts (title/tease)
    '''
    model = Post

class BlogDetail(DetailView):
    '''
        displays a single blog post in full
    '''
    model = Post

class BlogCreate(SavedUserForm):
    '''
        allows creation of a blog post
    '''
    model = Post
    form_class = BookForm

class BlogUpdate(AllowForCreatorForm):
    '''
        allows edit of a blog post
    '''
    model = Post
    form_class = BookForm

class BlogDelete(DeleteForCreator):
    '''
        allows deletion of a blog post
    '''
    model = Post
    success_url = reverse_lazy('blog_list')