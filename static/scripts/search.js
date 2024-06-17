/*======================== FORM ON CHANGE ========================*/
document.querySelector('.filter__form').addEventListener('change', refreshSitters)


/*======================== FORM ON SUBMIT ========================*/
function handleFilter() {
    const form = document.querySelector('.filter__form')

    form.addEventListener('submit', (e) => {
        e.preventDefault()
        refreshSitters()
    })
}

handleFilter()


