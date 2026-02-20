from .models import Profile
from .models import Times, Time_Achievements
from .models  import ProfilePersonalRecord
from django.urls import reverse_lazy
from Social.models import Comment, Post
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.views.generic import CreateView, UpdateView, FormView, DeleteView, DetailView, ListView
from .forms import ProfileForm, UserFormUpdate, ProfileFormUpdate,CustomCreateUser, PersonalRecordForm, PrivacyConfigForm, TimeForm

from .serializers import CreateUserSerializer, CreateProfileSerializer, UserUpdatePasswordSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer, PrivacySerializer, CreateTeamSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView,  DestroyAPIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.generics import UpdateAPIView
from rest_framework import status





class RegisterAPIView(APIView):
    def post(self, request):
        user_serializer = CreateUserSerializer(request.data)
        profile_serializer = CreateProfileSerializer(request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            profile = profile_serializer.save(commit=False)
            profile.user = user
            profile.save()
            return Response({"message": "User registered successfully"}, status=201)
        
        errors = {
            "user_errors": user_serializer.errors,
            "profile_errors": profile_serializer.errors
        }
        return Response(errors, status=400)


class RegisterAPIViewTemplate(TemplateView):
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        user_serializer = CreateUserSerializer(request.data)
        profile_serializer = CreateProfileSerializer(request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            profile = profile_serializer.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
        
        errors = {
            "user_errors": user_serializer.errors,
            "profile_errors": profile_serializer.errors
        }
        return render(request, self.template_name, {"errors": errors})

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    

    def get_object(self):
        return self.request.user
    
class UserUpdatePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdatePasswordSerializer

    def get_object(self):
        return self.request.user



class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=200)
        return Response({"error": "Invalid credentials"}, status=400)
    



class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=200)
    


class UserList(ListView):
    model = User
    template_name = 'home.html'
    context_object_name = 'search_users'
    
    def get_queryset(self):
        
        search  = self.request.GET.get('search')
        if search:
            return User.objects.filter(username__icontains = search)
        
        return User.objects.all()



@login_required(login_url='login')
def user_update(request):
    user = request.user
    profile = user.profile
   
    
    if request.method == 'POST':
        form_type = request.POST.get('submit_type')

        form = UserFormUpdate(request.POST, instance=user)
        form_privacy = PrivacyConfigForm(instance=profile)

        if form_type == 'user_form':
            form = UserFormUpdate(request.POST, instance=user)
            
            if form.is_valid():
                form.save()
                return redirect('my_perfil')
            


        elif form_type == 'privacy_form':
            
            form_privacy = PrivacyConfigForm(request.POST, instance=profile)

            if form_privacy.is_valid():
                form_privacy.save()
                return redirect('my_perfil')


    else:
        form = UserFormUpdate(instance=user)
        form_privacy = PrivacyConfigForm(instance=profile)
 
    return render(request, 'user-update.html', {
        'form': form,
        'form_privacy': form_privacy,
      
    })




class UserUpdate(UpdateView):


    model = User
    form_class = UserFormUpdate
    template_name = 'user-update.html'
    success_url = reverse_lazy('my_perfil')

    
    def get_object(self):
        
        return self.request.user

    def form_valid(self, form):
        print("Dados recebidos no POST:", self.request.POST)
        response = super().form_valid(form)

        # Atualiza também o perfil
        profile = self.request.user.profile
        profile.box = self.request.POST.get('box')
        profile.category = self.request.POST.get('category')
        profile.weight = self.request.POST.get('weight')
        profile.height =  self.request.POST.get('height')
        profile.genre = self.request.POST.get('genre')
        
        
        profile.save()

        return response
    
    def form_invalid(self, form):
        print("Dados recebidos no POST:", self.request.POST)
        # You can print the errors to debug
        print(form.errors)

        # You can log or customize the response here
        return super().form_invalid(form)
    


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordUpdate(LoginRequiredMixin, FormView):
    template_name = 'pass-update.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login') 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserDelete(DeleteView):
    model = User
    template_name = 'user-delete.html'
    success_url = reverse_lazy ('home')

    



@method_decorator(login_required(login_url='login'), name='dispatch')
class PhotoUpdate(UpdateView):
    model = Profile 
    form_class = ProfileFormUpdate
    template_name = 'photo-update.html'
    success_url = reverse_lazy('my_perfil')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'  
        return context
    
    def get_object(self, queryset=None):
        return self.request.user.profile 
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class PhotoDelete(DeleteView):
    model = Profile
    template_name = 'photo-update.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.photo.delete(save=True)
        return redirect('user-detail', pk=self.object.user.pk)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.action = 'delete'  
        return context

    def get_object(self, queryset = ...):
        return self.request.user.profile
    
