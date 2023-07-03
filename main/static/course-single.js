const courseId = document.getElementById('course-id').textContent

getCourseData()

function getCourseData() {
    fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    document.getElementById('course-sections').innerHTML = ''
    document.getElementById('course-name').textContent = data.name
    document.getElementById('course-short_description').textContent = data.short_description
    document.getElementById('course-date_updated').textContent = data.date_updated
    document.getElementById('course-language').textContent = data.language
    data.sections.forEach(section => createSection(section))
}

function expandSection(event) {
    this.classList.toggle('invisible')
}

function createSection(section) {
    const clone = document.getElementById('template-course-section').content.cloneNode(true)
    const sectionDiv = clone.querySelector('div.course-section')
    clone.querySelector('span.section-name').textContent = section.name
    sectionDiv.setAttribute('section-id', section.id)
    clone.querySelector('svg.section-header-icon-expand').addEventListener('click', expandSection.bind(clone.querySelector('div.course-section-body')))
    
    // const filteredItems = section.items.filter(item => {
    //     const optionIndex = courseOptions.findIndex(el => el === courseOption)
    //     const slicedArr = courseOptions.slice(0, optionIndex + 1)
    //     return slicedArr.includes(item.option)
    // })
    section.items.forEach(item => createItem(clone.querySelector('div.course-section'), item))
    document.getElementById('course-sections').append(clone)
}


function createItem(section, item) {
    const itemTemplate = document.getElementById('template-section-item')
    const clone = itemTemplate.content.cloneNode(true)
    clone.querySelector('.item-name').textContent = item.name
    clone.querySelector('.section-item').setAttribute('item-id', item.id)
    clone.querySelector('.section-item').setAttribute('item-type', item.type)
    clone.querySelector('svg use').setAttribute('href', `#icon-${item.type}`)
    section.querySelector('.section-items').append(clone)
}