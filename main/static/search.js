let url = new URL(document.location)
let params = url.searchParams;
// params.append('lang', 'eng')
// window.history.pushState({path: url.href}, '', url.href)

document.querySelector('p').addEventListener('click', event => {
    document.getElementById('test1').classList.toggle('test1-move')
    document.getElementById('test2').classList.toggle('test2-expand')
})

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
        const section = document.getElementById('test2')
        section.append(this.createElement())
        return section.lastElementChild
    }
}


class CourseManager {
    static courses = []

    static addCourse(course) {
        this.courses.push(course)
    }
}


function renderCourses(data) {
    data.forEach(element => {
        let course = new Course(element)
        CourseManager.addCourse(course)
    });
    console.log(CourseManager.courses)
}
