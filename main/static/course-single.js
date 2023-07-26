const courseId = document.getElementById('course-id').textContent

getCourseData()

class Lesson {
    constructor(id, data, sectionIndex) {
        this.id = id
        this.name = data.name
        this.file = data.file
        this.section = sectionIndex
    }

    get playlistElement() {
        return {
            name: this.name,
            sources: [{
                src: this.file,
                type: 'video/mp4'
            }]
        }
    }
}

class LessonManager {
    static lessons = []
    
    static addLesson(lesson) {
        this.lessons.push(lesson)
    }

    static get lessonsPlaylist() {
        return Array.from(this.lessons, lesson => lesson.playlistElement)
    }

    static findLessonById(lessonId) {
        return this.lessons.find(lesson => lesson.id === lessonId)
    }
    
    static getSectionLessons(lessonId) {
        const currentLesson = this.findLessonById(lessonId)
        return this.lessons.filter(lesson => lesson.section === currentLesson.section)
    }

    static getNextSectionLesson(lessonId) {
        const currentLesson = this.findLessonById(lessonId)
        return this.lessons.find(lesson => lesson.section === currentLesson.section + 1)
    }

    static getPreviousSectionLesson(lessonId) {
        const currentLesson = this.findLessonById(lessonId)
        return this.lessons.findLast(lesson => lesson.section === currentLesson.section - 1)
    }
}

class Section {
    constructor(sectionData) {
        this.name = sectionData.name
        this.items = sectionData.items
        this.element = this.renderElement(this.createElement())
    }

    createElement() {
        const clone = document.getElementById('template-course-section').content.cloneNode(true)
        clone.querySelector('span.section-name').textContent = this.name
        clone.querySelector('svg.section-header-icon-expand').addEventListener('click', this.expandSection.bind(this))
        return clone
    }

    renderElement(element) {
        document.getElementById('course-sections').append(element)
        return document.getElementById('course-sections').lastElementChild
    }

    createItems() {
        this.items.forEach(item => {
            switch (item.type) {
                case 'lesson':
                    new SectionLesson(this, item)
                    break
                default:
                    new SectionItem(this, item)
            }
        })
    }

    expandSection() {
        this.element.querySelector('div.course-section-body').classList.toggle('invisible')
    }
}


class SectionItem {
    constructor(section, itemData) {
        this.section = section
        this.data = itemData
        this.name = itemData.name
        this.type = itemData.type
        this.option = itemData.option
        this.element = this.renderElement(this.createElement())
        this.extra()
        ContentManager.addToManager(this)
    }

    createElement() {
        const itemTemplate = document.getElementById('template-section-item')
        const clone = itemTemplate.content.cloneNode(true)
        clone.querySelector('.item-name').textContent = this.name
        clone.querySelector('svg use').setAttribute('href', `#icon-${this.type}`)
        return clone
    }

    renderElement(clone) {
        this.section.element.querySelector('.section-items').append(clone)
        return this.section.element.querySelector('.section-items').lastElementChild
    }

    extra() {
        
    }
}


function formatVideoLessonDuration(duration) {
    const hours = Math.floor(duration / 3600)
    const minutes = Math.floor(duration % 3600 / 60)
    const seconds = Math.floor(duration % 3600 % 60)

    const hoursDisplay = hours > 0 ? hours < 10 ? "0" + hours + ":" : hours + ":" : ""
    const minutesDisplay = minutes > 0 ? minutes < 10 ? "0" + minutes + ":" : minutes + ":" : ""
    const secondsDisplay = seconds > 0 ? seconds < 10 ? "0" + seconds : seconds : ""
    return hoursDisplay + minutesDisplay + secondsDisplay 
}


class SectionLesson extends SectionItem {
    extra() {
        if (this.data.file) {
            this.element.querySelector('.item-name').classList.add('lesson-link')
        }
        if (this.data.duration) {
            this.element.querySelector('.item-right span').textContent = formatVideoLessonDuration(this.data.duration)
        }
    }
}

class ContentManager {
    static content = []
    static str_mappings = {
        'lesson': 'уроков',
        'test': 'тестов',
        'homework': 'дом. заданий', 
        'extra-file': 'доп. файлов'
    }
    static item_options = ['basic', 'extra', 'premium']

    static addToManager(item) {
        this.content.push(item)
    }

