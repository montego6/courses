categoriesLink = document.getElementById('header-categories-link')
popoverMenu = document.getElementById('header-popover-categories')

categoriesLink.addEventListener('mouseenter', (event) => {popoverMenu.classList.remove('invisible')})
categoriesLink.addEventListener('mouseleave', (event) => 
{
    catLinkCoords = categoriesLink.getBoundingClientRect()
    if (!(event.clientY >= catLinkCoords.bottom)) {
        popoverMenu.classList.add('invisible')
    }
}
)
popoverMenu.addEventListener('mouseleave', (event) => {popoverMenu.classList.add('invisible')})
