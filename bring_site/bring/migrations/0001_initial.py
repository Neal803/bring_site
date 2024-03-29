# Generated by Django 4.0.4 on 2022-09-08 11:37

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150, verbose_name='username')),
                ('communication', models.CharField(blank=True, max_length=256, verbose_name='Способ связи')),
                ('first_name', models.CharField(max_length=150, verbose_name='First Name')),
                ('email_verify', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='banners/')),
            ],
            options={
                'verbose_name': 'банер',
                'verbose_name_plural': 'банери',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активировано?')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='URL')),
                ('priority', models.IntegerField(blank=True, default=5, null=True, verbose_name='Приоритет выдачи')),
            ],
            options={
                'verbose_name': 'категорія',
                'verbose_name_plural': 'категорії',
            },
        ),
        migrations.CreateModel(
            name='Stuff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('picture', models.ImageField(blank=True, default='pictures/default.png', null=True, upload_to='pictures/')),
                ('slug', models.SlugField(max_length=256, unique=True, verbose_name='URL')),
                ('priority', models.IntegerField(blank=True, default=5, null=True, verbose_name='Приоритет выдачи')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активировано?')),
                ('is_action', models.BooleanField(default=False, verbose_name='Акційна пропозиція')),
                ('price_per_ton', models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена за тонну')),
                ('price_per_bag', models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена за мешок')),
                ('price_per_piece', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Цена за штуку')),
                ('price_per_hour', models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена за час')),
                ('price_per_day', models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена за сутки')),
                ('for_search_my', models.TextField(blank=True, default=' ', null=True, verbose_name='Слова для поиска')),
                ('for_search', models.TextField(default='Автоматичне поле', verbose_name='Для поиска(авто)')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stuffs', to='bring.category', verbose_name='Категорії')),
                ('fans', models.ManyToManyField(blank=True, related_name='favs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'позиція',
                'verbose_name_plural': 'позиції',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=256, verbose_name='Комментарий')),
                ('rating_vote', models.FloatField(blank=True, null=True, verbose_name='Оценка')),
                ('pub_comment_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации комментария')),
                ('is_new', models.BooleanField(default=True, verbose_name='Новое')),
                ('answer_by_admin', models.CharField(blank=True, max_length=256, null=True, verbose_name='Ответ Администратора')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('stuff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='bring.stuff')),
            ],
            options={
                'verbose_name': 'відгук',
                'verbose_name_plural': 'відгуки',
            },
        ),
    ]
