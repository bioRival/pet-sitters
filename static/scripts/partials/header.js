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




/*========================= USER-DROPDOWN MENU =========================*/
function showUserDropdown(content, button) {
    const   dropdownContent = document.getElementById(content),
            dropdownButton = document.getElementById(button)
    
    // If elements exist
    if (dropdownButton && dropdownContent) {
        // Show menu
        dropdownButton.addEventListener('click', () => {
            dropdownContent.classList.toggle('show-user-dropdown')
        })

        // When menu is open click on anything else to close it
        document.addEventListener('click', (e) => {
            if (e.target !== dropdownButton) {
                dropdownContent.classList.remove('show-user-dropdown')
            }
        })
    }
}

showUserDropdown('user-dropdown-content', 'user-dropdown-button')

