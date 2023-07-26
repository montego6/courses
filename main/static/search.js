// const url = window.location.href
let url = new URL(document.location)
let params = url.searchParams;
params.append('lang', 'eng')
window.history.pushState({path: url.href}, '', url.href)