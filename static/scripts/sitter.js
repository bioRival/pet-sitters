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




