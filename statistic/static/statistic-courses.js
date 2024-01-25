class CourseStats {
    block = document.querySelector('#stats')
    
    constructor(data) {
        this.id = data.id
        this.name = data.name
        this.reviews = data.num_reviews
        this.rating = data.rating
        this.students = data.num_students
        this.payments = data.total_payments
        this.curMonthPayments = data.cur_month_payments
    }

    createElement() {
        const clone = document.querySelector('#template-stats').content.cloneNode(true)
        clone.querySelector('.course-id').textContent = this.id
        clone.querySelector('.course-name').textContent = this.name
        clone.querySelector('.course-name').setAttribute('href', `/statistic/subjects/by_subcategory/${this.id}/`)
        clone.querySelector('.course-reviews').textContent = this.reviews
        clone.querySelector('.course-rating').textContent = this.rating
        clone.querySelector('.course-students').textContent = this.students
        clone.querySelector('.course-payments').textContent = this.payments
        clone.querySelector('.course-month-payments').textContent = this.curMonthPayments
        return clone
    }

    renderElement() {
        this.block.append(this.createElement())
    }
}


function getStatisticsData() {
    const subjectId = document.querySelector('#subject-id').textContent
    fetch(`/api/courses/by_subject/${subjectId}/statistics/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    console.log(data)
    data.forEach(courseStat => {
        let courseStatObj = new CourseStats(courseStat)
        courseStatObj.renderElement()
    });
}

getStatisticsData()