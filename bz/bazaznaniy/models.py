from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Place(models.Model):
    """модель площадки (кампуса) колледжа"""
    name = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=300)
    slug = models.SlugField('URL', unique=True, max_length=200)
    color = models.CharField('Цвет темы', max_length=7, default='#008cff', 
                            help_text='Hex код цвета (например, #008cff)')
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})


class Course(models.Model):
    """модель курса обучения (1-4 курс)"""
    place = models.ForeignKey(Place, on_delete=models.CASCADE, 
                             related_name='courses', verbose_name='Площадка')
    number = models.IntegerField('Номер курса', 
                                choices=[(1, '1 курс'), (2, '2 курс'), 
                                        (3, '3 курс'), (4, '4 курс')])
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['place', 'number']
        unique_together = ['place', 'number']
    
    def __str__(self):
        return f"{self.number} курс - {self.place.name}"
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={
            'place_slug': self.place.slug, 
            'course_number': self.number
        })


class Subject(models.Model):
    """модель предмета (дисциплины)"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, 
                              related_name='subjects', verbose_name='Курс')
    name = models.CharField('Название предмета', max_length=200)
    slug = models.SlugField('URL', max_length=200)
    description = models.TextField('Описание', blank=True)
    icon = models.CharField('Иконка', max_length=50, blank=True,
                          help_text='Название иконки или emoji')
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['course', 'order', 'name']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.name} ({self.course})"
    
    def get_absolute_url(self):
        return reverse('subject_detail', kwargs={
            'place_slug': self.course.place.slug,
            'course_number': self.course.number,
            'subject_slug': self.slug
        })
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Topic(models.Model):
    """модель темы урока"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, 
                               related_name='topics', verbose_name='Предмет')
    title = models.CharField('Название темы', max_length=300)
    slug = models.SlugField('URL', max_length=200, blank=True)
    content = models.TextField('Содержание темы')
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['subject', 'order', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Question(models.Model):
    """модель вопроса теста"""
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
    """модель варианта ответа на вопрос"""
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
    """модель прогресса пользователя"""
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
        return f"{self.user.username} - {self.topic.title}"
    
    @property
    def percentage(self):
        """процент выполнения"""
        if self.max_score > 0:
            return round((self.score / self.max_score) * 100, 1)
        return 0