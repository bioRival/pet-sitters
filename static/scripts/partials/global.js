// Function to cut the string short adding ellipsis
function truncate(str, max) {
    return str.length > max ? str.substr(0, max-1) + '…' : str;
}





/*======================== REQUEST ========================*/
// Json Fetch request
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




/*======================== STAR RENDER ========================*/
// adds star icons into container depending on given rating
// example: renderStars(document.getElementById('con'), 4.5)
function renderStars(container, rating) {
    if (!typeof rating == 'number') return
    if (rating > 5 || rating < 0) return

    let fullStars = Math.floor(rating)
    let hollowStars = 5 - Math.floor(rating)
    let remainder = rating - Math.floor(rating)
    // print full stars first
    for (let i = 0; i < fullStars; i++) {
        let iStar = document.createElement('i')
        iStar.className = 'ri-star-fill'
        container.appendChild(iStar)
    }
    // if remainder above 0.5 - print half star
    if (remainder >= 0.5) {
        let iStar = document.createElement('i')
        iStar.className = 'ri-star-half-line'
        container.appendChild(iStar)
        hollowStars -= 1
    }
    // print hollow stars last
    for (let i = 0; i < hollowStars; i++) {
        let iStar = document.createElement('i')
        iStar.className = 'ri-star-line'
        container.appendChild(iStar)
    }
}






/*======================== RADIO TOGGLE ========================*/
// makes radio buttons uncheckable on click
applyRadioToggle('.filter__button')
function applyRadioToggle(labelName) {
    document.querySelectorAll(labelName).forEach(label => {
        label.addEventListener('click', (e) => {
            e.preventDefault()
            let input = document.getElementById(label.htmlFor)
            if (input.checked) {
                input.checked = false
            } else {
                input.checked = true
            }
            triggerFormChangeEvent()
        })
    })
    
    // Function to trigger the change event on the form
    function triggerFormChangeEvent() {
        const form = document.querySelector('.filter__form')
        const event = new Event('change', {
            bubbles: true,  // Allow the event to bubble up the DOM
            cancelable: true  // Allow the event to be canceled
        });
        form.dispatchEvent(event);
    }
}