export type ChatMessage = {
    id: string;
    message: string;
    timestamp: string;
    fromMe: boolean;
};

export type Contact = {
    id: string;
    name: string;
    phoneNumber: string;
    image: string;
    chat: ChatMessage[];
};

export const CONTACTS_DATA: Contact[] = [
    {
        id: '1',
        name: 'George Alan',
        phoneNumber: '+1234567890',
        image: 'https://randomuser.me/api/portraits/men/1.jpg',
        chat: [
            { id: '1', message: 'Hey George!', timestamp: '2025-05-27T10:00:00Z', fromMe: true },
            { id: '2', message: 'Hi! How are you?', timestamp: '2025-05-27T10:02:00Z', fromMe: false },
        ],
    },
    {
        id: '2',
        name: 'John Paul',
        phoneNumber: '+1234567891',
        image: 'https://randomuser.me/api/portraits/men/2.jpg',
        chat: [
            { id: '1', message: 'Meeting at 5?', timestamp: '2025-05-27T09:15:00Z', fromMe: true },
            { id: '2', message: 'Sure. See you there!', timestamp: '2025-05-27T09:17:00Z', fromMe: false },
        ],
    },
    {
        id: '3',
        name: 'Safiya Fareena',
        phoneNumber: '+1234567892',
        image: 'https://randomuser.me/api/portraits/women/1.jpg',
        chat: [
            { id: '1', message: 'Can you send the notes?', timestamp: '2025-05-26T20:30:00Z', fromMe: false },
            { id: '2', message: 'Sent. Check your mail.', timestamp: '2025-05-26T20:31:00Z', fromMe: true },
        ],
    },
    {
        id: '4',
        name: 'Robert Allen',
        phoneNumber: '+1234567893',
        image: 'https://randomuser.me/api/portraits/men/3.jpg',
        chat: [
            { id: '1', message: 'Game night today?', timestamp: '2025-05-27T08:00:00Z', fromMe: false },
            { id: '2', message: 'Definitely! Let’s meet at 7.', timestamp: '2025-05-27T08:01:00Z', fromMe: true },
        ],
    },
    {
        id: '5',
        name: 'Epic Games',
        phoneNumber: '+1234567894',
        image: 'https://randomuser.me/api/portraits/men/4.jpg',
        chat: [
            { id: '1', message: 'Your free game is available!', timestamp: '2025-05-25T13:00:00Z', fromMe: false },
        ],
    },
    {
        id: '6',
        name: 'Scott Franklin',
        phoneNumber: '+1234567895',
        image: 'https://randomuser.me/api/portraits/men/5.jpg',
        chat: [
            { id: '1', message: 'Lunch tomorrow?', timestamp: '2025-05-26T18:45:00Z', fromMe: true },
            { id: '2', message: 'Let’s do it!', timestamp: '2025-05-26T18:47:00Z', fromMe: false },
        ],
    },
    {
        id: '7',
        name: 'Mohammed',
        phoneNumber: '+1234567896',
        image: 'https://randomuser.me/api/portraits/men/6.jpg',
        chat: [
            { id: '1', message: 'Project deadline is near.', timestamp: '2025-05-25T15:00:00Z', fromMe: false },
            { id: '2', message: 'I’ll finish the report today.', timestamp: '2025-05-25T15:10:00Z', fromMe: true },
        ],
    },
    {
        id: '8',
        name: 'Michael Scott',
        phoneNumber: '+1234567897',
        image: 'https://randomuser.me/api/portraits/men/7.jpg',
        chat: [
            { id: '1', message: 'That’s what she said.', timestamp: '2025-05-24T12:00:00Z', fromMe: false },
        ],
    },
    {
        id: '9',
        name: 'Paul David',
        phoneNumber: '+1234567898',
        image: 'https://randomuser.me/api/portraits/men/8.jpg',
        chat: [
            { id: '1', message: 'All set for the interview?', timestamp: '2025-05-27T07:00:00Z', fromMe: false },
            { id: '2', message: 'Yeah, prepping now!', timestamp: '2025-05-27T07:01:00Z', fromMe: true },
        ],
    },
    {
        id: '10',
        name: 'Tessa Wilson',
        phoneNumber: '+1234567899',
        image: 'https://randomuser.me/api/portraits/women/2.jpg',
        chat: [
            { id: '1', message: 'Wanna catch up this weekend?', timestamp: '2025-05-26T11:00:00Z', fromMe: true },
            { id: '2', message: 'Absolutely! Let’s do brunch.', timestamp: '2025-05-26T11:05:00Z', fromMe: false },
        ],
    },
    {
        id: '11',
        name: 'Linda Carter',
        phoneNumber: '+1234567800',
        image: 'https://randomuser.me/api/portraits/women/3.jpg',
        chat: [
            { id: '1', message: 'Happy Birthday! 🎉', timestamp: '2025-05-25T00:00:00Z', fromMe: true },
            { id: '2', message: 'Thank you!! 😊', timestamp: '2025-05-25T00:05:00Z', fromMe: false },
        ],
    },
    {
        id: '12',
        name: 'Samantha Lee',
        phoneNumber: '+1234567801',
        image: 'https://randomuser.me/api/portraits/women/4.jpg',
        chat: [
            { id: '1', message: 'Don’t forget the assignment.', timestamp: '2025-05-26T16:00:00Z', fromMe: false },
            { id: '2', message: 'I submitted it already.', timestamp: '2025-05-26T16:03:00Z', fromMe: true },
        ],
    },
    {
        id: '13',
        name: 'Kevin Brown',
        phoneNumber: '+1234567802',
        image: 'https://randomuser.me/api/portraits/men/9.jpg',
        chat: [
            { id: '1', message: 'Bro, the match was wild!', timestamp: '2025-05-27T00:00:00Z', fromMe: true },
            { id: '2', message: 'Insane! That last goal 😱', timestamp: '2025-05-27T00:02:00Z', fromMe: false },
        ],
    },
    {
        id: '14',
        name: 'Jessica Smith',
        phoneNumber: '+1234567803',
        image: 'https://randomuser.me/api/portraits/women/5.jpg',
        chat: [
            { id: '1', message: 'Wanna collaborate on that UX project?', timestamp: '2025-05-26T13:15:00Z', fromMe: true },
            { id: '2', message: 'Sure, send me the brief.', timestamp: '2025-05-26T13:20:00Z', fromMe: false },
        ],
    },
    {
        id: '15',
        name: 'David Johnson',
        phoneNumber: '+1234567804',
        image: 'https://randomuser.me/api/portraits/men/10.jpg',
        chat: [
            { id: '1', message: 'Call me when you’re free.', timestamp: '2025-05-25T18:00:00Z', fromMe: false },
            { id: '2', message: 'Will do tonight.', timestamp: '2025-05-25T18:05:00Z', fromMe: true },
        ],
    },
];
