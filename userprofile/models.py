from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField("E-mail", max_length=255, blank=True)
    first_name = models.CharField("Имя", max_length=100, blank=True)
    last_name = models.CharField("Фамилия", max_length=100, blank=True)
    phone_number = models.CharField("Телефон", max_length=20, blank=True)
    address = models.TextField("Адрес", blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

    def sync_to_user(self):
        """Копируем данные из профиля в User"""
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.email = self.email
        self.user.save()

    def sync_from_user(self):
        """Копируем данные из User в профиль"""
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        self.email = self.user.email

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.sync_from_user()
        profile.save()
    else:
        instance.profile.sync_from_user()
        instance.profile.save()