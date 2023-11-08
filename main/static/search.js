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

const optionsMap = {
    'lesson': 'Уроки',
    'test': 'Тесты',
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
            OptionsManager.renderAllOptions()
            PricesManager.renderAllPrices()
            SubjectsManager.renderAllSubjects()
            RatingsManager.renderAllRatings()
            initializePage()
        })

let allLanguages
fetch('static/langmap.json').then(response => response.json()).then(data => allLanguages = data)


function initializePage() {
    document.querySelectorAll('.filter-header svg').forEach(expandIcon => expandIcon.addEventListener('click', event => {
        event.target.closest('div.filter-option').querySelector('.filter-body').classList.toggle('invisible')
    }))
}

class Course {
    constructor (data) {
        this.id = data.id
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
        clone.querySelector('a').setAttribute('href', `http://127.0.0.1:8000/course/${this.id}`)
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
        language: [],
        options: [],
        prices: [],
        subjects: [],
        ratings: [],
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
        return OptionsFilter
    }
}

class OptionsFilter {
    static filter(courses, filtersArr) {
        let filters = filtersArr.options
        if (filters.length) {
            let filteredArr = []
            filters.forEach(filter => {
                let filteredCourses = courses.filter(course => course.options.includes(filter))
                filteredCourses.forEach(course => {
                    if (!filteredArr.includes(course)) {
                        filteredArr.push(course)
                    }
                })
            })
            return filteredArr
        } else {
            return courses
        }
    }

    static next() {
        return PricesFilter
    }
}

class PricesFilter {
    static filter(courses, filtersArr) {
        let filters = filtersArr.prices
        if (filters.length) {
            let filteredArr = []
            filters.forEach(filter => {
                let filteredCourses = courses.filter(course => course.price > filter)
                filteredCourses.forEach(course => {
                    if (!filteredArr.includes(course)) {
                        filteredArr.push(course)
                    }
                })
            })
            return filteredArr
        } else {
            return courses
        }
    }

    static next() {
        return SubjectsFilter
    }
}

class SubjectsFilter {
    static filter(courses, filtersArr) {
        let filters = filtersArr.subjects
        if (filters.length) {
            let filteredArr = []
            filters.forEach(filter => {
                let filteredCourses = courses.filter(course => course.subject == filter)
                filteredCourses.forEach(course => {
                    if (!filteredArr.includes(course)) {
                        filteredArr.push(course)
                    }
                })
            })
            return filteredArr
        } else {
            return courses
        }
    }

    static next() {
        return RatingFilter
    }
}

