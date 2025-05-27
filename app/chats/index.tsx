import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Image, TextInput, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { CONTACTS_DATA } from '@/data/contactsData';
import { Ionicons } from '@expo/vector-icons';

export default function ChatListScreen() {
    const router = useRouter();
    const [search, setSearch] = useState('');
    const [filteredContacts, setFilteredContacts] = useState(CONTACTS_DATA);

    const handleSearch = (text: string) => {
        setSearch(text);
        if (!text.trim()) {
            setFilteredContacts(CONTACTS_DATA);
        } else {
            const lower = text.toLowerCase();
            setFilteredContacts(
                CONTACTS_DATA.filter(
                    c =>
                        c.name.toLowerCase().includes(lower) ||
                        c.phoneNumber.includes(lower)
                )
            );
        }
    };

    return (
        <View style={{ flex: 1, backgroundColor: '#fff' }}>
            {/* Top bar with back arrow and search */}
            <View style={styles.topBar}>
                <TouchableOpacity onPress={() => router.replace('/home')} style={styles.backButton}>
                    <Ionicons name="arrow-back" size={24} color="black" />
                </TouchableOpacity>
                <TextInput
                    style={styles.searchInput}
                    placeholder="Search name or number"
                    value={search}
                    onChangeText={handleSearch}
                    autoCapitalize="none"
                />
            </View>

            <FlatList
                data={filteredContacts}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <TouchableOpacity
                        onPress={() => router.push(`/chats/${item.id}`)}
                        style={styles.contactItem}
                    >
                        <Image source={{ uri: item.image }} style={styles.avatar} />
                        <View>
                            <Text style={styles.name}>{item.name}</Text>
                            <Text style={styles.phone}>{item.phoneNumber}</Text>
                        </View>
                    </TouchableOpacity>
                )}
                contentContainerStyle={{ paddingBottom: 20 }}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    topBar: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 10,
        backgroundColor: '#fff',
        borderBottomWidth: 1,
        borderBottomColor: '#eee',
    },
    backButton: {
        marginRight: 10,
        padding: 5,
    },
    searchInput: {
        flex: 1,
        height: 40,
        backgroundColor: '#f2f2f2',
        borderRadius: 20,
        paddingHorizontal: 15,
        fontSize: 16,
    },
    contactItem: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#f0f0f0',
    },
    avatar: {
        width: 48,
        height: 48,
        borderRadius: 24,
        marginRight: 12,
    },
    name: {
        fontSize: 16,
        fontWeight: 'bold',
    },
    phone: {
        color: 'gray',
    },
});
