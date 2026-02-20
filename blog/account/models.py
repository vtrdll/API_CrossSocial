from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.








class  Box(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= "Criador")
    box_name = models.CharField(max_length=20, null=False,  blank= False, verbose_name= "Nome da BOX")

    def __str__(self):
        return f'Box {self.box_name} -'

class Profile (models.Model):
    
    
    CATEGORY_CHOICES = (('FITNESS', 'FITNESS'), ('SCALED','SCALED'),('AMADOR', 'AMADOR'), ('RX','RX',), ('MASTER', 'MASTER'))
    GENRE_CHOICES =(('MASCULINO', 'MASCULINO'),  ('FEMININO','FEMININO'), ('NÃO-ESPECIFICAR','NÃO-ESPECIFICAR'))
    
    genre = models.CharField(choices=GENRE_CHOICES, default = 'NÃO-ESPECIFICAR', verbose_name="Genero")
    view_weight  = models.BooleanField(default=True)
    view_height = models.BooleanField(default=True)
    view_category = models.BooleanField(default=True)
    view_box  = models.BooleanField(default=True)
    view_personal_record = models.BooleanField(default=True)

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    photo = models.ImageField(upload_to='media_profile', null=True, blank=True,verbose_name="Foto Perfil")
    created_at_profile =  models.DateField(auto_now=True, verbose_name="Data Adessão")
    birthday = models.DateField(max_length=50, default=timezone.now, verbose_name="Aniversário")
    weight = models.DecimalField(max_digits= 5, decimal_places = 2, validators=[MaxValueValidator (300), MinValueValidator(0)], default=0, verbose_name="Peso")
    height = models.DecimalField(max_digits= 5, decimal_places = 2,  default=0, verbose_name="Altura")
    category = models.CharField(choices= CATEGORY_CHOICES, default= 'EXPERIMENTAL', verbose_name="Categoria")
    box = models.ForeignKey(Box, default = 'DEFAULT', on_delete=models.CASCADE, blank=True, null= True)
    is_coach = models.BooleanField(default=False, verbose_name= "Coach ? ")
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    


class ProfilePersonalRecord(models.Model):
    
    athlete =  models.ForeignKey(User, on_delete=models.CASCADE)
    moviment = models.ForeignKey('WOD.Movement', default='NONE', on_delete=models.CASCADE)
    created_at  =models.DateField(auto_now=True)
    date = models.DateField(max_length=50, default=timezone.now)
    personal_record = models.DecimalField (max_digits=5, decimal_places=1, validators=[MaxValueValidator(500),  MinValueValidator(5)], default=0)
    
    
    

    def  __str__(self):
        return f'Personal Record de {self.athlete} - movimento -{self.moviment} -   {self.personal_record} kg'
    

class Times(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Criador do Time', related_name= 'times_criados')
    name = models.CharField(max_length=50, verbose_name= 'Time_name', blank=False,  null= False, )
    description = models.CharField(max_length=500, verbose_name="Descrição")
    box = models.ForeignKey(Box, on_delete=models.CASCADE, default = 'DEFAULT')
    category = models.CharField(choices= Profile.CATEGORY_CHOICES, default= 'EXPERIMENTAL', verbose_name="Categoria do Time")
    membros = models.ManyToManyField(User, related_name='times_membros', verbose_name='Membros')

    ['creator','name','description', 'box','category', 'membros' ]
 
    



    def __str__(self):
        return f'Nome {self.name} - Criador {self.creator} '
    

    def adicionar_membro(self, usuario):
        if usuario not in self.membros.all():
            self.membros.add(usuario)

    def remover_membro(self, usuario):
        if usuario in self.membros.all():
            self.membros.remove(usuario)


class Time_Achievements(models.Model):
    time = models.ForeignKey(Times, on_delete=models.CASCADE, verbose_name='Time_Conquista')
    achievement = models.CharField(max_length=200, verbose_name='Conquista')
    placement= models.IntegerField(default=0, verbose_name="Colocação em Competições", validators=[MinValueValidator(0)])


    def __str__(self):
        return f'Conquista: {self.achievement} do Time: {self.time.name}'