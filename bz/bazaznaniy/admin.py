from django.contrib import admin
from .models import Sector, Language, Topic, Question, Answer, UserProgress, Tip

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1
    fields = ('name', 'slug', 'order', 'is_active')
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

class TipInline(admin.TabularInline):
    model = Tip
    extra = 1
    fields = ('title', 'content', 'order', 'is_active')
    show_change_link = True

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LanguageInline]
    ordering = ('order', 'name')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'slug', 'is_active', 'order', 'created_at')
    list_filter = ('sector', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TopicInline]
    list_editable = ('is_active', 'order')
    ordering = ('sector', 'order', 'name')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'lang', 'icon', 'is_active', 'order', 'created_at')
    list_filter = ('lang', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [QuestionInline, TipInline]
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

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'is_active', 'order', 'created_at')
    list_filter = ('topic', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('is_active', 'order')
    ordering = ('topic', 'order', 'title')
    list_select_related = ('topic',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_completed', 'score', 'max_score', 'percentage', 'attempts', 'last_attempt_at')
    list_filter = ('is_completed', 'topic', 'user')
    search_fields = ('user__username', 'topic__name')
    ordering = ('-last_attempt_at',)