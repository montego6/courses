class CategoriesStats {
    block = document.querySelector('#stats')
    
    constructor(data) {
        this.id = data.id
        this.name = data.name
        this.courses = data.courses
        this.authors = data.authors
        this.students = data.students
        this.payments = data.payments
        this.curMonthPayments = data.cur_month_payments
    }

    createElement() {
        const clone = document.querySelector('#template-stats').content.cloneNode(true)
        clone.querySelector('.cat-id').textContent = this.id
        clone.querySelector('.cat-name').textContent = this.name
        clone.querySelector('.cat-name').setAttribute('href', `/statistic/subcategories/by_category/${this.id}`)
        clone.querySelector('.cat-courses').textContent = this.courses
        clone.querySelector('.cat-authors').textContent = this.authors
        clone.querySelector('.cat-students').textContent = this.students
        clone.querySelector('.cat-payments').textContent = this.payments
        clone.querySelector('.cat-month-payments').textContent = this.curMonthPayments
        return clone
    }

    renderElement() {
        this.block.append(this.createElement())
    }
}


function getStatisticsData() {
    fetch(`/api/categories/statistics/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    data.forEach(catStat => {
        let catStatObj = new CategoriesStats(catStat)
        catStatObj.renderElement()
    });
}

getStatisticsData()