class ProfileDetail(DetailView):
    
    def get(self, request, pk):
        user_profile = get_object_or_404(User, pk=pk)
        
        posts = Post.objects.filter(author=user_profile).order_by('-created_at')
        comments = Comment.objects.filter(author=user_profile).order_by('-created_at')
        return render(request, 'profile.html', {
            'user_profile': user_profile,
            
            'posts': posts,
            'comments': comments,
        })
    

def register_pr (request):
    
    if request.method == 'POST':
        form = PersonalRecordForm(request.POST, user=request.user)

        if form.is_valid():
            pr =  form.save(commit=False)
            pr.athlete = request.user
            pr.save()
            return redirect('list_pr')
        
    else:
        form  = PersonalRecordForm()

    return  render (request, 'create_pr.html',{'form':form})

def update_pr (request,pk):
    obj =  get_object_or_404(ProfilePersonalRecord,  pk  = pk)
    
    if  obj.athlete!=request.user:
        return HttpResponseForbidden("Você não tem permissão para editar este registro.")

    if request.method =='POST':
        new_pr =  request.POST.get('personal_record')
        
        if new_pr:
            obj.personal_record = new_pr
            obj.save()
            return redirect('my_perfil')
    return render  (request,'update_pr.html',{'obj':obj})

def list_pr(request):

    detail = ProfilePersonalRecord.objects.filter(athlete=request.user)

    return render(request, 'home_pr.html',  {'pr_list':detail})



class PrivacyConfigAPIView(APIView):


    def post(self, request):
        profile = request.user.profile
        privacy_serializer = PrivacySerializer(profile, data = request.data)

        
        if privacy_serializer.is_valid():
            data = privacy_serializer.validated_data
            privacy_serializer.save()
            return Response({"message": "Privacy configuration updated successfully"}, status=201)
         

        return Response(privacy_serializer.errors, status=400)  
    
class  CreateTeamAPIView(APIView):


    def post(self, request):
     
        create_team_serializer = CreateTeamSerializer( data = request.data)
      
        if create_team_serializer.is_valid():
            data = create_team_serializer.validated_data
            create_team_serializer.save(creator=request.user)
            return Response({"message": "Create Team successfully"}, status=201)
        
        return Response(create_team_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_time(request):
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            time = form.save(commit=False)
            time.creator = request.user
            time.save()
            return redirect('update_time', time_id=time.id)
    else:
        form = TimeForm()

    return render(request, 'create_time.html', {'form': form})

def detail_time(request, time_id):
    time = get_object_or_404(Times, id=time_id)
    membros = time.membros.all()
    return render(request, 'detail_time.html', {'time': time, 'membros': membros})

def add_member(request, time_id):
    time = get_object_or_404(Times, id=time_id)

    if time.creator != request.user:
        return HttpResponseForbidden("Você não é o dono deste time.")

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = get_object_or_404(User, id=usuario_id)
        time.membros.add(usuario)
        return redirect('update_time', time_id=time.id)


    return render(request, 'update_time.html', {'time': time, })

def my_time(request):

    user =  request.user
    times = Times.objects.filter(creator = user)
    return render(request, 'my_perfil.html', {'times': times})
    
def list_time(request):
    times = Times.objects.all()
    time_achievements = Time_Achievements.objects.filter(time__in=times) 
    return render(request, 'list_time.html',{'times':times, 'time_achievements': time_achievements})
    
def delete_time(request, time_id):
    time = get_object_or_404(Times, id=time_id)

    if request.method == 'POST':
        if time.creator == request.user:
            time.delete()
            return redirect('list_time')  
        else:
            return HttpResponseForbidden("Você não tem permissão para deletar este registro.")
    else:
        return HttpResponseForbidden("Método não permitido.")
    
def remove_member(request, time_id, user_id):
    time = get_object_or_404(Times, id = time_id)
    if request.method == 'GET':
        if time.creator == request.user:
            member = get_object_or_404(time.membros.all(), id=user_id)
            time.membros.remove(member)

        return redirect('update_time', time_id=time_id)
    
    else:
        
        return HttpResponseForbidden("Erro em remover membro!")

def update_time(request, time_id):
    time = get_object_or_404(Times, pk=time_id)
    usuarios_disponiveis = User.objects.exclude(id__in=time.membros.values_list('id', flat=True))
    if request.method == 'POST':
        if time.creator == request.user:
            form = TimeForm(request.POST, instance=time)
            if form.is_valid():
                form.save()
                return redirect('detail_time', time_id=time_id)
    else:
        form = TimeForm(instance=time)

    return render(request, 'update_time.html', {'form': form, 'time': time, 'usuarios_disponiveis': usuarios_disponiveis})