/*======================== STAR RENDER ========================*/
initStarRender('.sitter__stars', '.sitter__rating-number')
initStarRender('#stars-container', '#rating-number')
function initStarRender(conClass, numClass) {
    const numberContainer = document.querySelector(numClass)
    const rating = parseFloat(numberContainer.textContent.replace(',', '.'))
    numberContainer.textContent = rating.toFixed(1)

    renderStars(
        document.querySelector(conClass),
        rating
    )
}



/*======================== ALBUM ========================*/
// Handle more than 5 photos
handleAlbumOverflow()
function handleAlbumOverflow() {
    imageCons = document.querySelectorAll('.about__image-container')
    console.log(imageCons.length)
    if (imageCons.length > 5) {
        const lastCon = imageCons[4]
        lastCon.querySelector('img').style.display = 'none'
        lastCon.classList.add('about__image-all')
        lastCon.textContent = 'Посмотреть еще фото'
    }
}



