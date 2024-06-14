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
        })

        const data = Object.fromEntries(formData)
        console.log(JSON.stringify(data))
        console.log(searchUrl)
        
        makeRequest(searchUrl, 'post', data).then(response => console.log(response))
    })
}

handleFilter()

/*======================== SITTER LIST ========================*/
function refreshSitterList() {
    const sitterList = document.querySelector('.sitter__list')
    // Create elements
    let li = document.createElement('li')
    li.className = 'sitter__item'

    let a = document.createElement('a')
    a.href = '#';
    a.className = 'sitter__image-container'

    let img = document.createElement('img')
    img.src = `${staticUrl}images/home/sitter-1.png`
    img.className = 'sitter__image'
    img.alt = 'sitter photo'

    let spanTag1 = document.createElement('span')
    spanTag1.className = 'sitter__tag'
    let iWalk = document.createElement('i')
    iWalk.className = 'ri-walk-line'
    spanTag1.appendChild(iWalk)
    spanTag1.appendChild(document.createTextNode('Выгульщик'))

    let spanTag2 = document.createElement('span')
    spanTag2.className = 'sitter__tag'
    let imgIcon = document.createElement('img')
    imgIcon.className = 'sitter__tag-icon'
    imgIcon.src = `${staticUrl}images/icons/dog-icon.svg`
    imgIcon.alt = 'icon'
    spanTag2.appendChild(imgIcon)
    spanTag2.appendChild(document.createTextNode('Догситтер'))

    a.appendChild(img)
    a.appendChild(spanTag1)
    a.appendChild(spanTag2)

    let divData = document.createElement('div')
    divData.className = 'sitter__data'

    let divColumn1 = document.createElement('div')
    divColumn1.className = 'sitter__column'

    let divInfo = document.createElement('div')
    divInfo.className = 'sitter__info'
    let spanName = document.createElement('span')
    spanName.className = 'sitter__name'
    spanName.textContent = 'Иван'
    let spanAge = document.createElement('span')
    spanAge.className = 'sitter__age'
    spanAge.textContent = '28 лет'
    let divJobs = document.createElement('div')
    divJobs.className = 'sitter__jobs'
    divJobs.innerHTML = '<span>3 заказов</span> | <span>2 отзывов</span>'

    divInfo.appendChild(spanName)
    divInfo.appendChild(spanAge)
    divInfo.appendChild(divJobs)

    let divRating = document.createElement('div')
    divRating.className = 'sitter__rating'
    for (let i = 0; i < 5; i++) {
        let iStar = document.createElement('i')
        iStar.className = 'ri-star-fill'
        divRating.appendChild(iStar)
    }
    let divRatingNumber = document.createElement('div');
    divRatingNumber.className = 'sitter__rating-number'
    divRatingNumber.textContent = '5.0'

    divRating.appendChild(divRatingNumber)

    divColumn1.appendChild(divInfo)
    divColumn1.appendChild(divRating)

    let divQuote = document.createElement('div')
    divQuote.className = 'sitter__quote'
    let pQuote = document.createElement('p')
    pQuote.textContent = 'С удовольствием погуляю с вашим питомцем! Вымою лапы и покормлю после прогулки.'
    divQuote.appendChild(pQuote);

    let divAddress = document.createElement('div')
    divAddress.className = 'sitter__address'
    let iHome = document.createElement('i')
    iHome.className = 'ri-home-2-line'
    let spanAddress = document.createElement('span')
    spanAddress.textContent = 'г.п. Дубровка, Ленинградская область'

    divAddress.appendChild(iHome)
    divAddress.appendChild(spanAddress)

    let divColumn2 = document.createElement('div')
    divColumn2.className = 'sitter__column'

    let divPrice = document.createElement('div')
    divPrice.className = 'sitter__price'
    divPrice.textContent = '800 ₽'

    let aLink = document.createElement('a')
    aLink.className = 'sitter__link'
    let iArrow = document.createElement('i')
    iArrow.className = 'ri-arrow-right-line'
    aLink.appendChild(iArrow)

    divColumn2.appendChild(divPrice)
    divColumn2.appendChild(aLink)

    divData.appendChild(divColumn1)
    divData.appendChild(divQuote)
    divData.appendChild(divAddress)
    divData.appendChild(divColumn2)

    li.appendChild(a)
    li.appendChild(divData)

    // Append the created 'li' element to the desired parent element
    sitterList.appendChild(li)
}

refreshSitterList()