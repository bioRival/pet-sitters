// =========================================================
// DATA - test example of data from server
// =========================================================
const PEOPLE = [
    {
        "id": 1,
        "name": "Белка Стрелка",
        "price": 800,
        "coordinates": [37.48393778966657, 55.74814175164691]
    },
    {
        "id": 2,
        "name": "Серый Волк",
        "price": 1100,
        "coordinates": [37.79372314793984, 55.77778803795607]
    },
    {
        "id": 3,
        "name": "Шимпанзе Энос",
        "price": 500,
        "coordinates": [37.54681901505547, 55.4552872934669]
    }
]

// =========================================================
// ADDRESS AUTOCOMPLETE
// =========================================================

// Yandex Geocode API
const API_KEY_Y_GECODE = '23ed166a-ffb0-4867-b8fc-f0ae8521ea51'

// Yandex Geosuggest API
const API_KEY_Y_GEOSUGGEST = "078789ba-87af-4113-b9cf-35a9cb93c231"


// initAddressAutocomplete - initializes autocomplete
//  callback - function executed upon click on autocomplete item
function initAddressAutocomplete(callback) {

    // Get container for input element
    const inputContainerElement = document.getElementById("filter__geosuggest-container")

    // Get input element
    const inputElement = document.getElementById("address-input")

    // Minimum letters before autocomplete will react
    const MIN_ADDRESS_LENGTH = 3

    // Delay before autocomplete will react to input in ms
    const DEBOUNCE_DELAY = 1000

    let currentTimeout

    /* Process a user input: */
    inputElement.addEventListener("input", function (e) {
        // Cancel previous timeout
        if (currentTimeout) clearTimeout(currentTimeout)

        /* Current autocomplete items data */
        let currentItems
        const currentValue = this.value

        // Skip empty or short address strings
        if (!currentValue || currentValue.length < MIN_ADDRESS_LENGTH) {
            return false;
        }

        /* Call the Address Autocomplete API with a delay */
        currentTimeout = setTimeout(() => {

            /* Create a new promise and send geocoding request */
            const promise = new Promise((resolve, reject) => {

                // API call to yandex geosuggest
                const URL = `https://suggest-maps.yandex.ru/v1/suggest?apikey=${API_KEY_Y_GEOSUGGEST}&types=district,locality,metro,street&print_address=1&text=${encodeURIComponent(currentValue)}`

                fetch(URL)
                    .then(response => {

                        // check if the call was successful
                        if (response.ok) {
                            response.json().then(data => resolve(data))
                        } else {
                            response.json().then(data => reject(data))
                        }
                    })
            })

            promise.then((data) => {
                // here we get address suggestions
                currentItems = data.results;

                // Clean autocomplete-items
                closeDropDownList()

                /*create a DIV element that will contain the items (values):*/
                const autocompleteItemsElement = document.createElement("div")
                autocompleteItemsElement.setAttribute(
                    "class",
                    "filter__autocomplete-items"
                )
                inputContainerElement.appendChild(autocompleteItemsElement)

                /* For each item in the results */
                data.results.forEach((result, index) => {
                    /* Create a DIV element for each element: */
                    const itemElement = document.createElement("div")

                    /* Set formatted address as item value */
                    const text = result.address.formatted_address
                    itemElement.innerHTML = text

                    /* Set the value for the autocomplete text field and notify: */
                    itemElement.addEventListener("click", function (e) {
                        inputElement.value = text
                        callback(e)
                        /* Close the list of autocompleted values: */
                        closeDropDownList()
                    })

                    autocompleteItemsElement.appendChild(itemElement)
                })

            }, (err) => {
                if (!err.canceled) {
                    console.log(err)
                }
            });
        }, DEBOUNCE_DELAY);
    })

    function closeDropDownList() {
        const autocompleteItemsElement =
            inputContainerElement.querySelector(".filter__autocomplete-items")
        if (autocompleteItemsElement) {
            inputContainerElement.removeChild(autocompleteItemsElement)
        }
    }

    /* Close the autocomplete dropdown when the document is clicked. 
    Skip, when a user clicks on the input field */
    document.addEventListener("click", function (e) {
        if (e.target !== inputElement) {
            closeDropDownList()
        }
    })
}






// =========================================================
// YANDEX MAP
// =========================================================
async function initMap() {
    await ymaps3.ready

    const {
        YMap,
        YMapDefaultSchemeLayer,
        YMapMarker,
        YMapDefaultFeaturesLayer,
        YMapControls,
    } = ymaps3

    // Load the control package and extract the geolocation control from it
    const { YMapGeolocationControl } = await ymaps3.import('@yandex/ymaps3-controls@0.0.1')

    const map = new YMap(
        document.getElementById('map'),
        {
            location: {
                center: [37.61911740784069, 55.75918886347444],
                zoom: 12
            }
        }
    )

    // Adding layer with roads and buildings
    map.addChild(new YMapDefaultSchemeLayer())

    // Adding layer for markers
    map.addChild(new YMapDefaultFeaturesLayer())

    // Adding geolocation button
    map.addChild(
        // Using YMapControls you can change the position of the control
        new YMapControls({ position: 'top right' })
            // Add the geolocation control to the map
            .addChild(new YMapGeolocationControl({}))
    )

    
    // Initilize marker
    PEOPLE.forEach(person => {
        const content = document.createElement('img')
        content.src = `${staticUrl}images/icons/ymap-marker.svg`
        content.style = `
            width: 50px; 
            height: 50px; 
            transform: translate(-50%, -100%);
        `

        const marker = new YMapMarker(
            {
                coordinates: person.coordinates,
            },
            content
        )

        // Adding marker on the map
        map.addChild(marker);
    })


    // Initilize autocomplete and pass function on click
    initAddressAutocomplete(
        (e) => {
            const address = e.target.textContent

            // Makes a call to geocode yandex, moves map if location is found
            async function updateMapOnClick() {
                const response = await fetch(`https://geocode-maps.yandex.ru/1.x/?apikey=${API_KEY_Y_GECODE}&geocode=${encodeURIComponent(address)}&format=json`)
                const geodata = await response.json()

                // Update map if coordinates exist
                try {
                    // Format coordinates from string to number array
                    let coordinates = geodata.response.GeoObjectCollection.featureMember[0].GeoObject.Point.pos.split(" ")
                    coordinates = coordinates.map(coord => Number(coord))

                    // Update map
                    map.update(
                        {
                            location: {
                                center: coordinates,
                                zoom: 12,
                                duration: 1000
                            }
                        })
                } catch (error) {
                    console.error(error)
                }
            }
            updateMapOnClick()
        }
    )
}

initMap()

