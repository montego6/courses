class SubCategoriesStats {
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
        clone.querySelector('.subcat-id').textContent = this.id
        clone.querySelector('.subcat-name').textContent = this.name
        clone.querySelector('.subcat-name').setAttribute('href', `http://127.0.0.1:8000/statistic/subjects/by_subcategory/${this.id}/`)
        clone.querySelector('.subcat-courses').textContent = this.courses
        clone.querySelector('.subcat-authors').textContent = this.authors
        clone.querySelector('.subcat-students').textContent = this.students
        clone.querySelector('.subcat-payments').textContent = this.payments
        clone.querySelector('.subcat-month-payments').textContent = this.curMonthPayments
        return clone
    }

    renderElement() {
        this.block.append(this.createElement())
    }
}


function getStatisticsData() {
    const catId = document.querySelector('#cat-id').textContent
    fetch(`http://127.0.0.1:8000/api/subcategories/by_category/${catId}/statistics/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    data.forEach(subCatStat => {
        let subCatStatObj = new SubCategoriesStats(subCatStat)
        subCatStatObj.renderElement()
    });
}

getStatisticsData()