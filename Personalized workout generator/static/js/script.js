// ===== State =====
let currentWorkoutData = null;

// ===== DOM Elements =====
const workoutForm = document.getElementById('workout-form');
const workoutResults = document.getElementById('workout-results');
const backHomeBtn = document.getElementById('back-home');
const saveWorkoutBtn = document.getElementById('save-workout-btn');
const accountBtn = document.getElementById('account-btn');
const progressBtn = document.getElementById('progress-btn');
const authModal = document.getElementById('auth-modal');
const authClose = document.getElementById('auth-close');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const authError = document.getElementById('auth-error');
const authTabs = document.querySelectorAll('.auth-tab');
const userName = document.getElementById('user-name');
const progressLoginPrompt = document.getElementById('progress-login-prompt');
const progressContent = document.getElementById('progress-content');
const workoutHistory = document.getElementById('workout-history');
const progressLog = document.getElementById('progress-log');
const progressBack = document.getElementById('progress-back');

// ===== Auth =====
async function fetchWithCreds(url, opts = {}) {
    return fetch(url, { ...opts, credentials: 'include' });
}

async function checkAuth() {
    const res = await fetchWithCreds('/api/me');
    const data = await res.json();
    if (data.username) {
        userName.textContent = data.username;
        userName.classList.remove('hidden');
        accountBtn.textContent = 'Logout';
        saveWorkoutBtn?.classList.remove('hidden');
    } else {
        userName.classList.add('hidden');
        accountBtn.textContent = 'Account';
        saveWorkoutBtn?.classList.add('hidden');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    authError.classList.add('hidden');
    const formData = new FormData(loginForm);
    const res = await fetchWithCreds('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: formData.get('username'),
            password: formData.get('password')
        })
    });
    const data = await res.json();
    if (res.ok) {
        authModal.classList.add('hidden');
        checkAuth();
        if (document.getElementById('progress-view')?.classList.contains('active')) loadProgress();
    } else {
        authError.textContent = data.error || 'Login failed';
        authError.classList.remove('hidden');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    authError.classList.add('hidden');
    const formData = new FormData(registerForm);
    const res = await fetchWithCreds('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password')
        })
    });
    const data = await res.json();
    if (res.ok) {
        authModal.classList.add('hidden');
        checkAuth();
    } else {
        authError.textContent = data.error || 'Registration failed';
        authError.classList.remove('hidden');
    }
}

async function handleLogout() {
    await fetchWithCreds('/api/logout', { method: 'POST' });
    checkAuth();
}

async function loadProgress() {
    const res = await fetchWithCreds('/api/me');
    const me = await res.json();
    if (!me.username) {
        progressLoginPrompt.classList.remove('hidden');
        progressContent.classList.add('hidden');
        return;
    }
    progressLoginPrompt.classList.add('hidden');
    progressContent.classList.remove('hidden');

    const workoutsRes = await fetchWithCreds('/api/workouts');
    const workouts = workoutsRes.ok ? await workoutsRes.json() : [];
    workoutHistory.innerHTML = workouts.length
        ? workouts.map(w => `<div class="workout-item">${w.workout_type} — ${new Date(w.created_at).toLocaleDateString()}</div>`).join('')
        : '<p>No saved workouts yet.</p>';

    const progressRes = await fetchWithCreds('/api/progress');
    const logs = progressRes.ok ? await progressRes.json() : [];
    progressLog.innerHTML = logs.length
        ? logs.map(l => `<div class="progress-item">${l.exercise_name}: ${l.sets || '-'}x${l.reps || '-'} — ${new Date(l.logged_at).toLocaleDateString()}</div>`).join('')
        : '<p>No progress logged yet.</p>';
}

// ===== Navigation =====
function showView(viewId) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const id = viewId === 'results' ? 'results-view' : viewId === 'progress' ? 'progress-view' : viewId;
    const view = document.getElementById(id);
    if (view) view.classList.add('active');
    if (viewId === 'progress') loadProgress();
}

// ===== Form to API mapping =====
function getFormData() {
    const equipment = Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(e => e.value);
    const exerciseTypes = Array.from(document.querySelectorAll('input[name="exercise_type"]:checked')).map(e => e.value);
    const reps = document.getElementById('reps-input')?.value || 10;

    return {
        equipment,
        exercise_type: exerciseTypes,
        reps: parseInt(reps, 10) || 10
    };
}

