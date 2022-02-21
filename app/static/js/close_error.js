const errors = document.querySelectorAll('.flash')


errors.forEach((error) => {
    error.addEventListener('click', () => {
        console.log('he')
        error.remove()
    })
})