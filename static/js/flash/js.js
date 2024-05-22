let error_icon = document.querySelector('.error_icon'), sign_error = document.querySelector('.flash');


error_icon.addEventListener('click', () => {
    removeFlash()
})

function removeFlash() {
    error_icon.className = 'fa-solid fa-chevron-right error_icon'
    if (sign_error.classList.contains('error')) {
        sign_error.classList.remove('error')
    } else {
        sign_error.classList.remove('success')
    }
}

setInterval(removeFlash, 2000)