async function fetchWorkout(formData) {
    try {
        const res = await fetchWithCreds('/api/generate-workout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const data = await res.json();
        currentWorkoutData = data;
        renderResults(data);
        showView('results');
    } catch (err) {
        console.error(err);
        currentWorkoutData = getFallbackWorkout(formData);
        renderResults(currentWorkoutData);
        showView('results');
    }
}

function getFallbackWorkout(formData = {}) {
    const types = formData.exercise_type || ['strength'];
    const primary = types.includes('strength') ? 'strength_training' : types.includes('cardio') ? 'cardio' : 'mixed';
    return {
        workout_type: primary,
        exercises: [
            { name: 'Warm-up: Light cardio', sets: '5 min' },
            { name: 'Squats', sets: `3x${formData.reps || 12}`, video_embed_id: 'acLH3-2EPLc' },
            { name: 'Push-ups', sets: `3x${formData.reps || 10}`, video_embed_id: 'IODxDxX7oi4' },
            { name: 'Plank', sets: '3x30 sec', video_embed_id: 'pSHjTRCQxIw' }
        ]
    };
}

async function saveWorkout() {
    if (!currentWorkoutData) return;
    const res = await fetchWithCreds('/api/workouts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            workout_type: currentWorkoutData.workout_type,
            exercises: currentWorkoutData.exercises,
            completed: false
        })
    });
    if (res.ok) {
        saveWorkoutBtn.textContent = 'Saved!';
        saveWorkoutBtn.disabled = true;
    }
}

function renderResults(data) {
    const type = data.workout_type || 'mixed';
    const exercises = data.exercises || getFallbackWorkout().exercises;

    workoutResults.innerHTML = `
        <div class="workout-card">
            <h3>${formatWorkoutType(type)}</h3>
            <div class="exercise-list">
                ${exercises.map(ex => `
                    <div class="exercise-item">
                        <div class="exercise-info">
                            <strong>${ex.name}</strong>
                            <span class="exercise-sets">${ex.sets}</span>
                        </div>
                        ${ex.video_embed_id ? `
                            <div class="exercise-video">
                                <iframe src="https://www.youtube.com/embed/${ex.video_embed_id}?rel=0" title="${ex.name} demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function formatWorkoutType(type) {
    const labels = {
        strength_training: 'Strength Training',
        calisthenics: 'Calisthenics',
        cardio: 'Cardio',
        mixed: 'Mixed Full Body'
    };
    return labels[type] || type;
}

// ===== Event Listeners =====
workoutForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    fetchWorkout(getFormData());
});

backHomeBtn?.addEventListener('click', () => showView('homepage'));

saveWorkoutBtn?.addEventListener('click', saveWorkout);

accountBtn?.addEventListener('click', async () => {
    const res = await fetchWithCreds('/api/me');
    const me = await res.json();
    if (me.username) {
        handleLogout();
    } else {
        authModal.classList.remove('hidden');
        document.querySelector('[data-tab="login"]').click();
    }
});

progressBtn?.addEventListener('click', () => showView('progress'));
progressBack?.addEventListener('click', () => showView('homepage'));

authClose?.addEventListener('click', () => authModal.classList.add('hidden'));

authTabs?.forEach(tab => {
    tab.addEventListener('click', () => {
        authTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        loginForm.classList.toggle('hidden', tab.dataset.tab !== 'login');
        registerForm.classList.toggle('hidden', tab.dataset.tab !== 'register');
        authError.classList.add('hidden');
    });
});

loginForm?.addEventListener('submit', handleLogin);
registerForm?.addEventListener('submit', handleRegister);

document.getElementById('log-progress-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const exercise = document.getElementById('log-exercise').value.trim();
    const sets = parseInt(document.getElementById('log-sets').value, 10) || null;
    const reps = parseInt(document.getElementById('log-reps').value, 10) || null;
    const res = await fetchWithCreds('/api/progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exercise_name: exercise, sets, reps })
    });
    if (res.ok) {
        document.getElementById('log-progress-form').reset();
        loadProgress();
    }
});

// Init
checkAuth();
