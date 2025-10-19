from django.contrib import admin
from .models import Place, Course, Subject, Topic, Question, Answer, UserProgress

# Вспомогательные классы для отображения связанных данных
class CourseInline(admin.TabularInline):
    model = Course
    extra = 1  # Количество пустых форм для добавления новых курсов
    fields = ('number', 'description', 'is_active')  # Поля для редактирования
    show_change_link = True  # Ссылка на редактирование курса

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1  # Количество пустых форм для добавления новых тем
    fields = ('title', 'slug', 'order', 'is_active')  # Поля для редактирования
    show_change_link = True  # Ссылка на редактирование темы

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1
    fields = ('name', 'slug', 'order', 'is_active')
    show_change_link = True

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'points', 'is_active')
    show_change_link = True

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # Количество пустых форм для вариантов ответа
    fields = ('text', 'is_correct', 'order')

# Кастомизация для Place
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'color', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)  # Фильтр по активности
    search_fields = ('name', 'address')  # Поиск по названию и адресу
    list_editable = ('is_active', 'order')  # Редактирование прямо в списке
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug на основе name
    inlines = [CourseInline]  # Показ курсов, связанных с площадкой
    ordering = ('order', 'name')

# Кастомизация для Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('number', 'place', 'description_short', 'is_active')
    list_filter = ('place', 'number', 'is_active')  # Фильтры по площадке, номеру и активности
    search_fields = ('description',)  # Поиск по описанию
    inlines = [SubjectInline]  # Показ предметов, связанных с курсом
    ordering = ('place', 'number')

    def description_short(self, obj):
        """Короткое описание для списка (первые 50 символов)"""
        return obj.description[:50] + '...' if obj.description else ''
    description_short.short_description = 'Описание'

# Кастомизация для Subject
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'icon', 'is_active', 'order', 'created_at')
    list_filter = ('course', 'is_active')  # Фильтры по курсу и активности
    search_fields = ('name', 'description')  # Поиск по названию и описанию
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug
    inlines = [TopicInline]  # Показ тем, связанных с предметом
    list_editable = ('is_active', 'order')
    ordering = ('course', 'order', 'name')

# Кастомизация для Topic
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('subject', 'is_active')  # Фильтры по предмету и активности
    search_fields = ('title', 'content')  # Поиск по названию и содержанию
    prepopulated_fields = {'slug': ('title',)}  # Автозаполнение slug
    inlines = [QuestionInline]  # Показ вопросов, связанных с темой
    list_editable = ('is_active', 'order')
    ordering = ('subject', 'order', 'title')

# Кастомизация для Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'topic', 'question_type', 'points', 'is_active', 'order')
    list_filter = ('topic', 'question_type', 'is_active')  # Фильтры по теме, типу вопроса и активности
    search_fields = ('text',)  # Поиск по тексту вопроса
    inlines = [AnswerInline]  # Показ ответов, связанных с вопросом
    list_editable = ('points', 'is_active', 'order')
    ordering = ('topic', 'order')

    def text_short(self, obj):
        """Короткий текст вопроса для списка"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст вопроса'

# Кастомизация для Answer
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'question', 'is_correct', 'order')
    list_filter = ('question', 'is_correct')  # Фильтры по вопросу и правильности
    search_fields = ('text',)  # Поиск по тексту ответа
    list_editable = ('is_correct', 'order')
    ordering = ('question', 'order')

    def text_short(self, obj):
        """Короткий текст ответа для списка"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст ответа'

# Кастомизация для UserProgress
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_completed', 'score', 'max_score', 'percentage', 'attempts', 'last_attempt_at')
    list_filter = ('is_completed', 'topic', 'user')  # Фильтры по завершению, теме и пользователю
    search_fields = ('user__username', 'topic__title')  # Поиск по имени пользователя и названию темы
    ordering = ('-last_attempt_at',)