let url = new URL(document.location)
let params = url.searchParams;
// params.append('lang', 'eng')
// window.history.pushState({path: url.href}, '', url.href)

const DURATION_FILTER = {
    'duration-1': {low: 0, high: 60*60},
    'duration-2': {low: 60*60, high: 3*60*60},
    'duration-3': {low: 3*60*60, high: 6*60*60},
    'duration-4': {low: 6*60*60, high: 17*60*60},
    'duration-5': {low: 17*60*60, high: 5000*60*60},
}

document.querySelector('p').addEventListener('click', event => {
    document.getElementById('filters').classList.toggle('filters-move')
    document.getElementById('courses').classList.toggle('courses-expand')
})

document.querySelectorAll('#filter-duration .filter-choice input').forEach(filter => filter.addEventListener('change', event => {
    if (event.target.checked) {
        CourseManager.filters.duration.push(DURATION_FILTER[event.target.id])
    } else {
        let idx = CourseManager.filters.duration.findIndex(el => el === DURATION_FILTER[event.target.id])
        CourseManager.filters.duration.splice(idx, 1)
    }
    CourseManager.renderCourses()
}))


fetch('http://127.0.0.1:8000/api/courses/search/?' + params).then(response => response.json())
        .then(data => {
            console.log(data)
            renderCourses(data)
            LanguageManager.renderAllLanguages()
        })

let allLanguages
fetch('static/langmap.json').then(response => response.json()).then(data => allLanguages = data)


class Course {
    constructor (data) {
        this.name = data.name
        this.description = data.short_description
        this.author = data.author
        this.cover = data.cover
        this.language = data.language
        this.price = data.price
        this.duration = data.duration
        this.options = data.options
        this.element = this.renderElement()
    }

    createElement() {
        const clone = document.getElementById('template-course').content.cloneNode(true)
        clone.querySelector('.course-cover img').setAttribute('src', this.cover)
        clone.querySelector('.course-name').textContent = this.name
        clone.querySelector('.course-description').textContent = this.description
        clone.querySelector('.course-author').textContent = this.author
        clone.querySelector('.course-price').textContent = this.price
        return clone
    }

    renderElement() {
        const section = document.getElementById('courses')
        section.append(this.createElement())
        return section.lastElementChild
    }
}


class CourseManager {
    static courses = []

    static filters = {
        duration: [],
        language: []
    }

    static addCourse(course) {
        this.courses.push(course)
    }

    static filterCourses() {
        let filter = DurationFilter
        let courses = this.courses
        while (filter) {
            courses = filter.filter(courses, this.filters) 
            filter = filter.next()
        }
        return courses
    }

    static renderCourses() {
       let filtersContent = Object.values(this.filters).filter(arr => arr.length != 0)
        if (filtersContent.length) {
            document.getElementById('courses').innerHTML = ''
            this.filterCourses().forEach(course => course.renderElement())
        } else {
            document.getElementById('courses').innerHTML = ''
            this.courses.forEach(course => course.renderElement())
        }
    }
}

class DurationFilter {
    static filter(courses, filtersArr) {
        let filters = filtersArr.duration
        if (filters.length) {
            let filteredArr = []
            filters.forEach(filter => {
                filteredArr.push(...courses.filter(course => filter.low < course.duration && course.duration < filter.high))
            })
            return filteredArr 
        } else {
            return courses
       }
    }

    static next() {
        return LanguageFilter
    }
}

class LanguageFilter {
    static filter(courses, filtersArr) {
        let filters = filtersArr.language
        if (filters.length) {
            let filteredArr = []
            filters.forEach(filter => {
                filteredArr.push(...courses.filter(course => filter.includes(course.language)))
            })
            return filteredArr 
        } else {
            return courses
        }
    }

    static next() {
        return null
    }
}


class LanguageManager {
    static getDistinctLanguages() {
        let languagesArr = Array.from(CourseManager.courses, course => course.language)
        let languagesSet = new Set(languagesArr)
        return languagesSet
    }

    static getLanguageElement(language) {
        const clone = document.getElementById('template-filter-language').content.cloneNode(true)
        clone.querySelector('input').id = 'language-' + language
        clone.querySelector('label').setAttribute('for', 'language-' + language)
        clone.querySelector('label').textContent = allLanguages[language]
        return clone
    }

    static renderLanguageElement(element) {
        document.querySelector('#filter-language .filter-body').append(element)
    }

    static renderAllLanguages() {
        let allLanguages = this.getDistinctLanguages()
        allLanguages.forEach(language => {
            const element = this.getLanguageElement(language)
            this.renderLanguageElement(element)
        })
        this.setEventListeners()
    }

    static setEventListeners() {
        document.querySelectorAll('#filter-language .filter-choice input').forEach(filter => filter.addEventListener('change', event => {
            if (event.target.checked) {
                CourseManager.filters.language.push(event.target.id.split('-')[1])
            } else {
                let idx = CourseManager.filters.language.findIndex(el => el === event.target.id.split('-')[1])
                CourseManager.filters.language.splice(idx, 1)
            }
            CourseManager.renderCourses()
        }))
    }
}


class OptionsManager {
    static getDistinctOptions() {
        let optionsArr = Array.from(CourseManager.courses, course => course.options)
        console.log(optionsArr)
        optionsArr = optionsArr.flat()
        let optionsSet = new Set(optionsArr)
        console.log(optionsSet)
        return optionsSet
    }

    static getOptionElement(option) {
        const clone = document.getElementById('template-filter-language').content.cloneNode(true)
        clone.querySelector('input').id = 'language-' + language
        clone.querySelector('label').setAttribute('for', 'language-' + language)
        clone.querySelector('label').textContent = allLanguages[language]
        return clone
    }
}



function renderCourses(data) {
    data.forEach(element => {
        let course = new Course(element)
        CourseManager.addCourse(course)
    });
    OptionsManager.getDistinctOptions()
}
