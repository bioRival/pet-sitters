/*========================= SHOW MENU =========================*/

const   navMenu = document.getElementById('nav-menu'),
navToggle = document.getElementById('nav-toggle'),
navClose = document.getElementById('nav-close')


// Menu show
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    })
    console.log('navToggle')
}

if(navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
    console.log('navClose')
}

/*========================= REMOVE MENU MOBILE =========================*/
const navLink = document.querySelectorAll('.nav__link')

navLink.forEach(link => link.addEventListener('click', () => {
    const navMenu = document.getElementById('nav-menu')
    // When we click on any nav__link, we remove show-menu class
    navMenu.classList.remove('show-menu')
}))


/*========================= ADD BLUR HEADER =========================*/
function blurHeader() {
    const header = document.getElementById('header')
    this.scrollY >= 50  ? header.classList.add('blur-header')
                        : header.classList.remove('blur-header')
}
window.addEventListener('scroll', blurHeader)