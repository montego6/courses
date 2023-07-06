const categoriesLink = document.getElementById('header-categories-link')
const popoverMenu = document.getElementById('header-popover-categories')
const popoverSubMenu = document.getElementById('header-popover-subcategories')
const popoverSubjects = document.getElementById('header-popover-subjects')
const popoverTemplate = document.getElementById('header-popover-template')
let categories


fetch('http://localhost:8000/api/categories/').then(response => response.json())
.then(data => {
    categories = data
    createMenuElements(categories, popoverMenu)
})

const backdrop = document.querySelector('#backdrop')


getChildMenu = (menu) => (menu === popoverMenu ? popoverSubMenu : popoverSubjects) 
getChildElements = (menu, element) => (menu === popoverMenu ? element.subcategories: element.subjects)

function createMenuElements(catList, menu) {
    catList.forEach(catElement => {
        const clone = popoverTemplate.content.cloneNode(true)
        clone.querySelector('a').textContent = catElement.name
        const divEl = clone.querySelector('div')
        if (!(menu === popoverSubjects)) 
        {
            divEl.addEventListener('mouseenter', showSubMenu.bind(divEl, menu, catElement))
        }
        menu.append(clone)
    });
}

function showSubMenu(menu, element, event) {
    const childMenu = getChildMenu(menu)
    childMenu.innerHTML = ''
    childMenu.classList.remove('invisible')
    createMenuElements(getChildElements(menu, element), childMenu)
    childMenu.addEventListener('mouseleave', hideMenu.bind(childMenu))
}

function hideMenu (event) {
    menuCoords = this.getBoundingClientRect()
    if (!(event.clientX + 3 >= menuCoords.right)) {
        this.classList.add('invisible')
        getChildMenu(this).classList.add('invisible')
    } else if (this === popoverSubjects) {
        popoverMenu.classList.add('invisible')
        popoverSubMenu.classList.add('invisible')
        popoverSubjects.classList.add('invisible')
    }
}

categoriesLink.addEventListener('mouseenter', (event) => {popoverMenu.classList.remove('invisible')})
categoriesLink.addEventListener('mouseleave', (event) => 
{
    catLinkCoords = categoriesLink.getBoundingClientRect()
    if (!(event.clientY >= catLinkCoords.bottom)) {
        popoverMenu.classList.add('invisible')
    }
}
)
popoverMenu.addEventListener('mouseleave', hideMenu.bind(popoverMenu))
