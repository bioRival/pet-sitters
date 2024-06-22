// =========================================================
// DATA variables
// =========================================================
// list of sitters
let PEOPLE = []

// list of ids of sitters visible on the map
let idList = []

// current map states
let CENTER, ZOOM




/*======================== FILL FORM ========================*/
// handle data transfer from home page if home form was used
fillTheForm()
function fillTheForm() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.toString() !== '') {
        // set dog checkbox
        if (urlParams.get('checkbox-dog')) {
            document.getElementById('checkbox-dog').checked = true
        }
        // set cat checkbox
        if (urlParams.get('checkbox-cat')) {
            document.getElementById('checkbox-cat').checked = true
        }
        // set type of service
        const serviceInputs = document.getElementsByName('service')
        if (urlParams.get('type')) {
            for (let input of serviceInputs) {
                if (input.value === urlParams.get('type')) {
                    input.checked = true
                }
            }
        }
        // set start date
        if (urlParams.get('date-start')) {
            document.getElementById('date-start').value = urlParams.get('date-start')
        }
        // set end date
        if (urlParams.get('date-end')) {
            document.getElementById('date-end').value = urlParams.get('date-end')
        }
        //set weight
        const weightInputs = document.getElementsByName('weight')
        if (urlParams.get('weight')) {
            for (let input of weightInputs) {
                if (input.value === urlParams.get('weight')) {
                    input.checked = true
                }
            }
        }
        //set address
        if (urlParams.get('address')) {
            document.getElementById('address-input').value = urlParams.get('address')
        }
        // set map states
        if (urlParams.get('zoom') && urlParams.get('center')) {
            let cords = urlParams.get('center').split(',')
            cords = cords.map(Number)
            
            CENTER = cords
            ZOOM = parseInt(urlParams.get('zoom'))
        }
    }
}








// =========================================================
// YANDEX MAP INITIATION
// =========================================================
ymaps.ready(initMap)
async function initMap(){
    myMap = new ymaps.Map("map", {
        center: CENTER || [55.7605173, 37.6185126], // Moscow coordinates
        zoom: ZOOM || 11,
        controls: [],
    })

    // Add zoom control and geolocation button
    myMap.controls.add('zoomControl', {
        position: {
            top: 'auto',
            right: 10,
            bottom: 80
        }
    })

    myMap.controls.add('geolocationControl', {
        position: {
            top: 'auto',
            right: 10,
            bottom: 300
        }
    })
    
    const markers = []

    // Get all sitters
    await makeRequest(`${searchUrl}all`, 'get').then(
        response => PEOPLE = response
    )

    // Place sitters markers on the map
    PEOPLE.forEach(person => {
        // if no coordinates - don't place the markers
        if (!person?.coordinates) return

        // create markers
        var placemark = new ymaps.Placemark(person.coordinates, {
            hintContent: person.name,
            balloonContent: 'Name: ' + person.name + '<br>ID: ' + person.id
        }, {
            iconLayout: 'default#image',
            iconImageHref: `${staticUrl}images/icons/ymap-marker.svg`,
            iconImageSize: [30, 42],
            iconImageOffset: [-15, -42]
        })
        myMap.geoObjects.add(placemark)
        markers.push({person, placemark})
    })


    // Triggers every time map is moved or zoomed
    function updateVisiblePeople() {
        idList = []
        const bounds = myMap.getBounds()
        markers.forEach(function(marker) {
            const coord = marker.person.coordinates
            if (bounds[0][0] <= coord[0] && coord[0] <= bounds[1][0] &&
                bounds[0][1] <= coord[1] && coord[1] <= bounds[1][1]) {
                idList.push(marker.person.id)
            }
        })
        refreshSitters() // show sitters in a list
    }

    myMap.events.add('boundschange', updateVisiblePeople)

    updateVisiblePeople() // Initial update

    // Geosuggest
    var suggestView = new ymaps.SuggestView('address-input')

    suggestView.events.add('select', function (e) {
        var address = e.get('item').value

        ymaps.geocode(address).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0)
            var coords = firstGeoObject.geometry.getCoordinates()
            myMap.setCenter(coords, 14)
        })
    })
}









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
    const lazyCat = document.querySelector('.sitter__lazy-cat')
    let lazyInterval
    // if there is no sitters found
    if (!sitterList.querySelector('.sitter__item')) {
        // show empty message
        paginator.style.display = 'none'
        emptyMessage.removeAttribute('style')

        // play lazy cat animation every 3 seconds
        lazyCat.play()
        lazyInterval = setInterval(() => lazyCat.play(), 3000)
    } else {
        // hide empty message
        paginator.removeAttribute('style')
        emptyMessage.style.display = 'none'

        // stop lazy cat animation
        lazyCat.load()
        clearInterval(lazyInterval)
    }
}

