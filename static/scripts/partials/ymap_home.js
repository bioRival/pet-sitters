// =========================================================
// DATA variables
// =========================================================
// list of sitters
let PEOPLE = []

// current map states
let CENTER, ZOOM



// =========================================================
// YANDEX MAP INITIATION
// =========================================================
ymaps.ready(initMap)
async function initMap(){
    var myMap = new ymaps.Map("map", {
        center: [55.751574, 37.573856], // Moscow coordinates
        zoom: 12,
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

    // On Bounds change
    myMap.events.add('boundschange', updateLocation)
    function updateLocation() {
        CENTER = myMap.getCenter()
        ZOOM = myMap.getZoom()
    }

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





/*========================= ON SUBMIT =========================*/
// filter submit button sends user to search page
// and fills the form with saved data
document.querySelector('.filter__form').addEventListener('submit', (e)=>{
    e.preventDefault()
    const form = document.querySelector('.filter__form')
    const formData = new FormData(form)


    // cleanup - delete empty fields caught in query
    if (!formData.get('date-start')) {
        formData.delete('date-start')
    }
    if (!formData.get('date-end')) {
        formData.delete('date-end')
    }
    if (!formData.get('address')) {
        formData.delete('address')
    }

    // Add map states if they were changed
    if (CENTER && ZOOM) {
        formData.append('zoom', ZOOM)
        formData.append('center', CENTER)
    }

    // Check if FormData has data
    const hasData = formData.entries().next().done === false;

    if (hasData) {
        const queryString = new URLSearchParams(formData).toString()
        window.location.href = `${searchUrl}?${queryString}`
    } else {
        window.location.href = searchUrl
    }
})