    static getItemsCount(type, option) {
        const slicedArr = this.item_options.slice(0, this.item_options.findIndex(el => el === option) + 1)
        let counter = 0
        slicedArr.forEach(option => counter += this.content.filter(item => item.type === type && item.option === option).length)
        return counter
    }

    static getElement(type, option) {
        let div = document.createElement('div')
        let svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        svg.classList.add('course-header-icon')
        let use = document.createElementNS('http://www.w3.org/2000/svg', 'use')
        use.setAttributeNS('http://www.w3.org/1999/xlink','href',`#icon-${type}`)
        svg.append(use)
        div.append(svg)
        let span = document.createElement('span')
        span.textContent = `${this.getItemsCount(type, option)} ${this.str_mappings[type]}`
        div.append(span)
        return div 
            // return this.getItemsCount(type, option) ? `<span>${this.getItemsCount(type, option)} ${this.str_mappings[type]}</span>` : '' 
    }

    static renderBuyElement(option) {
        let content = ''
        Object.keys(this.str_mappings).forEach(key => {
            content += this.getElement(key, option)
        })
        document.querySelector(`#buy-${option}-content`).innerHTML = content

    }

    static renderBuyElements() {
        this.item_options.forEach(type => this.renderBuyElement(type))
    }

    static renderSidemenuContent(option) {
        document.querySelector('#side-menu-options-content').innerHTML = ''
        Object.keys(this.str_mappings).forEach(type => {
            if (this.getItemsCount(type, option)) {
                document.querySelector('#side-menu-options-content').append(this.getElement(type, option))
            }
        })
    }
}



let player = videojs(document.querySelector('.video-js'))

let stripe = Stripe('pk_test_51McWQcDlPs5u4HwiXU90HVvWjuDJjOPFOoQV35sWS44HHELoefCrjSoHdRN4hRfoLfmsZkxSARDuRF4Q412znY0d00t6YkA4M7')

buyBtns = document.querySelectorAll('.buy-course')
buyBtns.forEach(buyBtn => {
    let option = buyBtn.id.split('-')[1]
    buyBtn.addEventListener('click', event => {
        fetch(`http://127.0.0.1:8000/api/courses/${courseId}/buy/${option}/`)
            .then(response => response.json())
            .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
    })
})



const videoDialog = document.querySelector('#dialog-video-player')
backdrop.addEventListener('click', event => {
    backdrop.classList.add('invisible')
    document.querySelector('dialog[open]').close()
    player.pause()
})


function initializePlayer(lessonPlaylist) {
    player.playlist(lessonPlaylist)
    player.playlist.autoadvance(0)
    player.on('playlistitem', () => {
        updatePlayerUI()
    })
}

function updatePlayerUI() {
    document.querySelector('.video-player-items').innerHTML = ''
    currentLesson = player.playlist.currentItem()
    sectionlessonsPlaylist = LessonManager.getSectionLessons(currentLesson)

    sectionlessonsPlaylist.forEach(lesson => {
        const clone = document.getElementById('template-video-player-ui-element').content.cloneNode(true)
        clone.querySelector('li').textContent = lesson.name
        clone.querySelector('li').addEventListener('click', event => player.playlist.currentItem(lesson.id))
        if (lesson.id === currentLesson) {
            clone.querySelector('li').classList.add('active')
        }
        document.querySelector('.video-player-items').append(clone)
    })
    
    const nextSectionBtn = document.querySelector('#video-player-ui-next-section')
    if (LessonManager.getNextSectionLesson(currentLesson) != undefined) {
        nextSectionBtn.classList.remove('invisible')
        nextSectionBtn.addEventListener('click', event => {
            player.playlist.currentItem(LessonManager.getNextSectionLesson(currentLesson).id)
    })}
    else {
        nextSectionBtn.classList.add('invisible')
    }

    const previousSectionBtn = document.querySelector('#video-player-ui-previous-section')
    if (LessonManager.getPreviousSectionLesson(currentLesson) != undefined) {
        previousSectionBtn.classList.remove('invisible')
        previousSectionBtn.addEventListener('click', event => {
            player.playlist.currentItem(LessonManager.getPreviousSectionLesson(currentLesson).id)
    })}
    else {
        previousSectionBtn.classList.add('invisible')
    }
}

function getCourseData() {
    fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))
}

function initializeHeader(data) {
    document.getElementById('course-name').textContent = data.name
    document.getElementById('course-short_description').textContent = data.short_description
    document.getElementById('course-date_updated').textContent = data.date_updated
    document.getElementById('course-language').textContent = data.language
}

