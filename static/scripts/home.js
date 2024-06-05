
/*=============================== BANNER SLIDESHOW ===============================*/
function bannerSlideshow() {
    // Getting array of images
    
    let images = [...document.querySelectorAll('.banner__image')]
    images.reverse() // they are backwards, so reversing in order

    let current = 0 // index of image visible

    function slideshow() {
        // images.classList.remove('banner__show-image')
        // document.querySelectorAll('.banner__image').classList.remove('banner__show-image')
        for (let i = 0; i < images.length; i++) {
            images[i].style.opacity = 0
            images[i].style.transform = `translateX(1rem)`
        }
        current = (current != images.length - 1) ? current + 1 : 0

        images[current].style.opacity = 1
        images[current].style.transform = `translateX(-1rem)`
        // images[current].classList.add('banner__show-image')
    }
    slideshow(); // Execute on loading the page first
    setInterval(slideshow, 5000); // Setting the time in ms
}

bannerSlideshow()