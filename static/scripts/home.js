
/*========================= BANNER SLIDESHOW =========================*/
function bannerSlideshow() {
    // Getting array of images
    // let images = [...document.querySelectorAll('.banner__image')]
    let images = document.querySelectorAll('.banner__image')
    // images.reverse() // they are backwards, so reversing in order

    // Getting carousel dots
    let dots = document.querySelectorAll('.banner__carousel-indicators li')

    let current = 0 // index of image visible

    function slideshow() {
        for (let i = 0; i < images.length; i++) {
            images[i].classList.remove('banner__show-image')
            dots[i].classList.remove('active')
        }

        images[current].classList.add('banner__show-image')
        dots[current].classList.add('active')
        
        current = (current != images.length - 1) ? current + 1 : 0
    }
    
    slideshow(); // Execute on loading the page first
    setInterval(slideshow, 5000); // Setting the time in ms
}

bannerSlideshow()




/*====================== CAT / DOG FILTER BUTTONS ======================*/
function initCatDogButtons() {
    let timeout;
    function handleChange(e, pngImg, gifImg) {
        if (e.currentTarget.checked) {
            clearTimeout(timeout)
            pngImg.style.display = 'none'
            gifImg.style.display = 'inline-block'
            timeout = setTimeout(() => {
                pngImg.style.display = 'inline-block'
                gifImg.style.display = 'none'
            }, 800)
        } else {
            pngImg.style.display = 'inline-block'
            gifImg.style.display = 'none'
        }
    }

    document.getElementById('checkbox-dog').addEventListener('change', (e) => handleChange(
        e,
        document.getElementById('dog-png'),
        document.getElementById('dog-gif'),
    ))
    document.getElementById('checkbox-cat').addEventListener('change', (e) => handleChange(
        e,
        document.getElementById('cat-png'),
        document.getElementById('cat-gif'),
    ))


}
initCatDogButtons()



/*========================= REVIEW CAROUSEL =========================*/
initReviewCarusel()
function initReviewCarusel() {
    // Grid gap in px
    const gap = 20;

    const   carousel = document.getElementById("review__carousel"),
            content = document.getElementById("review__content"),
            next = document.getElementById("review__next"),
            prev = document.getElementById("review__prev")

    // Next button 
    next.addEventListener("click", e => {
        carousel.scrollBy(width + gap, 0)

        if (carousel.scrollWidth !== 0) {
            prev.style.display = "flex";
        }

        if (content.scrollWidth - width - gap <= carousel.scrollLeft + width) {
            next.style.display = "none";
        }
    })

    // Previous button 
    prev.addEventListener("click", e => {
        carousel.scrollBy(-(width + gap), 0)
        if (carousel.scrollLeft - width - gap <= 0) {
            prev.style.display = "none"
        }
        if (!content.scrollWidth - width - gap <= carousel.scrollLeft + width) {
            next.style.display = "flex"
        }
    })

    let width = carousel.offsetWidth
    window.addEventListener("resize", e => (width = carousel.offsetWidth))

}
// review truncate
document.querySelectorAll('.review__text').forEach(review => {
    review.textContent = truncate(review.textContent, 320)
})







/*========================= ACCORDION =========================*/
function initAccordion() {
    const items = document.querySelectorAll('.accordion__item')

    items.forEach((item) => {
        const header = item.querySelector('.accordion__header')

        header.addEventListener('click', () => {
            const openItem = document.querySelector('.accordion-open')
            
            toggleItem(item)

            // when clicked on the other item, close the previous one
            if (openItem && openItem !== item) {
                toggleItem(openItem)
            }
        })


    })

    function toggleItem(item) {
        const content = item.querySelector('.accordion__content')

        if (item.classList.contains('accordion-open')) {
            content.removeAttribute('style')
            item.classList.remove('accordion-open')
        } else {
            content.style.height = content.scrollHeight + 'px'
            item.classList.add('accordion-open')
        }


    }

}

initAccordion()

