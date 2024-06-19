let PEOPLE

// get coordinates of sitter through dataset left in main
function getCoords() {
    const coords = document.querySelector('.main').dataset.coords
    try {
        return JSON.parse(coords)
    } catch (error) {
        console.log(error)
        return null
    }
    
}





// =========================================================
// YANDEX MAP INITIATION
// =========================================================
ymaps.ready(initMap)
async function initMap(){
    const sitterCoords = getCoords()

    var myMap = new ymaps.Map("map", {
        center: sitterCoords || [55.7605173, 37.6185126], // Moscow coordinates
        zoom: 11,
        controls: [],
    })
    
    const markers = []

    // Get all sitters
    // await makeRequest(`${searchUrl}all`, 'get').then(
    //     response => PEOPLE = response
    // )

    // Place sitter on the map
    // if no coordinates - don't place the marker
    
    if (sitterCoords) {
        let placemark = new ymaps.Placemark(sitterCoords, {
            hintContent: 'dummy',
            balloonContent: 'something'
        }, {
            iconLayout: 'default#image',
            iconImageHref: `${staticUrl}images/icons/ymap-marker.svg`,
            iconImageSize: [30, 42],
            iconImageOffset: [-15, -42]
        })
        myMap.geoObjects.add(placemark)
        // markers.push({person, placemark})
    }
}