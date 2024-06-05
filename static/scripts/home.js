
/*=============================== BANNER SLIDESHOW ===============================*/
function bannerSlideshow() {
    // Getting array of images
    
    let images = [...document.querySelectorAll('.banner__image')]
    images.reverse() // they are backwards, so reversing in order

    let current = 0 // index of image visible

    function slideshow() {
        for (let i = 0; i < images.length; i++) {
            images[i].classList.remove('banner__show-image')
        }

        current = (current != images.length - 1) ? current + 1 : 0

        images[current].classList.add('banner__show-image')
    }
    
    slideshow(); // Execute on loading the page first
    setInterval(slideshow, 5000); // Setting the time in ms
}

bannerSlideshow()