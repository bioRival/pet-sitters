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
        refreshSitters()
    })
}

handleFilter()


/*======================== REFRESH SITTERS ========================*/
function refreshSitters() {
    const form = document.querySelector('.filter__form')
    const formData = new FormData(form)
    formData.forEach((value, key) => {
        console.log(key + ': ' + value);
    })

    const data = Object.fromEntries(formData)
    console.log(JSON.stringify(data))
    console.log(searchUrl)

    makeRequest(searchUrl, 'post', data)
    .then(response => renderSitterList(response))
}

/*======================== CLEAN SITTER LIST ========================*/
function cleanSitterList() {
    document.querySelectorAll('.sitter__item').forEach(
        item=>item.remove()
    )
}

/*======================== RENDER SITTER LIST ========================*/
function renderSitterList(sitters) {
    // Maximum amount of letters in quote section
    const maxQuote = 100

    const sitterList = document.querySelector('.sitter__list')

    
    // Delete old items
    cleanSitterList()
    
    // Create new items
    sitters.map(sitter => {
        // Create item
        let li = document.createElement('li')
        li.className = 'sitter__item'

        let a = document.createElement('a')
        a.href = '#';
        a.className = 'sitter__image-container'

        // Avatar image
        let img = document.createElement('img')
        sitter?.imageUrl 
            ? img.src = sitter.imageUrl
            : img.src = `${staticUrl}images/global/default-avatar.png`
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

        // Name | Age | Amount of orders | Amount of reviews
        let divInfo = document.createElement('div')
        divInfo.className = 'sitter__info'
        // Name
        let spanName = document.createElement('span')
        spanName.className = 'sitter__name'
        sitter?.name
            ? spanName.textContent = sitter.name
            : spanName.textContent = 'Аноним'
        let spanAge = document.createElement('span')
        // Age
        spanAge.className = 'sitter__age'
        if (sitter?.age)
            spanAge.textContent = sitter?.age + ' лет'
        let divJobs = document.createElement('div')
        divJobs.className = 'sitter__jobs'
        // Amount of orders
        let spanOrders = document.createElement('span')
        spanOrders.className = 'sitter__orders'
        sitter?.orders || sitter?.orders === 0
            ? spanOrders.textContent = sitter?.orders + ' заказов'
            : spanOrders = null
        // Amount of reviews
        let spanReviews = document.createElement('span')
        spanReviews.className = 'sitter__reviews'
        sitter?.reviews || sitter?.reviews === 0
            ? spanReviews.textContent = sitter.reviews + ' заказов'
            : spanReviews = null
        spanOrders ? divJobs.appendChild(spanOrders) : null
        // Seperator
        if (spanOrders && spanReviews) {
            let spanSeperator = document.createElement('span')
            spanSeperator.className = 'sitter__seperator'
            spanSeperator.textContent = ' | '
            divJobs.appendChild(spanSeperator)
        }
        spanReviews ? divJobs.appendChild(spanReviews) : null

        divInfo.appendChild(spanName)
        divInfo.appendChild(spanAge)
        divInfo.appendChild(divJobs)

        // Rating
        let divRating = document.createElement('div')
        divRating.className = 'sitter__rating'
        let divRatingNumber = document.createElement('div')
        divRatingNumber.className = 'sitter__rating-number'
        if (sitter?.rating) {
            let fullStars = Math.floor(sitter.rating)
            let hollowStars = 5 - Math.floor(sitter.rating)
            let remainder = sitter.rating - Math.floor(sitter.rating)
            // print full stars first
            for (let i = 0; i < fullStars; i++) {
                let iStar = document.createElement('i')
                iStar.className = 'ri-star-fill'
                divRating.appendChild(iStar)
            }
            // if remainder above 0.5 - print half star
            if (remainder >= 0.5) {
                let iStar = document.createElement('i')
                iStar.className = 'ri-star-half-line'
                divRating.appendChild(iStar)
                hollowStars -= 1
            }
            // print hollow stars last
            for (let i = 0; i < hollowStars; i++) {
                let iStar = document.createElement('i')
                iStar.className = 'ri-star-line'
                divRating.appendChild(iStar)
            }
            divRatingNumber.textContent = sitter.rating.toFixed(1)
        } else {
            for (let i = 0; i < 5; i++) {
                let iStar = document.createElement('i')
                iStar.className = 'ri-star-line'
                divRating.appendChild(iStar)
            }
            divRatingNumber.textContent = '0.0'
        }

        divRating.appendChild(divRatingNumber)

        divColumn1.appendChild(divInfo)
        divColumn1.appendChild(divRating)
        
        // Quote
        let divQuote = document.createElement('div')
        divQuote.className = 'sitter__quote'
        let pQuote = document.createElement('p')
        if (sitter?.quote)
            (pQuote.textContent = `“${truncate(sitter.quote, maxQuote)}”`)
        divQuote.appendChild(pQuote);
        
        // Address
        let divAddress = document.createElement('div')
        divAddress.className = 'sitter__address'
        if (sitter?.address) {
            let iHome = document.createElement('i')
            iHome.className = 'ri-building-line'
            let spanAddress = document.createElement('span')
            spanAddress.textContent = sitter.address

            divAddress.appendChild(iHome)
            divAddress.appendChild(spanAddress)
        }


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
    })

    // change display if none sitters are found
    handleEmptyList()

    // refresh hover effects on new sitter items
    initSitterHover()
}

// refreshSitterList()