const courseId = document.getElementById('course-id').textContent

getCourseData()


let player = videojs(document.querySelector('.video-js'))

player.playlist([
    { 
    name: 'Video1',
    sources: [{
        src: '/files/media/courses/lessons/0.0_%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5.mp4',
        type: 'video/mp4'
    }]
}, 
{
    name: 'video2',
    sources: [{
        src: '/files/media/courses/lessons/1.1_%D0%94%D0%BB%D1%8F_%D1%87%D0%B5%D0%B3%D0%BE_%D0%BD%D1%83%D0%B6%D0%BD%D0%B0_%D0%9E%D0%A1.mp4',
        type: 'video/mp4'
    }]
}, {
    name: 'video3',
    sources: [{
        src: '/files/media/courses/lessons/1.2_%D0%9F%D0%B5%D1%80%D0%B2%D0%B0%D1%8F_%D0%9E%D0%A1_._%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F_Multics.mp4',
        type: 'video/mp4'
    }]
}  
])
player.playlist.autoadvance(0)
player.on('playlistitem', () => {})
document.getElementById('ui-next-video').addEventListener('click', event => player.playlist.currentItem(2))

// player.playlistUi()

function getCourseData() {
    fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    document.getElementById('course-sections').innerHTML = ''
    document.getElementById('course-name').textContent = data.name
    document.getElementById('course-short_description').textContent = data.short_description
    document.getElementById('course-date_updated').textContent = data.date_updated
    document.getElementById('course-language').textContent = data.language
    
    data.what_will_learn.forEach(item => {
        const clone = document.getElementById('template-what_will_learn').content.cloneNode(true)
        clone.querySelector('span').textContent = item
        document.getElementById('what_will_learn-items').append(clone)
    })

    let lessonCounter = 0
    data.sections.forEach(section => {
        lessonArr = section.items.filter(item => item.type === 'lesson')
        lessonCounter += lessonArr.length
    })
    document.getElementById('course-content-info').textContent = `${data.sections.length} секций - ${lessonCounter} видеоуроков`
    
    data.sections.forEach(section => createSection(section))

    data.requirements.forEach(requierement => {
        const clone = document.getElementById('template-requirements').content.cloneNode(true)
        clone.querySelector('li').textContent = requierement
        document.querySelector('#course-requirements ul').append(clone)
    })

    document.getElementById('course-full_description').innerHTML = data.full_description

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