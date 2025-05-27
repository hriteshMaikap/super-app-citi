import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TextInput, StyleSheet, Image, FlatList, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { CONTACTS_DATA, Contact, ChatMessage } from '@/data/contactsData';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';

export default function ChatScreen() {
    const { id } = useLocalSearchParams();
    const contact: Contact | undefined = CONTACTS_DATA.find(c => c.id === id);
    const [messages, setMessages] = useState<ChatMessage[]>(contact?.chat ?? []);
    const [inputText, setInputText] = useState('');
    const router = useRouter();

    // FlatList ref
    const flatListRef = useRef<FlatList<ChatMessage>>(null);

    const handleSend = () => {
        if (inputText.trim() && contact) {
            const newMessage: ChatMessage = {
                id: Date.now().toString(),
                message: inputText,
                fromMe: true,
                timestamp: new Date().toISOString(),
            };

            setMessages(prev => [...prev, newMessage]);
            contact.chat.push(newMessage);
            setInputText('');
        }
    };

    // Scroll to bottom when messages change
    useEffect(() => {
        if (flatListRef.current && messages.length > 0) {
            flatListRef.current.scrollToEnd({ animated: true });
        }
    }, [messages]);

    const renderMessage = ({ item }: { item: ChatMessage }) => (
        <View style={[
            styles.messageContainer,
            item.fromMe ? styles.myMessage : styles.theirMessage
        ]}>
            <Text style={item.fromMe ? styles.myText : styles.theirText}>{item.message}</Text>
            <Text style={styles.timestamp}>
                {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </Text>
        </View>
    );

    if (!contact) {
        return (
            <View style={styles.centered}>
                <Text>Contact not found.</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {/* Top Bar */}
            <View style={styles.topBar}>
                <TouchableOpacity onPress={() => router.replace('/chats')} style={styles.backButton}>
                    <Ionicons name="arrow-back" size={24} color="black" />
                </TouchableOpacity>
                <Image source={{ uri: contact.image }} style={styles.contactImage} />
                <View style={styles.contactInfo}>
                    <Text style={styles.contactName}>{contact.name}</Text>
                    <Text style={styles.contactStatus}>Online</Text>
                </View>
                <View style={styles.actions}>
                    <TouchableOpacity style={styles.actionButton}>
                        <Ionicons name="call" size={24} color="#007AFF" />
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.actionButton}>
                        <MaterialIcons name="info" size={24} color="#007AFF" />
                    </TouchableOpacity>
                </View>
            </View>


            {/* Chat Messages */}
            <FlatList
                ref={flatListRef}
                data={messages}
                renderItem={renderMessage}
                keyExtractor={item => item.id}
                contentContainerStyle={styles.chatContainer}
                // DO NOT use inverted here!
            />

            {/* Input Area */}
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={styles.inputContainer}
            >
                <TextInput
                    style={styles.input}
                    placeholder="Type a message..."
                    value={inputText}
                    onChangeText={setInputText}
                    onSubmitEditing={handleSend}
                    multiline
                />
                <TouchableOpacity onPress={handleSend} style={styles.sendButton}>
                    <Ionicons name="send" size={24} color="white" />
                </TouchableOpacity>
            </KeyboardAvoidingView>
        </View>
    );
}

export const options = {
    tabBarStyle: { display: 'none' },
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F5F5',
    },
    centered: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    topBar: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 15,
        backgroundColor: 'white',
        borderBottomWidth: 1,
        borderBottomColor: '#E0E0E0',
    },
    backButton: {
        marginRight: 10,
    },
    contactImage: {
        width: 40,
        height: 40,
        borderRadius: 20,
        marginRight: 10,
    },
    contactInfo: {
        flex: 1,
    },
    contactName: {
        fontSize: 18,
        fontWeight: 'bold',
    },
    contactStatus: {
        color: '#4CAF50',
        fontSize: 14,
    },
    actions: {
        flexDirection: 'row',
        gap: 15,
    },
    actionButton: {
        padding: 5,
    },
    chatContainer: {
        padding: 15,
    },
    messageContainer: {
        maxWidth: '80%',
        marginVertical: 8,
        padding: 12,
        borderRadius: 15,
    },
    myMessage: {
        alignSelf: 'flex-end',
        backgroundColor: '#007AFF',
        borderBottomRightRadius: 5,
    },
    theirMessage: {
        alignSelf: 'flex-start',
        backgroundColor: '#E0E0E0',
        borderBottomLeftRadius: 5,
    },
    myText: {
        color: 'white',
        fontSize: 16,
    },
    theirText: {
        color: 'black',
        fontSize: 16,
    },
    timestamp: {
        fontSize: 12,
        color: '#BDBDBD',
        marginTop: 5,
        alignSelf: 'flex-end',
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 15,
        backgroundColor: 'white',
        borderTopWidth: 1,
        borderTopColor: '#E0E0E0',
    },
    input: {
        flex: 1,
        backgroundColor: '#F5F5F5',
        borderRadius: 25,
        paddingHorizontal: 20,
        paddingVertical: 10,
        marginRight: 10,
        maxHeight: 100,
    },
    sendButton: {
        backgroundColor: '#007AFF',
        borderRadius: 25,
        width: 45,
        height: 45,
        justifyContent: 'center',
        alignItems: 'center',
    },
});
