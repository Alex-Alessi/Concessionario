const usernameInput = document.getElementById('id_username');
const passwordInput = document.getElementById('id_password');
const leftPupil = document.getElementById('leftPupil');
const rightPupil = document.getElementById('rightPupil');
const leftWiper = document.getElementById('leftWiper');
const rightWiper = document.getElementById('rightWiper');
const leftHeadlight = document.getElementById('leftHeadlight');
const rightHeadlight = document.getElementById('rightHeadlight');
const loginForm = document.getElementById('loginForm');

    // Funzione per muovere le pupille verso un punto
function movePupils(x, y, containerRect) {
    const pupils = [leftPupil, rightPupil];
    const headlights = [leftHeadlight, rightHeadlight];

    pupils.forEach((pupil, index) => {
        const headlight = headlights[index];
        const headlightRect = headlight.getBoundingClientRect();
                  
        // Calcola il centro del faro
        const centerX = headlightRect.left + headlightRect.width / 2;
        const centerY = headlightRect.top + headlightRect.height / 2;

        // Calcola l'angolo verso il punto target
        const angle = Math.atan2(y - centerY, x - centerX);
                  
        // Distanza massima che la pupilla può muoversi (12px dal centro)
        const maxDistance = 12;
                  
        // Calcola le nuove coordinate della pupilla
        const offsetX = Math.cos(angle) * maxDistance;
        const offsetY = Math.sin(angle) * maxDistance;

        pupil.style.transform = `translate(calc(-50% + ${offsetX}px), calc(-50% + ${offsetY}px))`;
    });
}

function resetPupils() {
    leftPupil.style.transform = 'translate(-50%, -50%)';
    rightPupil.style.transform = 'translate(-50%, -50%)';
}

function closeEyes() {
    leftHeadlight.classList.add('closed');
    rightHeadlight.classList.add('closed');
}

function openEyes() {
    leftHeadlight.classList.remove('closed');
    rightHeadlight.classList.remove('closed');
}

// Evento per il campo username, segue il cursore
usernameInput.addEventListener('input', function(e) {
    leftWiper.classList.remove('active');
    rightWiper.classList.remove('active');
    openEyes();
});

usernameInput.addEventListener('focus', function(e) {
    leftWiper.classList.remove('active');
    rightWiper.classList.remove('active');
    openEyes();
});

// Tracking del mouse nel campo username
usernameInput.addEventListener('mousemove', function(e) {
    const rect = this.getBoundingClientRect();
    movePupils(e.clientX, e.clientY, rect);
});

// Tracking del cursore di testo nel campo username
usernameInput.addEventListener('keyup', function(e) {
    const rect = this.getBoundingClientRect();
    const textWidth = this.value.length * 8;
    const cursorX = rect.left + 15 + textWidth;
    const cursorY = rect.top + rect.height / 2;
    movePupils(cursorX, cursorY, rect);
});

usernameInput.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    movePupils(e.clientX, e.clientY, rect);
});

passwordInput.addEventListener('focus', function() {
    closeEyes();
    leftWiper.classList.add('active');
    rightWiper.classList.add('active');
    resetPupils();
});

passwordInput.addEventListener('blur', function() {
    openEyes();
    if (!usernameInput.matches(':focus')) {
        leftWiper.classList.remove('active');
        rightWiper.classList.remove('active');
    }
});

usernameInput.addEventListener('blur', function() {
    if (!passwordInput.matches(':focus')) {
        setTimeout(() => {
            leftWiper.classList.remove('active');
            rightWiper.classList.remove('active');
            resetPupils();
        }, 100);
    }
});


loginForm.addEventListener('submit', function() {
    openEyes();
    leftWiper.classList.remove('active');
    rightWiper.classList.remove('active');

    resetPupils();
});


document.addEventListener('click', function(e) {
    if (!usernameInput.contains(e.target) && !passwordInput.contains(e.target)) {
        resetPupils();
        openEyes();
        if (!passwordInput.matches(':focus')) {
            leftWiper.classList.remove('active');
            rightWiper.classList.remove('active');
        }
    }
});


