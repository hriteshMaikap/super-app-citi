import { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Modal, Pressable, Image, TextInput, Linking } from 'react-native';
import { useRouter } from 'expo-router';

export default function ProfileScreen() {
    const router = useRouter();
    const [modalVisible, setModalVisible] = useState(false);
    const [contactModalVisible, setContactModalVisible] = useState(false);

    // Dummy user data (replace with real user data as needed)
    const user = {
        username: 'john_doe',
        email: 'ashishableo12@gmail.com',
        firstName: 'John',
        lastName: 'Doe',
        phone: '+91 8826745173',
        image: 'https://randomuser.me/api/portraits/men/1.jpg',
    };

    const handleSignOut = () => setModalVisible(true);

    const handleConfirmSignOut = () => {
        setModalVisible(false);
        router.replace('/(auth)/Login');
    };

    const handleCancelSignOut = () => {
        setModalVisible(false);
        router.replace('/(tabs)/home');
    };

    const handleFAQ = () => {
        router.push('/(tabs)/faq');
    };

    const handleContactUs = () => {
        setContactModalVisible(true);
    };

    const handleCloseContact = () => {
        setContactModalVisible(false);
    };

    // Optional: You can add a simple contact form or just contact info
    return (
        <View style={styles.container}>
            {/* Top half - User Details */}
            <View style={styles.profileBox}>
                <Image source={{ uri: user.image }} style={styles.profileImage} />
                <Text style={styles.name}>{user.firstName} {user.lastName}</Text>
                <Text style={styles.info}>Username: {user.username}</Text>
                <Text style={styles.info}>Email: {user.email}</Text>
                <Text style={styles.info}>Phone: {user.phone}</Text>
            </View>

            {/* Bottom half - Options */}
            <View style={styles.optionsBox}>
                <TouchableOpacity style={styles.optionBtn} onPress={handleFAQ}>
                    <Text style={styles.optionText}>FAQ</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.optionBtn} onPress={handleContactUs}>
                    <Text style={styles.optionText}>Contact Us</Text>
                </TouchableOpacity>
                <TouchableOpacity style={[styles.optionBtn, { backgroundColor: '#ff4d4d' }]} onPress={handleSignOut}>
                    <Text style={[styles.optionText, { color: '#fff' }]}>Sign Out</Text>
                </TouchableOpacity>
            </View>

            {/* Modal for Sign Out Confirmation */}
            <Modal
                transparent
                visible={modalVisible}
                animationType="fade"
                onRequestClose={() => setModalVisible(false)}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.modalBox}>
                        <Text style={styles.modalTitle}>Are you sure you want to sign out?</Text>
                        <View style={styles.modalButtons}>
                            <Pressable style={[styles.modalBtn, styles.yesBtn]} onPress={handleConfirmSignOut}>
                                <Text style={styles.yesText}>Yes</Text>
                            </Pressable>
                            <Pressable style={[styles.modalBtn, styles.noBtn]} onPress={handleCancelSignOut}>
                                <Text style={styles.noText}>No</Text>
                            </Pressable>
                        </View>
                    </View>
                </View>
            </Modal>

            {/* Modal for Contact Us */}
            <Modal
                transparent
                visible={contactModalVisible}
                animationType="fade"
                onRequestClose={handleCloseContact}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.contactModalBox}>
                        <Text style={styles.contactTitle}>Contact Us</Text>
                        <Text style={styles.contactInfo}>Email: ashishableo12@gmail.com</Text>
                        <Text style={styles.contactInfo}>Phone: +91 8826745173</Text>
                        <TouchableOpacity
                            onPress={() => Linking.openURL('mailto:support@example.com')}
                            style={styles.contactAction}
                        >
                            <Text style={styles.contactActionText}>Send Email</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            onPress={handleCloseContact}
                            style={[styles.contactAction, { backgroundColor: '#eee', marginTop: 12 }]}
                        >
                            <Text style={[styles.contactActionText, { color: '#007AFF' }]}>Close</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 24,
        backgroundColor: '#f9f9f9',
        justifyContent: 'flex-start',
    },
    profileBox: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 24,
        alignItems: 'center',
        marginBottom: 32,
        elevation: 2,
        shadowColor: '#000',
        shadowOpacity: 0.08,
        shadowRadius: 8,
        shadowOffset: { width: 0, height: 2 },
    },
    profileImage: {
        width: 90,
        height: 90,
        borderRadius: 45,
        marginBottom: 16,
        borderWidth: 2,
        borderColor: '#007AFF',
    },
    name: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    info: {
        fontSize: 16,
        color: '#444',
        marginBottom: 4,
    },
    optionsBox: {
        marginTop: 16,
    },
    optionBtn: {
        backgroundColor: '#eee',
        padding: 16,
        borderRadius: 8,
        marginBottom: 16,
        alignItems: 'center',
    },
    optionText: {
        fontSize: 18,
        fontWeight: '500',
        color: '#333',
    },
    // Modal styles
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.3)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalBox: {
        width: 300,
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 24,
        alignItems: 'center',
    },
    modalTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 24,
        textAlign: 'center',
    },
    modalButtons: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '100%',
    },
    modalBtn: {
        flex: 1,
        paddingVertical: 12,
        marginHorizontal: 8,
        borderRadius: 8,
        alignItems: 'center',
    },
    yesBtn: {
        backgroundColor: '#ff4d4d',
    },
    noBtn: {
        backgroundColor: '#eee',
    },
    yesText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
    noText: {
        color: '#333',
        fontWeight: 'bold',
        fontSize: 16,
    },
    // Contact modal
    contactModalBox: {
        width: 300,
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 24,
        alignItems: 'center',
    },
    contactTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 16,
    },
    contactInfo: {
        fontSize: 16,
        color: '#333',
        marginBottom: 8,
    },
    contactAction: {
        backgroundColor: '#007AFF',
        borderRadius: 8,
        paddingVertical: 10,
        paddingHorizontal: 18,
        marginTop: 8,
    },
    contactActionText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
});
