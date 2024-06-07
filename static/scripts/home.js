
/*=============================== BANNER SLIDESHOW ===============================*/
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




/*=============================== CAT / DOG FILTER BUTTONS ===============================*/
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
        console.log("Hello")
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





