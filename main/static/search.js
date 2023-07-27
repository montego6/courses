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

document.querySelectorAll('.filter-choice input').forEach(filter => filter.addEventListener('change', event => {
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
        })


class Course {
    constructor (data) {
        this.name = data.name
        this.description = data.short_description
        this.author = data.author
        this.cover = data.cover
        this.language = data.language
        this.price = data.price
        this.duration = data.duration
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
        duration: []
    }

    static addCourse(course) {
        this.courses.push(course)
    }

    static filterCourses() {
        return DurationFilter.filter(this.courses, this.filters.duration)
    }

    static renderCourses() {
       let empty_filters = Object.values(this.filters).filter(arr => arr.length != 0)
        if (empty_filters.length) {
            document.getElementById('courses').innerHTML = ''
            this.filterCourses().forEach(course => course.renderElement())
        } else {
            document.getElementById('courses').innerHTML = ''
            this.courses.forEach(course => course.renderElement())
        }
    }
}

class DurationFilter {
    static filter(courses, filters) {
        if (filters) {
            let filteredArr = []
            filters.forEach(filter => {
                filteredArr.push(...courses.filter(course => filter.low < course.duration && course.duration < filter.high))
            })
            return filteredArr 
        } else {
            return courses
       }
    }
}


function renderCourses(data) {
    data.forEach(element => {
        let course = new Course(element)
        CourseManager.addCourse(course)
    });
    console.log(CourseManager.courses)
}
