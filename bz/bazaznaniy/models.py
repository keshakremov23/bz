from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Sector(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True, max_length=200, blank=True)
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отрасль'
        verbose_name_plural = 'Отрасли'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sector_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Lang(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, 
                             related_name='langs', verbose_name='Отрасль')
    number = models.IntegerField('Уровень', 
                                choices=[(1, '1 уровень'), (2, '2 уровень'), 
                                        (3, '3 уровень'), (4, '4 уровень')])
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Язык Программирования'
        verbose_name_plural = 'Языки Программирования'
        ordering = ['sector', 'number']
        unique_together = ['sector', 'number']
    
    def __str__(self):
        return f"{self.number} уровень - {self.sector.name}"
    
    def get_absolute_url(self):
        return reverse('lang_detail', kwargs={
            'sector_slug': self.sector.slug, 
            'lang_number': self.number
        })

class Topic(models.Model):
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE, 
                             related_name='topics', verbose_name='Язык Программирования')
    name = models.CharField('Название темы', max_length=200)
    slug = models.SlugField('URL', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    icon = models.CharField('Иконка', max_length=50, blank=True,
                            help_text='Название иконки или emoji')
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['lang', 'order', 'name']
        unique_together = ['lang', 'slug']
    
    def __str__(self):
        return f"{self.name} ({self.lang})"
    
    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={
            'sector_slug': self.lang.sector.slug,
            'lang_number': self.lang.number,
            'topic_slug': self.slug
        })
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Question(models.Model):
    QUESTION_TYPES = [
        ('single', 'Один правильный ответ'),
        ('multiple', 'Несколько правильных ответов'),
        ('text', 'Текстовый ответ'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, 
                             related_name='questions', verbose_name='Тема')
    text = models.TextField('Текст вопроса')
    question_type = models.CharField('Тип вопроса', max_length=20, 
                                    choices=QUESTION_TYPES, default='single')
    order = models.IntegerField('Порядок', default=0)
    points = models.IntegerField('Баллы', default=1)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['topic', 'order']
    
    def __str__(self):
        return f"Вопрос {self.order}: {self.text[:50]}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, 
                                related_name='answers', verbose_name='Вопрос')
    text = models.CharField('Текст ответа', max_length=500)
    is_correct = models.BooleanField('Правильный ответ', default=False)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                            related_name='progress', verbose_name='Пользователь')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, 
                             related_name='user_progress', verbose_name='Тема')
    is_completed = models.BooleanField('Завершена', default=False)
    score = models.IntegerField('Набрано баллов', default=0)
    max_score = models.IntegerField('Максимум баллов', default=0)
    attempts = models.IntegerField('Количество попыток', default=0)
    completed_at = models.DateTimeField('Дата завершения', null=True, blank=True)
    last_attempt_at = models.DateTimeField('Последняя попытка', auto_now=True)
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = ['user', 'topic']
        ordering = ['-last_attempt_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name}"
    
    @property
    def percentage(self):
        if self.max_score > 0:
            return round((self.score / self.max_score) * 100, 1)
        return 0