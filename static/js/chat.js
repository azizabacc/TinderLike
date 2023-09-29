console.log('hello')
function resetTextarea() {
    document.getElementById('message').value = '';
}
const editButtons = document.querySelectorAll('.edit-button');
const editTextareas = document.querySelectorAll('.edit-form');

editButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
        editTextareas[index].classList.remove('hidden');
});
});

let messages = document.querySelectorAll(".message")
let id_user = document.querySelector('.chat-messages')
console.log(id_user.id)
messages.forEach((message)=>{
    console.log(message.id)
    if(message.id===id_user.id){
        message.classList.toggle('sent')
    }else{
        message.classList.toggle('received')

    }
})

