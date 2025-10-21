from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Sector, Lang, Topic, Question, Answer, UserProgress

def index(request):
    sectors = Sector.objects.filter(is_active=True).order_by('order', 'name')
    print("Sectors:", list(sectors))  # Отладочный вывод
    return render(request, 'bazaznaniy/index.html', {'sectors': sectors})

def sector_detail(request, slug):
    sector = get_object_or_404(Sector, slug=slug)
    return render(request, 'bazaznaniy/sector_detail.html', {'sector': sector})

def lang_detail(request, sector_slug, lang_number):
    lang = get_object_or_404(Lang, sector__slug=sector_slug, number=lang_number)
    return render(request, 'bazaznaniy/lang_detail.html', {'lang': lang})

def topic_detail(request, sector_slug, lang_number, topic_slug):
    topic = get_object_or_404(Topic, lang__sector__slug=sector_slug, lang__number=lang_number, slug=topic_slug)
    return render(request, 'bazaznaniy/topic_detail.html', {'topic': topic})

@login_required
def topic_test(request, sector_slug, lang_number, topic_slug):
    topic = get_object_or_404(Topic, lang__sector__slug=sector_slug, lang__number=lang_number, slug=topic_slug)
    questions = topic.questions.filter(is_active=True).order_by('order')

    if request.method == 'POST':
        score = 0
        total_points = 0
        for question in questions:
            total_points += question.points
            if question.question_type == 'single':
                selected_answer_id = request.POST.get(f'question_{question.id}')
                if selected_answer_id:
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    if selected_answer.is_correct:
                        score += question.points
            elif question.question_type == 'multiple':
                selected_answer_ids = request.POST.getlist(f'question_{question.id}')
                correct_answers = question.answers.filter(is_correct=True).count()
                correct_selected = sum(1 for ans_id in selected_answer_ids if Answer.objects.get(id=ans_id).is_correct)
                incorrect_selected = len(selected_answer_ids) - correct_selected
                if correct_selected == correct_answers and incorrect_selected == 0:
                    score += question.points
            else:  # text
                user_answer = request.POST.get(f'question_{question.id}', '').strip()
                correct_answer = question.correct_answer_text.strip()
                if user_answer.lower() == correct_answer.lower():
                    score += question.points

        # Сохраняем прогресс пользователя
        UserProgress.objects.update_or_create(
            user=request.user,
            topic=topic,
            defaults={'score': score, 'total_points': total_points}
        )
        return render(request, 'bazaznaniy/test_result.html', {
            'topic': topic,
            'score': score,
            'total_points': total_points,
            'percentage': (score / total_points * 100) if total_points > 0 else 0
        })

    return render(request, 'bazaznaniy/topic_test.html', {'topic': topic, 'questions': questions})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Перенаправление на профиль после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'bazaznaniy/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('profile')  # Перенаправление на профиль после выхода

def profile(request):
    if request.method == 'POST':
        # Обработка формы входа
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        login_form = AuthenticationForm()

    # Форма регистрации для неавторизованных пользователей
    register_form = UserCreationForm()

    # Получаем прогресс пользователя, если он авторизован
    progress = UserProgress.objects.filter(user=request.user) if request.user.is_authenticated else None

    return render(request, 'bazaznaniy/profile.html', {
        'login_form': login_form,
        'register_form': register_form,
        'progress': progress,
    })