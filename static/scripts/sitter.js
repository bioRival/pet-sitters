/*======================== STAR RENDER ========================*/
initStarRender()
function initStarRender() {
    const numberContainer = document.querySelector('.sitter__rating-number')
    const rating = parseFloat(numberContainer.textContent)
    numberContainer.textContent = rating.toFixed(1)

    renderStars(
        document.querySelector('.sitter__stars'),
        rating
    )
}