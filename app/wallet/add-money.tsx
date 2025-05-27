import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';

export default function AddMoneyScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Add Money</Text>
            {/* Add your add money form here */}
            <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
                <Text style={styles.backText}>Back to Wallet</Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 24 },
    backBtn: { marginTop: 24, padding: 12, backgroundColor: '#007AFF', borderRadius: 8 },
    backText: { color: '#fff', fontWeight: 'bold', fontSize: 16 }
});
