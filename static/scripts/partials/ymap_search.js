// =========================================================
// DATA - test example of data from server
// =========================================================
const PEOPLE = [
    {id: 1, name: 'Alice', coordinates: [55.751244, 37.618423]},
    {id: 2, name: 'Bob', coordinates: [55.755826, 37.6173]},
    {id: 3, name: 'Charlie', coordinates: [55.752023, 37.617499]},
    // Add more people as needed
]




// =========================================================
// YANDEX MAP INITIATION
// =========================================================
ymaps.ready(initMap)
function initMap(){
    var myMap = new ymaps.Map("map", {
        center: [55.751574, 37.573856], // Moscow coordinates
        zoom: 10,
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

    // Place sitters markers on the map
    PEOPLE.forEach(person => {
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

    
    // Show only those sitters, who are visible on the map
    const peopleList = document.getElementById('people-list')

    function updateVisiblePeople() {
        const bounds = myMap.getBounds()
        peopleList.innerHTML = ''
        markers.forEach(function(marker) {
            const coord = marker.person.coordinates
            if (bounds[0][0] <= coord[0] && coord[0] <= bounds[1][0] &&
                bounds[0][1] <= coord[1] && coord[1] <= bounds[1][1]) {
                const listItem = document.createElement('li')
                listItem.textContent = marker.person.name
                peopleList.appendChild(listItem)
            }
        })
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

