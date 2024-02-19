export class Course {
    constructor (data) {
        this.slug = data.slug
        this.name = data.name
        this.description = data.short_description
        this.author = data.author
        this.cover = data.cover
        this.language = data.language
        this.price = data.price
        this.duration = data.duration
        this.options = data.options
        this.subject = data.subject
        this.rating = data.rating
        this.students = data.students
        this.element = this.renderElement()
    }

    createElement() {
        const clone = document.getElementById('template-course').content.cloneNode(true)
        clone.querySelector('.course-cover img').setAttribute('src', this.cover)
        clone.querySelector('.course-name').textContent = this.name
        clone.querySelector('.course-description').textContent = this.description
        clone.querySelector('.course-author').textContent = this.author.name
        clone.querySelector('.course-price').textContent = this.price + ' руб.'
        clone.querySelector('.course-student-count').textContent = this.students
        clone.querySelectorAll(`svg.review-star-small:nth-child(-n+${Math.round(this.rating)})`).forEach(star => star.classList.add('star-selected'))
        clone.querySelector('.course-rating-number').textContent = this.rating
        clone.querySelector('a').setAttribute('href', `/course/${this.slug}`)
        return clone
    }

    renderElement() {
        const section = document.getElementById('courses')
        section.append(this.createElement())
        return section.lastElementChild
    }
}