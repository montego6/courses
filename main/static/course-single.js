const courseId = document.getElementById('course-id').textContent

getCourseData()


let player = videojs(document.querySelector('.video-js'))
let firstLessonInEachSection = []

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
    currentSectionIndex = firstLessonInEachSection.findLastIndex(lessonIndex => lessonIndex <= currentLesson)
    lessonPlaylist = player.playlist()
    nextSectionLesson = firstLessonInEachSection[currentSectionIndex + 1] || firstLessonInEachSection[currentSectionIndex] + 1
    prevSectionLesson = firstLessonInEachSection[currentSectionIndex - 1] || firstLessonInEachSection[currentSectionIndex] - 1
    lessonsSectionPlaylist =  lessonPlaylist.filter(lesson => (lesson.playlistItemId_ - 1 < nextSectionLesson) &&
                                                              (lesson.playlistItemId_ - 1 > prevSectionLesson))
    
    lessonsSectionPlaylist.forEach(lesson => {
        const clone = document.getElementById('template-video-player-ui-element').content.cloneNode(true)
        clone.querySelector('li').textContent = lesson.name
        clone.querySelector('li').setAttribute('playlist-id', lesson.playlistItemId_ - 1)
        clone.querySelector('li').addEventListener('click', event => {
            player.playlist.currentItem(Number(event.target.getAttribute('playlist-id')))
        })
        if (lesson.playlistItemId_ - 1 === currentLesson) {
            clone.querySelector('li').classList.add('active')
        }
        document.querySelector('.video-player-items').append(clone)
    })
    
    if (currentSectionIndex < firstLessonInEachSection.length - 1) {
        document.querySelector('#video-player-ui-next-section').classList.remove('invisible')
        document.querySelector('#video-player-ui-next-section').addEventListener('click', event => {
            player.playlist.currentItem(firstLessonInEachSection[currentSectionIndex + 1])
        })
    }   else {
        document.querySelector('#video-player-ui-next-section').classList.add('invisible')
    }

    if (currentSectionIndex > 0) {
        document.querySelector('#video-player-ui-previous-section').classList.remove('invisible')
        document.querySelector('#video-player-ui-previous-section').addEventListener('click', event => {
            player.playlist.currentItem(firstLessonInEachSection[currentSectionIndex - 1])
        })
    }   else {
        document.querySelector('#video-player-ui-previous-section').classList.add('invisible')
    }

}

function getCourseData() {
    fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {

    document.getElementById('video-player-course-title').textContent = data.name

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
    let lessonPlaylist = []
    data.sections.forEach(section => {
        lessonArr = section.items.filter(item => item.type === 'lesson')
        if (lessonArr.length) {
            firstLessonInEachSection.push(lessonCounter)
        }
        lessonArr.forEach(lesson => {
            playlistElement = {
                name: lesson.name,
                sources: [{
                    src: lesson.file,
                    type: 'video/mp4'
                }]
            }
            lessonPlaylist.push(playlistElement)
            lessonCounter++
        })
    })
    initializePlayer(lessonPlaylist)
    
    document.getElementById('course-content-info').textContent = `${data.sections.length} секций - ${lessonCounter} видеоуроков`
    
    data.sections.forEach(section => createSection(section))
    
    allLessonLinks = document.querySelectorAll('.lesson-link')
    allLessonLinks.forEach((lessonLink, index) => {
        lessonLink.addEventListener('click', event => {
            player.playlist.currentItem(index)
            backdrop.classList.remove('invisible')
            videoDialog.show()
            player.play()
        })
    })

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
    if (item.type === 'lesson') {
        clone.querySelector('.item-name').classList.add('lesson-link')
    }
    section.querySelector('.section-items').append(clone)
}