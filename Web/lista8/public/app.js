const socket = io()
console.log("Loading app.js...");

const messageForm = document.getElementById('messageForm')
const messageInput = document.getElementById('message')
const messages = document.getElementById('messages')
const chatArea = document.getElementById('chatArea')
const roomList = document.getElementById('roomList')

let username = ''
let currentRoom = ''

function formatISOtoCustom(isoDate) {
    const date = new Date(isoDate);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} - ${hours}:${minutes}:${seconds}`;
}


messageInput.addEventListener('keypress', () => {
    socket.emit('activity', username)
})

const quitButton = document.getElementById('quit-button')
quitButton.addEventListener('click', () => {
    socket.emit('leaveRoom', { username: username, room: currentRoom })
    chatArea.classList.add('hidden')
    messages.innerHTML = ''
    roomList.innerHTML = ''
    currentRoom = ''
    username = ''
    document.getElementById('greeting').classList.remove('hidden')
    document.getElementById('userListContainer').classList.add('hidden')
    document.getElementById('quit-button').classList.add('hidden')
    console.log('User left room:', username, currentRoom);
}
)

socket.on('roomList', rooms => {
    roomList.innerHTML = ''
    rooms.forEach(room => {
        const li = document.createElement('li')
        li.textContent = room.name + ' - ' + room.owner + ' Users:' + room.users
        li.classList.add('room')
        li.addEventListener('click', () => {
            if (room.id === currentRoom) return


            new_username = prompt("Enter your nickname:")
            if (!new_username) return

            if (currentRoom) {
                socket.emit('leaveRoom', { username: username, room: currentRoom })
                messages.innerHTML = ''
            }
            document.getElementById('greeting').classList.add('hidden')
            currentRoom = room.id
            console.log('Current room:', room.id)
            socket.emit('joinRoom', { username: new_username, room: room.id })
            chatArea.classList.remove('hidden')
            document.getElementById('userListContainer').classList.remove('hidden')
            document.getElementById('quit-button').classList.remove('hidden')
            username = new_username
        })
        roomList.appendChild(li)
    })
})

socket.on('message', (message, sound) => {
    const li = document.createElement('li')
    li.className = 'post'

    if (message.sender_id === socket.id) li.classList.add('post--right')
    else if (message.sender_id !== 'Admin') li.classList.add('post--left')
    if (message.sender_id !== 'Admin') {
        li.innerHTML = `<div class="post__header ${message.sender_id == socket.id
            ? 'post__header--user'
            : 'post__header--reply'}">
            <span class="post__header--name">${message.sender_id == socket.id ? 'Me' : message.sender}</span> 
            <span class="post__header--time">${formatISOtoCustom(message.time)}</span> 
            </div>
            <div class="post__text message-image" style="display: grid">${message.text} ${message.picture ? `<img src=data:image/png;base64,${message.picture}>` : ""} ${message.sound ? `<audio controls src=data:audio/mpeg;base64,${message.sound}>` : ""}</div>`

    } else {
        li.innerHTML = `<div class="post__text">${message.text}</div>`
    }
    if(message.sender_id !== socket.id && message.sender_id !== 'Admin' && sound !== false){
        const audio = new Audio('notification.mp3');
        audio.play();
        const title = document.title;
        document.title = `New message from ${message.sender}`;
        setTimeout(() => {
            document.title = title;
        }, 3000);
    }

    messages.appendChild(li)
    messages.scrollTop = messages.scrollHeight
})

const activity = document.querySelector('.activity');
let activityTimer
socket.on("activity", (name) => {
    activity.textContent = `${name} is typing...`
    clearTimeout(activityTimer)
    activityTimer = setTimeout(() => {
        activity.textContent = ""
    }, 3000)
})

socket.on('userList', users => {
    const userList = document.getElementById('userList')
    userList.innerHTML = ''
    users.forEach(user => {
        const li = document.createElement('li')
        li.textContent = user
        userList.appendChild(li)
    })
}
)

socket.on("createRoom", (id) => {
    new_username = prompt("Enter your nickname:")
    if (!new_username) return

    if (currentRoom) {
        socket.emit('leaveRoom', { username: username, room: currentRoom })
        messages.innerHTML = ''
    }
    document.getElementById('greeting').classList.add('hidden')
    currentRoom = id
    socket.emit('joinRoom', { username: new_username, room: id })
    chatArea.classList.remove('hidden')
    document.getElementById('userListContainer').classList.add('hidden')
    document.getElementById('quit-button').classList.add('hidden')
    username = new_username
})

const fileInput = document.getElementById('Attachment');
const fileErrorDiv = document.getElementById('fileError');
const maxFileSizeMB = 2;
const allowedExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.mp3'];
const allowedMimeTypes = ['image/png', 'image/jpeg', 'image/gif', 'audio/mpeg'];

document.getElementById('messageForm').addEventListener('submit', e => {
    e.preventDefault()
    console.log(socket.id);

    const text = messageInput.value
    fileErrorDiv.textContent = '';
    const selectedFile = fileInput.files[0];

    if (selectedFile) {
        const fileSizeMB = selectedFile.size / (1024 * 1024);
        const fileName = selectedFile.name.toLowerCase();
        const fileExtension = fileName.substring(fileName.lastIndexOf('.'));
        const fileMimeType = selectedFile.type;

        if (!allowedMimeTypes.includes(fileMimeType)) {
            fileErrorDiv.textContent = `Allowed are only: ${allowedExtensions.join(', ')}. Choosen: ${fileMimeType}`;
            e.preventDefault();
            return;
        }

        if (!allowedExtensions.includes(fileExtension)) {
            fileErrorDiv.textContent = `Allwoed are only: ${allowedExtensions.join(', ')}. Choosen: ${fileExtension}`;
            e.preventDefault();
            return;
        }

        if (fileSizeMB > maxFileSizeMB) {
            fileErrorDiv.textContent = `Maximum size ${maxFileSizeMB}MB. Choosen: ${fileSizeMB.toFixed(2)}MB`;
            e.preventDefault();
            return;
        }
    }
    if (text || selectedFile) {
        if (text.length > 1000) {
            fileErrorDiv.textContent = `Message is too long. Maximum length is 1000 characters.`;
            e.preventDefault();
            return;
        }
        if (selectedFile) {
            const fileName = selectedFile.name.toLowerCase();
            const fileExtension = fileName.substring(fileName.lastIndexOf('.'));
            const fileMimeType = selectedFile.type;
            const reader = new FileReader();
            reader.onload = function (event) {
                
                const base64String = event.target.result.split(',')[1];

                if (fileMimeType === 'audio/mpeg' && fileExtension === '.mp3') {
                    socket.emit('message', { name: username, text: text || "" , picture : null,sound: base64String });
                }else{
                    socket.emit('message', { name: username, text: text || "" , picture: base64String });
                }
                messageInput.value = ''
                fileInput.value = '';
            };
            reader.readAsDataURL(selectedFile);
        } else {
            socket.emit('message', { name: username, text });
            messageInput.value = ''
        }
    }
})



var modal = document.getElementById("popup");
var btn = document.getElementById("createRoomButton");
const form = document.getElementById("createRoomForm");
btn.onclick = function () {
    modal.style.display = "block";
}
var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
    modal.style.display = "none";
}
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
        console.log("close");
    }
}
form.addEventListener('submit', (e) => {
    const roomName = document.getElementById('roomName').value;
    const roomOwner = username ? username : "Anonymous"; 
    socket.emit('createRoom', { roomname: roomName, ownername: roomOwner });
    modal.style.display = "none";
})
