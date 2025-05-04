import express from 'express';
import { Server } from 'socket.io';
import http from 'http';
import path from 'path';
import { fileURLToPath } from 'url';
import { Chat, Message } from './server_dep.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const io = new Server(server, {maxHttpBufferSize: 1e7});

app.use(express.static(path.join(__dirname, 'public')));

const users = [];
const rooms = [];
rooms.push(new Chat('General', 'General', 'Admin'));
rooms.push(new Chat('General2', 'General2', 'Admin2'));


function generateGUID() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}

io.on('connection', (socket) => {
    io.emit('roomList', rooms.map(room => room));

    socket.on('joinRoom', ({ username, room }) => {
        const user = users.find(u => socket.id === u.id);
        const roomExists = rooms.find(r => r.id === room);

        if (!user) {
            users.push({ id: socket.id, username: username, room: room });
            const newUser = users.find(u => socket.id === u.id);
            const newRoom = rooms.find(r => r.id === newUser.room);
            if (newRoom) {
                newRoom.users = (newRoom.users || 0) + 1;
            }
        } else {
            if (user.username === username && user.room === room) {
                return;
            }

            const prevRoom = rooms.find(r => r.id === user.room);
            if (prevRoom && prevRoom.users > 0) {
                prevRoom.users--;
            }

            socket.leave(user.room);
            user.username = username;
            user.room = room;

            const newRoom = rooms.find(r => r.id === user.room);
            if (newRoom) newRoom.users = (newRoom.users || 0) + 1;
        }

        socket.join(room);

        for(const mess in roomExists.messages){
            socket.emit('message', roomExists.messages[mess], false);
            console.log('Message:', roomExists.messages[mess]);
        }

        socket.emit('message', new Message('Admin', 'Admin', `User ${username} joined chat`, null));
        roomExists.messages.push(new Message('Admin', 'Admin', `User ${username} joined chat`, null));

        socket.broadcast.to(room).emit('message', new Message('Admin', 'Admin', `User ${username} joined chat`, null));

        io.to(room).emit('userList', getUsersInRoom(room));
        io.emit('roomList', rooms.map(room => room));
    });

    socket.on('leaveRoom', ({ username, room }) => {
        console.log('User left room:', username, room);
        const user = users.find(u => socket.id === u.id);
        if (user) {
            const prevRoom = rooms.find(r => r.id === user.room);
            if (prevRoom && prevRoom.users > 0) {
                prevRoom.users--;
            }
            users.splice(users.indexOf(user), 1);
            socket.leave(room);
            io.to(room).emit('message', new Message('Admin', 'Admin', `${username} left`, null));
            const room = rooms.find(r => r.id === user.room);
            room.messages.push(new Message('Admin', 'Admin', `${username} left`, null));
            io.to(room).emit('userList', getUsersInRoom(room));
        }
        io.emit('roomList', rooms.map(room => room));
    });

    socket.on('message', ({ name, text, picture, sound }) => {
        const user = users.find(u => u.id === socket.id);
        if (user) {
            const new_message = new Message(name, socket.id, text, picture, sound);
            io.to(user.room).emit('message', new_message);
            const room = rooms.find(r => r.id === user.room);
            room.messages.push(new_message);
        }
    });

    socket.on('disconnect', () => {
        const index = users.findIndex(u => u.id === socket.id);
        
        if (index !== -1) {
            const { id, username, room } = users[index];
            const prevRoom = rooms.find(r => r.id === room);
            if (prevRoom && prevRoom.users > 0) {
                prevRoom.users--;
            }
            users.splice(index, 1);
            io.to(room).emit('message', new Message('Admin', 'Admin', `${username} left`, null));
            prevRoom.messages.push(new Message('Admin', 'Admin', `${username} left`, null));
            io.to(room).emit('userList', getUsersInRoom(room));
            
        }
        io.emit('roomList', rooms.map(room => room));
    });

    socket.on('activity', (username) => {
        const user = users.find(u => u.id === socket.id); 
        console.log('Activity:', socket.id);
        console.log(`Activity in room ${user.room} by ${username} ${user.id}`);
        if (user && user.room) { 
            socket.broadcast.to(user.room).emit('activity', username);
        } else {
            console.log(`Activity attempt by unknown or roomless user: ${socket.id}`);
        }
    });


    socket.on('createRoom', ({ roomname, ownername }) => {
        const chat = new Chat(generateGUID(), roomname, ownername);
        rooms.push(chat);
        io.emit('roomList', rooms.map(room => room));
        socket.emit('createdRoom',chat.id);   
    });
});

function getUsersInRoom(room) {
    return users.filter(u => u.room === room).map(user => user.username);
}

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server on port ${PORT}`));

