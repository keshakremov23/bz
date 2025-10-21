from django.contrib import admin
from .models import Sector, Lang, Topic, Question, Answer, UserProgress

class LangInline(admin.TabularInline):
    model = Lang
    extra = 1
    fields = ('number', 'description', 'is_active')
    show_change_link = True

class TopicInline(admin.TabularInline):
    model = Topic
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
    extra = 2
    fields = ('text', 'is_correct', 'order')

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LangInline]
    ordering = ('order', 'name')

@admin.register(Lang)
class LangAdmin(admin.ModelAdmin):
    list_display = ('number', 'sector', 'description_short', 'is_active')
    list_filter = ('sector', 'number', 'is_active')
    search_fields = ('description',)
    inlines = [TopicInline]
    ordering = ('sector', 'number')

    def description_short(self, obj):
        return obj.description[:50] + '...' if obj.description else ''
    description_short.short_description = 'Описание'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'lang', 'icon', 'is_active', 'order', 'created_at')
    list_filter = ('lang', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [QuestionInline]
    list_editable = ('is_active', 'order')
    ordering = ('lang', 'order', 'name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'topic', 'question_type', 'points', 'is_active', 'order')
    list_filter = ('topic', 'question_type', 'is_active')
    search_fields = ('text',)
    inlines = [AnswerInline]
    list_editable = ('points', 'is_active', 'order')
    ordering = ('topic', 'order')

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст вопроса'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'question', 'is_correct', 'order')
    list_filter = ('question', 'is_correct')
    search_fields = ('text',)
    list_editable = ('is_correct', 'order')
    ordering = ('question', 'order')

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст ответа'

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_completed', 'score', 'max_score', 'percentage', 'attempts', 'last_attempt_at')
    list_filter = ('is_completed', 'topic', 'user')
    search_fields = ('user__username', 'topic__name')
    ordering = ('-last_attempt_at',)