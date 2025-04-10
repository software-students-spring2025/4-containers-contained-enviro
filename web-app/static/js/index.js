document.addEventListener('DOMContentLoaded',(evt) => {
    console.log("Hello world")
    const record_btn = document.querySelector('.record-btn')
    const expand_btn = document.querySelector('.expand-btn')
    record_btn.id = 'stop-recording'
    record_btn.addEventListener('click',(evt) => {
        console.log("clicked button!")
        if (record_btn.id == 'stop-recording') {
            record_btn.innerHTML = '<ion-icon name="pause-outline"></ion-icon>'
            record_btn.id = 'start-recording'
            expand_btn.id = 'start-expand'
        } else {
            record_btn.innerHTML = '<ion-icon name="mic-outline"></ion-icon>'
            record_btn.id = 'stop-recording'
            expand_btn.id = 'stop-expand'
        }
    })
})