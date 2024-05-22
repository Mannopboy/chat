let microphone = document.querySelector('.microphone'), add_contact = document.querySelector('.contacts__block_btn'),
    menu = document.querySelector('.menu'), overlay = document.querySelector('.overlay'),
    right_close = document.querySelector('.right_close'), texts = document.querySelector('.texts'),
    basic__msg = document.querySelector('.basic__msg'), basic__sender = document.querySelector('.basic__sender'),
    contact = document.querySelector('#contact'), form_block = document.querySelector('.basic__msg_block'),
    right_modal = document.querySelector('.right_modal'), app_icon = document.querySelector('.basic_header_icon'),
    msg_block = document.querySelectorAll('.not_seen'), contact_overlay = document.querySelector('#contact_overlay'),
    chat_user = document.querySelector('.chat_user'), chat_time = document.querySelector('.chat_time'), msg_list = [],
    camera = document.querySelector('#camera'), file_img = document.querySelector('#file_img'),
    contact_modal = document.querySelector('.contact'), contact_img = document.querySelector('.contact_img'),
    confirmation = document.querySelector('.confirmation'), clear_history = document.querySelector('.clear_history'),
    info_chat = document.querySelector('.info_chat'), type_delete = '', yes = document.querySelector('.yes'),
    delete_chat = document.querySelector('.delete_chat'),
    basic__msg_overlay = document.querySelector('.basic__msg_overlay'), no = document.querySelector('.no'),
    settings = document.querySelector('#settings'), text_msg = document.querySelector('.text_msg');
sessionStorage.setItem(`${texts.dataset.user}`, `${texts.dataset.user}`)
camera.addEventListener('click', () => {
    file_img.click()
})
file_img.addEventListener('change', () => {
    const [file] = file_img.files
    if (file) {
        contact_img.src = `${URL.createObjectURL(file)}`
    }
})
texts.addEventListener('click', (event) => {
    if (event.target === texts) {
        basic__msg_overlay.classList.remove('active')
    }
})
info_chat.addEventListener('click', function () {
    if (basic__msg_overlay.classList.contains('active')) {
        basic__msg_overlay.classList.remove('active')
    } else {
        basic__msg_overlay.classList.add('active')
    }

})
clear_history.addEventListener('click', () => {
    type_delete = 'clear_history'
    confirmation.classList.add('active')
})
delete_chat.addEventListener('click', () => {
    type_delete = "delete_chat"
    confirmation.classList.add('active')
})
no.addEventListener('click', () => {
    confirmation.classList.remove('active')
})
yes.addEventListener('click', function () {
    fetch('/delete_info/' + type_delete, {
        method: "DELETE", body: JSON.stringify({})
    })
})
confirmation.addEventListener('click', (event) => {
    if (event.target === confirmation) {
        confirmation.classList.remove('active')
    }
})
contact_modal.addEventListener('click', (event) => {
    if (event.target === contact_modal) {
        contact_modal.classList.remove('active')
        menu.classList.add('menu_active')
    }
})
settings.addEventListener('click', () => {
    contact_modal.classList.add('active')
    menu.classList.remove('menu_active')
})
right_close.addEventListener('click', () => {
    basic__sender.style.display = "none"
    basic__msg.style.width = "70%"
})
right_modal.addEventListener('click', () => {
    basic__sender.style.display = "block"
    basic__msg.style.width = "50%"
})
add_contact.addEventListener('click', () => {
    overlay.classList.add('active')
})
overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
        overlay.classList.remove('active')
    }
})
text_msg.addEventListener('input', () => {
    if (text_msg.value) {
        microphone.className = 'fa-regular fa-paper-plane plane fa-rotate-45 microphone'
    } else {
        microphone.className = 'fa-solid fa-microphone microphone plane'
    }
})
app_icon.addEventListener('click', () => {
    menu.classList.add('menu_active')
})
menu.addEventListener('click', (event) => {
    if (event.target === menu) {
        menu.classList.remove('menu_active')
    }
})
contact.addEventListener('click', () => {
    contact_overlay.classList.add('active')
    menu.classList.remove('menu_active')
})
contact_overlay.addEventListener('click', (event) => {
    if (event.target === contact_overlay) {
        contact_overlay.classList.remove('active')
        menu.classList.add('menu_active')
    }
})
checkVisible()
let viewHeight = Math.max(document.documentElement.clientHeight, window.innerHeight);

