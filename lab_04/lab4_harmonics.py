import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# 1. Початкові параметри 
initial_A = 1.0
initial_f = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_cov = 0.1
initial_cutoff = 5.0

# Генерація часу та базового масиву шуму
t = np.linspace(0, 10, 1000)
base_noise = np.random.randn(len(t)) # Генерується один раз!

# 2. Математичні функції 
def harmonic_with_noise(A, f, phase, n_mean, n_cov):
    # Чиста гармоніка: y(t) = A * sin(2 * pi * f * t + phase)
    y_clean = A * np.sin(2 * np.pi * f * t + phase)
    # Шум: базовий шум масштабується на корінь з дисперсії (стандартне відхилення) + середнє
    noise = base_noise * np.sqrt(n_cov) + n_mean
    y_noisy = y_clean + noise
    return y_clean, y_noisy

def apply_filter(data, cutoff, fs=100):
    # Фільтр Баттерворта низьких частот 
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    # Якщо частота зрізу занадто висока або низька, повертаємо оригінал
    if normal_cutoff <= 0 or normal_cutoff >= 1:
        return data
    b, a = butter(3, normal_cutoff, btype='low', analog=False)
    y_filtered = filtfilt(b, a, data)
    return y_filtered

# 3. Налаштування вікна та графіків 
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(left=0.1, bottom=0.45) # Залишаємо місце знизу для повзунків

# Отримуємо початкові дані
y_clean, y_noisy = harmonic_with_noise(initial_A, initial_f, initial_phase, initial_noise_mean, initial_noise_cov)
y_filtered = apply_filter(y_noisy, initial_cutoff)

# Малюємо лінії
line_noisy, = ax.plot(t, y_noisy, label='Зашумлена гармоніка', color='orange', alpha=0.8)
line_clean, = ax.plot(t, y_clean, label='Чиста гармоніка', color='blue', linestyle='--', linewidth=2)
line_filtered, = ax.plot(t, y_filtered, label='Відфільтрована', color='purple', linewidth=2)

ax.legend(loc='upper right')
ax.set_title('Інтерактивна фільтрація гармоніки')
ax.set_xlabel('Час (t)')
ax.set_ylabel('Амплітуда y(t)')
ax.grid(True, linestyle=':', alpha=0.6)

# 4. Інтерфейс (
axcolor = 'lightgoldenrodyellow'
ax_amp = plt.axes([0.15, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_nmean = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_ncov = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_amp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=initial_A)
s_freq = Slider(ax_freq, 'Frequency', 0.1, 5.0, valinit=initial_f)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=initial_phase)
s_nmean = Slider(ax_nmean, 'Noise Mean', -2.0, 2.0, valinit=initial_noise_mean)
s_ncov = Slider(ax_ncov, 'Noise Covariance', 0.0, 1.0, valinit=initial_noise_cov)
s_cutoff = Slider(ax_cutoff, 'Cutoff Freq', 0.1, 20.0, valinit=initial_cutoff)

# Чекбокс для шуму
ax_check = plt.axes([0.85, 0.25, 0.12, 0.1])
check = CheckButtons(ax_check, ['Show Noise'], [True])

# Кнопка Reset
ax_reset = plt.axes([0.85, 0.1, 0.1, 0.05])
btn_reset = Button(ax_reset, 'Reset', hovercolor='0.975')

# 5. Логіка оновлення 
def update(val):
    A = s_amp.val
    f = s_freq.val
    phase = s_phase.val
    n_mean = s_nmean.val
    n_cov = s_ncov.val
    cutoff = s_cutoff.val

    # Перераховуємо дані
    new_y_clean, new_y_noisy = harmonic_with_noise(A, f, phase, n_mean, n_cov)
    new_y_filtered = apply_filter(new_y_noisy, cutoff)

    # Оновлюємо графіки
    line_clean.set_ydata(new_y_clean)
    line_noisy.set_ydata(new_y_noisy)
    line_filtered.set_ydata(new_y_filtered)
    fig.canvas.draw_idle()

# Прив'язуємо функцію оновлення до повзунків
s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_nmean.on_changed(update)
s_ncov.on_changed(update)
s_cutoff.on_changed(update)

def toggle_noise(label):
    line_noisy.set_visible(check.get_status()[0])
    fig.canvas.draw_idle()

check.on_clicked(toggle_noise)

def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_nmean.reset()
    s_ncov.reset()
    s_cutoff.reset()

btn_reset.on_clicked(reset)

# Запуск програми
plt.show()