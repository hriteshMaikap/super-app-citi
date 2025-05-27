import { Redirect } from 'expo-router';

export default function ChatsTab() {
    // This will redirect to /chats (which renders app/chats/index.tsx)
    return <Redirect href="/chats" />;
}
