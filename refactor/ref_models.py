from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Sector(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True, max_length=200)
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
        return reverse('place_detail', kwargs={'slug': self.slug})

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
        return reverse('course_detail', kwargs={
            'place_slug': self.sector.slug, 
            'course_number': self.number
        })

class Topic(models.Model):
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE, 
                              related_name='topics', verbose_name='Язык Программирования')
    name = models.CharField('Название темы', max_length=200)
    slug = models.SlugField('URL', max_length=200)
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
        return reverse('subject_detail', kwargs={
            'place_slug': self.lang.sector.slug,
            'course_number': self.lang.number,
            'subject_slug': self.slug
        })
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class TheTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, 
                               related_name='thetopics', verbose_name='Тема')
    title = models.CharField('Название подтемы', max_length=300)
    slug = models.SlugField('URL', max_length=200, blank=True)
    content = models.TextField('Содержание подтемы')
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Подтема'
        verbose_name_plural = 'Подтемы'
        ordering = ['topic', 'order', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.topic.name}"
    
    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)