function checkVisible() {
    let msg_block = document.querySelectorAll('.not_seen'), socketio = io();
    if (msg_block.length !== 0) {
        msg_block.forEach(item => {
            let rect = item.getBoundingClientRect();
            let viewHeight = Math.max(document.documentElement.clientHeight, window.innerHeight);
            let status = !(rect.bottom < 0 || rect.top - viewHeight >= 0);
            if (status && item.dataset.status !== "True") {
                socketio.emit("message", {
                    data: {
                        username: texts.dataset.user,
                        msg_id: item.dataset.msg,
                        chat_id: text_msg.dataset.chat,
                        type: "check_status",
                    }
                })
            }
        })
    }
}

function checkScroll() {
    let msg_block = document.querySelectorAll('.not_seen');
    if (msg_block.length !== 0) {
        texts.addEventListener("scroll", () => {
            checkVisible()
        })
    }
}

checkScroll()

let socketio = io(), plane = document.querySelector('.plane');
socketio.on("message", (data) => {

})
const createMessage = (data) => {
    let class_name = '', icon = '';
    if (sessionStorage.getItem(`${texts.dataset.user}`) === data['info']['user']['username']) {
        class_name = 'basic__msg_infos user'
        icon = `<i class="fa-solid fa-check"></i>`
    } else {
        class_name = 'basic__msg_infos not_seen infos'
    }
    let content = ''
    if (data['info']['day']) {
        content = `
        <div class="basic__msg_data">${data['info']['day']}</div>     
        <div data-msg="${data['info']['id']}" class="${class_name}">
             <p class="text">${data['info']['text']}</p>
             <div class="text_data">
                <p class="text_clock">${data['info']['time']}</p>
                ${icon}
            </div>
         </div>
        `
    } else {
        content = `
        <div data-msg="${data['info']['id']}" class="${class_name}">
            <p class="text">${data['info']['text']}</p>
            <div class="text_data">
                <p class="text_clock">${data['info']['time']}</p>
                ${icon}
            </div>
        </div>
      `
    }
    texts.innerHTML += content
    texts.scrollTop = texts.clientHeight + texts.scrollHeight
    checkVisible()
    alert(true)
    checkScroll()
}

function updateMessage(data) {
    let user_msg = document.querySelector(`[data-msg="${data['msg_id']}"]`),
        text_data = user_msg.querySelector('.text_data'), checkboxes = user_msg.querySelectorAll('.fa-solid .fa-check');

    if (!user_msg.classList.contains("infos")) {
        text_data.innerHTML += `<i class="fa-solid fa-check"></i>`
    }
}

socketio.on("message", (data) => {
    console.log(data)
    console.log(data['type'])
    if (data['type'] === "create_msg") {
        createMessage(data)
    } else if (data['type'] === "check_status") {
        console.log('update')
        updateMessage(data)
    } else if (data['type'] === "connect") {
        if (sessionStorage.getItem(`${texts.dataset.user}`) !== data['username']) {
            chat_time.innerHTML = 'online'
        }
    } else if (data['type'] === "disconnect") {
        chat_time.innerHTML = data['time']
    }

})


const sendMessage = () => {
    if (text_msg.value === "") return;
    socketio.emit("message", {
        data: {
            msg: text_msg.value, chat_id: text_msg.dataset.chat, type: "create_msg"
        }
    })
    text_msg.value = ""
}
plane.addEventListener('click', () => {
    sendMessage()
})
window.addEventListener('keydown', (event) => {
    if (event.key === "Enter") {
        sendMessage()
    }
})

// Disconnect uchun
// window.onbeforeunload = function () {
//         socket.emit('client_disconnecting', {'username':localStorage.getItem('username')});
//     }