class SubjectStats {
    block = document.querySelector('#stats')
    
    constructor(data) {
        this.id = data.id
        this.name = data.name
        this.courses = data.courses_num
        this.authors = data.authors
        this.students = data.students
        this.payments = data.payments
        this.curMonthPayments = data.cur_month_payments
    }

    createElement() {
        const clone = document.querySelector('#template-stats').content.cloneNode(true)
        clone.querySelector('.subject-id').textContent = this.id
        clone.querySelector('.subject-name').textContent = this.name
        clone.querySelector('.subject-name').setAttribute('href', `http://127.0.0.1:8000/statistic/subjects/by_subcategory/${this.id}/`)
        clone.querySelector('.subject-courses').textContent = this.courses
        clone.querySelector('.subject-authors').textContent = this.authors
        clone.querySelector('.subject-students').textContent = this.students
        clone.querySelector('.subject-payments').textContent = this.payments
        clone.querySelector('.subject-month-payments').textContent = this.curMonthPayments
        return clone
    }

    renderElement() {
        this.block.append(this.createElement())
    }
}


function getStatisticsData() {
    const subCatId = document.querySelector('#subcat-id').textContent
    fetch(`http://127.0.0.1:8000/api/subjects/by_subcategory/${subCatId}/statistics/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    data.forEach(subjStat => {
        let subjStatObj = new SubjectStats(subjStat)
        subjStatObj.renderElement()
    });
}

getStatisticsData()