function initializeWhatWillLearn(data) {
    data.what_will_learn.forEach(item => {
        const clone = document.getElementById('template-what_will_learn').content.cloneNode(true)
        clone.querySelector('span').textContent = item
        document.getElementById('what_will_learn-items').append(clone)
    })
}

function initializeVideoLessons(data) {
    let lessonCounter = 0
    data.sections.forEach((section, index) => {
        lessonArr = section.items.filter(item => item.type === 'lesson' && item.file)
        lessonArr.forEach(lesson => {
                    lessonObj = new Lesson(lessonCounter, lesson, index)
                    LessonManager.addLesson(lessonObj)
                    lessonCounter++
                }
    )})
    document.getElementById('course-content-info').textContent = `${data.sections.length} секций - ${lessonCounter} видеоуроков`
}

function initializeVideoLessonsLinks() {
    allLessonLinks = document.querySelectorAll('.lesson-link')
    allLessonLinks.forEach((lessonLink, index) => {
        lessonLink.addEventListener('click', event => {
            player.playlist.currentItem(index)
            backdrop.classList.remove('invisible')
            videoDialog.show()
            player.play()
        })
    })
}

function initizlizeRequirements(data) {
    data.requirements.forEach(requierement => {
        const clone = document.getElementById('template-requirements').content.cloneNode(true)
        clone.querySelector('li').textContent = requierement
        document.querySelector('#course-requirements ul').append(clone)
    })
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function initializeSidebar(data) {
    document.getElementById('side-menu-cover').src = data.cover
    document.getElementById('side-menu-price').textContent = data.price + '. руб.'
    data.options.forEach(element => {
        spanEl = `<span id="buy-${element.option}" data-option="${element.option}">${capitalizeFirstLetter(element.option)}</span>`
        document.getElementById('side-menu-options-header').innerHTML += spanEl
    })
    document.querySelectorAll('#side-menu-options-header span').forEach(option => option.addEventListener('click', event => {
        ContentManager.renderSidemenuContent(event.target.getAttribute('data-option'))
    }))
}

function initializePage(data) {
    document.getElementById('video-player-course-title').textContent = data.name
    document.getElementById('course-sections').innerHTML = ''
    initializeHeader(data)
    initializeWhatWillLearn(data)
    initializeVideoLessons(data)
    initializePlayer(LessonManager.lessonsPlaylist)

    data.sections.forEach(sectionData => {
        section = new Section(sectionData)
        section.createItems()
    })
    
    initializeVideoLessonsLinks()
    initizlizeRequirements(data)

    document.getElementById('course-full_description').innerHTML = data.full_description
    
    initializeSidebar(data)
    ContentManager.renderSidemenuContent('basic')

    // ContentManager.renderBuyElements()
}

// function expandSection(event) {
//     this.classList.toggle('invisible')
// }



// function createSection(section) {
//     const clone = document.getElementById('template-course-section').content.cloneNode(true)
//     // const sectionDiv = clone.querySelector('div.course-section')
//     clone.querySelector('span.section-name').textContent = section.name
//     // sectionDiv.setAttribute('section-id', section.id)
//     clone.querySelector('svg.section-header-icon-expand').addEventListener('click', expandSection.bind(clone.querySelector('div.course-section-body')))
    
//     // const filteredItems = section.items.filter(item => {
//     //     const optionIndex = courseOptions.findIndex(el => el === courseOption)
//     //     const slicedArr = courseOptions.slice(0, optionIndex + 1)
//     //     return slicedArr.includes(item.option)
//     // })
//     section.items.forEach(item => createItem(clone.querySelector('div.course-section'), item))
//     document.getElementById('course-sections').append(clone)
// }





// function createItem(section, item) {
//     const itemTemplate = document.getElementById('template-section-item')
//     const clone = itemTemplate.content.cloneNode(true)
//     clone.querySelector('.item-name').textContent = item.name
//     // clone.querySelector('.section-item').setAttribute('item-id', item.id)
//     // clone.querySelector('.section-item').setAttribute('item-type', item.type)
//     clone.querySelector('svg use').setAttribute('href', `#icon-${item.type}`)
//     if (item.type === 'lesson') {
//         clone.querySelector('.item-name').classList.add('lesson-link')
//     }
//     section.querySelector('.section-items').append(clone)
// }