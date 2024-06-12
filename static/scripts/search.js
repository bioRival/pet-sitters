/*======================== SITTER IMAGE HOVER ========================*/
// When hovering on the sitter image, 
// the arrow button moves to the right a bit.
// Impossible to achieve with CSS, 
// since image is not a parent of an arrow button
function initSitterHover() {
    const images = document.querySelectorAll('.sitter__image-container')

    images.forEach(image => {
        const link = image.parentElement.querySelector('.sitter__link')

        image.addEventListener('mouseover', () => {
            link.style.transform = 'translateX(.5rem)'
        })

        image.addEventListener('mouseout', () => {
            link.removeAttribute('style')
        })
    })
}

initSitterHover()