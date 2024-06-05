/*========================= SHOW MENU =========================*/

const   navMenu = document.getElementById('nav-menu'),
navToggle = document.getElementById('nav-toggle'),
navClose = document.getElementById('nav-close')


// Menu show
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    })
}

if(navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

/*========================= REMOVE MENU MOBILE =========================*/
const navLink = document.querySelectorAll('.nav__link')

navLink.forEach(link => link.addEventListener('click', () => {
    const navMenu = document.getElementById('nav-menu')
    // When we click on any nav__link, we remove show-menu class
    navMenu.classList.remove('show-menu')
}))


/*========================= TURN HEADER STICKY  =========================*/
window.addEventListener('scroll', () => {
    const header = document.getElementById('header')
    if (window.innerWidth <= 1150) {
        if (window.scrollY >= 100) {
            header.classList.add('sticky-header')
        } else {
            header.classList.remove('sticky-header')
        }
    }
})