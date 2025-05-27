import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function PaymentScreen() {
    const router = useRouter();

    return (
        <SafeAreaView style={styles.container}>
            {/* Back Button */}
            <TouchableOpacity style={styles.backButton} onPress={() => router.replace('/shopping')}>
                <Ionicons name="arrow-back" size={26} color="#007AFF" />
                <Text style={styles.backText}>Back to Shopping</Text>
            </TouchableOpacity>

            <Text style={styles.title}>Payment Page</Text>
            <Text style={styles.info}>This is where your payment form or summary will go.</Text>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        paddingTop: 48,
    },
    backButton: {
        flexDirection: 'row',
        alignItems: 'center',
        alignSelf: 'flex-start',
        marginLeft: 16,
        marginBottom: 32,
    },
    backText: {
        color: '#007AFF',
        fontSize: 16,
        fontWeight: 'bold',
        marginLeft: 4,
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        marginBottom: 16,
        textAlign: 'center',
    },
    info: {
        fontSize: 16,
        color: '#555',
        textAlign: 'center',
        paddingHorizontal: 32,
    },
});
