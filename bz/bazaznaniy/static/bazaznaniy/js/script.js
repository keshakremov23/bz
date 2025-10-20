function animateProgress(circle, targetProgress) {
    const progressValue = circle.querySelector('.progress-value');
    let currentProgress = 0;
    const duration = 1500; // 1.5 секунды
    const increment = targetProgress / (duration / 16); // 60 FPS
    
    const animation = setInterval(() => {
        currentProgress += increment;
        
        if (currentProgress >= targetProgress) {
            currentProgress = targetProgress;
            clearInterval(animation);
        }
        
        // Обновляем значение
        progressValue.textContent = Math.round(currentProgress) + '%';
        
        // Обновляем фон
        const degrees = (currentProgress / 100) * 360;
        circle.style.background = `conic-gradient(#2563EB ${degrees}deg, #e0e0e0 ${degrees}deg)`;
    }, 16);
}

// Использование
const progressCircle = document.querySelector('.circular-progress');
const targetProgress = parseInt(progressCircle.getAttribute('data-progress'));

// Запуск анимации при загрузке страницы
window.addEventListener('load', () => {
    animateProgress(progressCircle, targetProgress);
});