// Basement Cat Easter egg
function initBasedCat() {
    const   pawButton = document.querySelector('.footer__paw-icon'),
            basedCat = document.querySelector('.footer__based-cat')
    let clickCount = 0

    if (!pawButton && !basedCat) return

    pawButton.addEventListener('click', () => {
        clickCount += 1
        console.log("clickCount: " + clickCount)

        if (clickCount >= 3) {
            basedCat.classList.toggle('footer__show-based-cat')
        }
    })

    // If user at the bottom of the page
    // window.addEventListener('scroll', () => {
    //     if ((window.innerHeight + Math.round(window.scrollY)) >= document.body.offsetHeight) {
    //         basedCat.classList.add('footer__show-based-cat')
    //     }
    // })
}

initBasedCat()