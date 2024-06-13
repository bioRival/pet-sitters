/*======================== SITTER IMAGE HOVER ========================*/
// When hovering on the sitter image, 
// the arrow button moves to the right a bit.
// Impossible to achieve with CSS, 
// since image is not a parent of an arrow button
function initSitterHover() {
    const images = document.querySelectorAll('.sitter__image-container')

    images.forEach(image => {
        const link = image.parentElement.querySelector('.sitter__link')

        image.addEventListener('mouseover', () => {
            link.style.transform = 'translateX(.5rem)'
        })

        image.addEventListener('mouseout', () => {
            link.removeAttribute('style')
        })
    })
}

initSitterHover()


/*======================== HANDLE EMPTY LIST ========================*/
function handleEmptyList() {
    const sitterList = document.querySelector('.sitter__list')
    const paginator = document.querySelector('.sitter__pagination')
    const emptyMessage = document.querySelector('.sitter__empty')

    // if there is no items in the list
    if (!sitterList.querySelector('.sitter__item')) {
        paginator.style.display = 'none'
        emptyMessage.removeAttribute('style')
    } else {
        paginator.removeAttribute('style')
        emptyMessage.style.display = 'none'
    }
}

handleEmptyList()



/*======================== REQUEST ========================*/
async function makeRequest(url, method, body) {
    const headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    if (body) body = JSON.stringify(body)

    if (method === 'post') {
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
    }


    let response = await fetch(url, {
        method: method,
        headers: headers,
        body: body,
    })

    return await response.json()
}


/*======================== SUBMIT ========================*/
function handleFilter() {
    const form = document.querySelector('.filter__form')

    form.addEventListener('submit', (e) => {
        e.preventDefault()

        const formData = new FormData(e.target)
        formData.forEach((value, key) => {
            console.log(key + ': ' + value);
        });

        const data = Object.fromEntries(formData)
        console.log(JSON.stringify(data))
        console.log(djangoUrl)
        
        makeRequest(djangoUrl, 'post', data)
    })
}

handleFilter()