class RatingFilter {
    static filter(courses, filtersArr) {
        let filters = filtersArr.ratings
        if (filters.length) {
            let filteredArr = []
            filters.forEach(filter => {
                let filteredCourses = courses.filter(course => course.rating >= filter)
                filteredCourses.forEach(course => {
                    if (!filteredArr.includes(course)) {
                        filteredArr.push(course)
                    }
                })
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
        optionsArr = optionsArr.flat()
        let optionsSet = new Set(optionsArr)
        return optionsSet
    }

    static getOptionElement(option) {
        const clone = document.getElementById('template-filter-option').content.cloneNode(true)
        clone.querySelector('input').id = 'option-' + option
        clone.querySelector('label').setAttribute('for', 'option-' + option)
        clone.querySelector('label').textContent = optionsMap[option]
        return clone
    }

    static renderOptionElement(element) {
        document.querySelector('#filter-options .filter-body').append(element)
    }

    static renderAllOptions() {
        let options = this.getDistinctOptions() 
        document.querySelector('#filter-options .filter-body').innerHTML = ''
        options.forEach(option => this.renderOptionElement(this.getOptionElement(option)))
        this.setEventListeners()
    }

    static setEventListeners() {
        document.querySelectorAll('#filter-options input').forEach(input => input.addEventListener('change', event => {
            let element = event.target
            if (element.checked) {
                CourseManager.filters.options.push(element.id.split('-')[1])
            } else {
                let idx = CourseManager.filters.options.findIndex(el => el === element.id.split('-')[1])
                CourseManager.filters.options.splice(idx, 1)
            }
            CourseManager.renderCourses()
        }))
    }
}

class PricesManager {
    static pricesRanges = [0, 1000, 2000, 3000, 5000]
    
    static getDistinctPrices() {
        let pricesArr = Array.from(CourseManager.courses, course => course.price)
        let pricesRanges = []
        for (let price of pricesArr) {
            let idx = this.pricesRanges.length - 1
            while (price < this.pricesRanges[idx]) {
                idx--
            }
            pricesRanges.push(this.pricesRanges[idx])
        }
        let pricesSet = new Set(pricesRanges)
        return pricesSet
    }

    static getPriceElement(price) {
        const clone = document.getElementById('template-filter-price').content.cloneNode(true)
        clone.querySelector('input').id = 'price-' + price
        clone.querySelector('label').setAttribute('for', 'price-' + price)
        clone.querySelector('label').textContent = price + '+'
        return clone
    }

    static renderPriceElement(element) {
        document.querySelector('#filter-prices .filter-body').append(element)
    }

    static renderAllPrices() {
        let prices = this.getDistinctPrices()
        console.log('prices', prices)
        document.querySelector('#filter-prices .filter-body').innerHTML = ''
        prices.forEach(price => this.renderPriceElement(this.getPriceElement(price)))
        this.setEventListeners()
    }

    static setEventListeners() {
        document.querySelectorAll('#filter-prices input').forEach(input => input.addEventListener('change', event => {
            let element = event.target
            if (element.checked) {
                CourseManager.filters.prices.push(element.id.split('-')[1])
            } else {
                let idx = CourseManager.filters.prices.findIndex(el => el === element.id.split('-')[1])
                CourseManager.filters.prices.splice(idx, 1)
            }
            CourseManager.renderCourses()
        }))
    }
}

class SubjectsManager {
    static getDistinctSubjects() {
        let subjectsArr = Array.from(CourseManager.courses, course => course.subject)
        let subjectsSet = new Set(subjectsArr)
        return subjectsSet
    }

    static getSubjectElement(subject) {
        const clone = document.getElementById('template-filter-subject').content.cloneNode(true)
        clone.querySelector('input').id = 'subject-' + subject
        clone.querySelector('label').setAttribute('for', 'subject-' + subject)
        clone.querySelector('label').textContent = subject
        return clone
    }

    static renderSubjectElement(element) {
        document.querySelector('#filter-subjects .filter-body').append(element)
    }

    static renderAllSubjects() {
        let subjects = this.getDistinctSubjects()
        document.querySelector('#filter-subjects .filter-body').innerHTML = ''
        subjects.forEach(subject => this.renderSubjectElement(this.getSubjectElement(subject)))
        this.setEventListeners()
    }

    static setEventListeners() {
        document.querySelectorAll('#filter-subjects input').forEach(input => input.addEventListener('change', event => {
            let element = event.target
            if (element.checked) {
                CourseManager.filters.subjects.push(element.id.split('-')[1])
            } else {
                let idx = CourseManager.filters.subjects.findIndex(el => el === element.id.split('-')[1])
                CourseManager.filters.subjects.splice(idx, 1)
            }
            CourseManager.renderCourses()
        }))
    }
}


class RatingsManager {
    static ratings = [0, 1, 2, 3, 4, 5]

    static getDistinctRatings() {
        let ratingsArr = Array.from(CourseManager.courses, course => course.rating)
        let ratingsRanges = []
        for (let rating of ratingsArr) {
            let idx = this.ratings.length - 1
            while (rating < this.ratings[idx]) {
                idx--
            }
            ratingsRanges.push(this.ratings[idx])
        }
        let ratingsSet = new Set(ratingsRanges)
        return ratingsSet
    }


    static getRatingElement(rating) {
        const clone = document.getElementById('template-filter-rating').content.cloneNode(true)
        clone.querySelector('input').id = 'rating-' + rating
        clone.querySelector('label').setAttribute('for', 'rating-' + rating)
        clone.querySelector('label').textContent = rating + '+'
        return clone
    }

    static renderRatingElement(element) {
        document.querySelector('#filter-ratings .filter-body').append(element)
    }

    static renderAllRatings() {
        let ratings = this.getDistinctRatings()
        document.querySelector('#filter-ratings .filter-body').innerHTML = ''
        ratings.forEach(rating => this.renderRatingElement(this.getRatingElement(rating)))
        this.setEventListeners()
    }

    static setEventListeners() {
        document.querySelectorAll('#filter-ratings input').forEach(input => input.addEventListener('change', event => {
            let element = event.target
            if (element.checked) {
                CourseManager.filters.ratings.push(element.id.split('-')[1])
            } else {
                let idx = CourseManager.filters.ratings.findIndex(el => el === element.id.split('-')[1])
                CourseManager.filters.ratings.splice(idx, 1)
            }
            CourseManager.renderCourses()
        }))
    }
}


function renderCourses(data) {
    data.forEach(element => {
        let course = new Course(element)
        CourseManager.addCourse(course)
    });
}
