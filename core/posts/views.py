class PostListView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        form = PostForm()
        return render(request, 'posts/post_list.html', {'posts': posts, 'form': form})
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'posts/post_list.html', {'posts': posts, 'form': form})
class PostEditView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, 'posts/post_edit.html', {'form': form, 'post': post})
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        return render(request, 'posts/post_edit.html', {'form': form, 'post': post})
class PostDeleteView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')