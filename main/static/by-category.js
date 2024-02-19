import { Course } from './course.js'


let categoryId = document.querySelector('#category-id').textContent

const COURSES_PER_PAGE = 10


fetch(`/api/courses/by_category/${categoryId}/`).then(response => response.json()).then(data => initializeCourses(data, 1))
fetch(`/api/categories/${categoryId}/`).then(response => response.json()).then(data => {
    document.querySelector('#subject-name').textContent = data.name
})

function initializeCourses(data, page) {
    let params = new URLSearchParams(window.location.search)
    if (params.has('page')) {
        page = params.get('page')
    } 
    console.log(page)
    let slicedData = data.slice((page-1)* COURSES_PER_PAGE, page*COURSES_PER_PAGE) 
    slicedData.forEach(element => {
        new Course(element)
    });
    let pages = Math.ceil(data.length / COURSES_PER_PAGE)
    if (pages <= 3) {
        for (let i=1; i <= pages; i++) {
            let paging = document.createElement('a')
            paging.textContent = i
            paging.setAttribute('href', `/courses/by_category/${categoryId}?page=${i}`)
            document.querySelector('#paging').append(paging)
        }
        
    } else {
        for (let i=1; i < 4; i++) {
            let paging = document.createElement('a')
            paging.textContent = i
            paging.setAttribute('href', `/courses/by_category/${categoryId}?page=${i}`)
            document.querySelector('#paging').append(paging)
        }

        let dots = document.createElement('span')
        dots.textContent = '...'
        document.querySelector('#paging').append(paging)

        for (let i=pages - 3; i <= pages; i++) {
            let paging = document.createElement('a')
            paging.textContent = i
            paging.setAttribute('href', `/courses/by_category/${categoryId}?page=${i}`)
            document.querySelector('#paging').append(paging)
        }

    }
}