handleEmptyList()


/*======================== REFRESH SITTERS ========================*/
function refreshSitters() {
    const form = document.querySelector('.filter__form')
    const formData = new FormData(form)
    formData.append('idList', idList)

    const data = Object.fromEntries(formData)

    makeRequest(searchUrl, 'post', data)
    .then(response => {
        PEOPLE = response
        renderSitterList(response)
    })
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

        // Sitter link
        let a = document.createElement('a')
        if (sitter?.id) 
            a.href = `${homeUrl}sitters/${sitter.id}`
        a.className = 'sitter__image-container'

        // Avatar image
        let img = document.createElement('img')
        sitter?.imageUrl 
            ? img.src = sitter.imageUrl
            : img.src = `${staticUrl}images/global/default-avatar.png`
        img.className = 'sitter__image'
        img.alt = 'sitter photo'
        a.appendChild(img)

        // Tags
        if (sitter?.tags) {
            sitter.tags.forEach(tagName => {
                let imgIcon, iWalk;
                let spanTag = document.createElement('span')
                spanTag.className = 'sitter__tag'
                switch (tagName) {
                    case 'dogsitter':
                        imgIcon = document.createElement('img')
                        imgIcon.className = 'sitter__tag-icon'
                        imgIcon.src = `${staticUrl}images/icons/dog-icon.svg`
                        imgIcon.alt = 'icon'
                        spanTag.appendChild(imgIcon)
                        spanTag.appendChild(document.createTextNode('Догситтер'))
                        break
                    case 'catsitter':
                        imgIcon = document.createElement('img')
                        imgIcon.className = 'sitter__tag-icon'
                        imgIcon.src = `${staticUrl}images/icons/cat-icon.svg`
                        imgIcon.alt = 'icon'
                        spanTag.appendChild(imgIcon)
                        spanTag.appendChild(document.createTextNode('Кэтситтер'))
                        break
                    case 'walk':
                        iWalk = document.createElement('i')
                        iWalk.className = 'ri-walk-line'
                        spanTag.appendChild(iWalk)
                        spanTag.appendChild(document.createTextNode('Выгульщик'))
                        break
                    case 'boarding':
                        iWalk = document.createElement('i')
                        iWalk.className = 'ri-home-heart-line'
                        spanTag.appendChild(iWalk)
                        spanTag.appendChild(document.createTextNode('Бордер'))
                        break
                    case 'daycare':
                        iWalk = document.createElement('i')
                        iWalk.className = 'ri-hand-heart-line'
                        spanTag.appendChild(iWalk)
                        spanTag.appendChild(document.createTextNode('Дневная Няня'))
                        break
                    default: 
                        spanTag.appendChild(document.createTextNode(tagName))
                }
                a.appendChild(spanTag)
            })
        }

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
            ? spanReviews.textContent = sitter.reviews + ' отзывов'
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
            renderStars(divRating, sitter.rating)
            divRatingNumber.textContent = sitter.rating.toFixed(1)
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

        // Price
        let divPrice = document.createElement('div')
        divPrice.className = 'sitter__price'
        if (sitter?.price)
            divPrice.textContent = `${sitter.price} ₽`

        // Sitter link 2
        let aLink = document.createElement('a')
        aLink.className = 'sitter__link'
        if (sitter?.id) 
            aLink.href = `${homeUrl}sitters/${sitter.id}`
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
