from django.db import models

from django.urls import reverse
from googletrans import Translator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Stuff(models.Model):
    title = models.CharField('Название', max_length=128)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорії', related_name='stuffs')
    description = models.TextField('Описание')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, blank=True)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True, default='pictures/default.png')
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name='URL')
    priority = models.IntegerField('Приоритет выдачи', null=True, blank=True, default=5)
    is_active = models.BooleanField('Активировано?', default=True)
    is_action = models.BooleanField('Акційна пропозиція', default=False)
    fans = models.ManyToManyField('CustomUser', related_name='favs', blank=True)

    price_per_ton = models.IntegerField('Цена за тонну', null=True, blank=True, default=0)
    price_per_bag = models.IntegerField('Цена за мешок', null=True, blank=True, default=0)
    price_per_piece = models.FloatField('Цена за штуку', null=True, blank=True, default=0.0)
    price_per_hour = models.IntegerField('Цена за час', null=True, blank=True, default=0)
    price_per_day = models.IntegerField('Цена за сутки', null=True, blank=True, default=0)

    for_search_my = models.TextField('Слова для поиска', default=' ', null=True, blank=True,)
    for_search = models.TextField('Для поиска(авто)', default='Автоматичне поле')

    class Meta:
        verbose_name = "позиція"
        verbose_name_plural = "позиції"

    def packing(self):
        if any([self.price_per_ton, self.price_per_bag, self.price_per_piece, self.price_per_hour,
                self.price_per_day]) > 0.0:
            return [{'method_of_packing': 'поштучно', 'short_unit_packing': 'шт.', 'price': self.price_per_piece},
                    {'method_of_packing': 'у мішках', 'short_unit_packing': 'м.', 'price': self.price_per_bag},
                    {'method_of_packing': 'насипом', 'short_unit_packing': 'т.', 'price': self.price_per_ton},
                    {'method_of_packing': 'погодинно', 'short_unit_packing': 'г ', 'price': self.price_per_hour},
                    {'method_of_packing': 'подобово', 'short_unit_packing': 'д ', 'price': self.price_per_day},
                    ]

    def __str__(self):
        return self.title

    def rating(self):
        comments = self.comments.filter(rating_vote__range=(0.50, 5.10))
        if comments:
            return round(sum(comment.rating_vote for comment in comments) / len(comments), 2)
        else:
            return 0.0

    def get_absolute_url(self):
        return reverse('bring:stuff', kwargs={'slug': self.slug})

    def for_search_str(self):
        for_search_ua = f'{self.title}' + f', {self.description}' + f', {self.cat}' + f', {self.for_search_my}'
        try:
            translator = Translator(service_urls=['translate.google.com'])
            for_search_ru = translator.translate(for_search_ua, src='uk', dest='ru')
            for_search_en = translator.translate(for_search_ua, src='uk', dest='en')
            for_search_all = for_search_ua + ' ' + for_search_ru.text + ' ' + for_search_en.text
            return for_search_all.lower()
        except:
            return for_search_ua.lower()

    def save(self, *args, **kwargs):
        self.for_search = self.for_search_str()
        super(Stuff, self).save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField('Название', max_length=64)
    is_active = models.BooleanField('Активировано?', default=True)
    slug = models.SlugField(max_length=64, unique=True, db_index=True, verbose_name='URL')
    priority = models.IntegerField('Приоритет выдачи', null=True, blank=True, default=5)

    class Meta:
        verbose_name = "категорія"
        verbose_name_plural = "категорії"

    def __str__(self):
        return self.title

    def related_stuffs(self):
        return [stuff for stuff in self.stuffs.all()]

    def get_absolute_url(self):
        return reverse('bring:category', kwargs={'cat_slug': self.slug})


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=False)
    communication = models.CharField('Способ связи', max_length=256, blank=True, unique=False)
    first_name = models.CharField(_("First Name"), max_length=150, unique=False)
    email_verify = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def init_communication(self):
        if self.communication == '':
            return 'Не вказано'

    def save(self, *args, **kwargs):
        if self.communication == '' or self.communication is None:
            self.communication = 'Не вказано'
        super(CustomUser, self).save(*args, **kwargs)


class Comment(models.Model):
    stuff = models.ForeignKey(Stuff, on_delete=models.SET_NULL, related_name="comments", null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.CharField('Комментарий', max_length=256)
    rating_vote = models.FloatField('Оценка', null=True, blank=True)
    pub_comment_date = models.DateTimeField('Дата публикации комментария', auto_now_add=True, blank=True)
    is_new = models.BooleanField('Новое', default=True)
    answer_by_admin = models.CharField('Ответ Администратора', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "відгук"
        verbose_name_plural = "відгуки"

    def __str__(self):
        return self.comment_text


class Banner(models.Model):
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)

    class Meta:
        verbose_name = "банер"
        verbose_name_plural = "банери"
