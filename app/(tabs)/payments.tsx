import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, TextInput, Alert, ScrollView, ActivityIndicator, Modal } from 'react-native';
import { Ionicons, MaterialCommunityIcons, FontAwesome5, MaterialIcons } from '@expo/vector-icons';

const paymentOptions = [
    { key: 'upi', label: 'UPI', icon: <MaterialCommunityIcons name="bank-transfer" size={24} color="#007AFF" /> },
    { key: 'card', label: 'Credit/Debit Card', icon: <FontAwesome5 name="credit-card" size={22} color="#007AFF" /> },
    { key: 'netbanking', label: 'Net Banking', icon: <MaterialIcons name="language" size={24} color="#007AFF" /> },
    { key: 'wallet', label: 'Wallet', icon: <Ionicons name="wallet" size={24} color="#007AFF" /> },
    { key: 'cod', label: 'Cash on Delivery', icon: <MaterialCommunityIcons name="cash" size={24} color="#007AFF" /> },
];

export default function PaymentsScreen() {
    const [selected, setSelected] = useState('upi');
    const [upiId, setUpiId] = useState('');
    const [amount, setAmount] = useState('');
    const [cardNumber, setCardNumber] = useState('');
    const [cardExpiry, setCardExpiry] = useState('');
    const [cardCvv, setCardCvv] = useState('');
    const [wallet, setWallet] = useState('');
    const [loading, setLoading] = useState(false);
    const [paymentFailed, setPaymentFailed] = useState(false);
    const [qrModal, setQrModal] = useState(false);

    const handlePay = () => {
        setLoading(true);
        setPaymentFailed(false);
        setTimeout(() => {
            setLoading(false);
            setPaymentFailed(true);
        }, 2000);
    };

    const handleScanQR = () => {
        setQrModal(true);
    };

    if (loading) {
        return (
            <View style={styles.centered}>
                <ActivityIndicator size="large" color="#0d7f3f" />
                <Text style={{ marginTop: 18, fontSize: 18, color: '#333' }}>Processing your payment...</Text>
            </View>
        );
    }

    if (paymentFailed) {
        return (
            <View style={styles.centered}>
                <Ionicons name="close-circle" size={64} color="#ff3b30" />
                <Text style={styles.paymentFailedText}>Payment Failed</Text>
                <Text style={styles.paymentFailedSubText}>No payment method added yet.</Text>
                <TouchableOpacity style={styles.retryButton} onPress={() => setPaymentFailed(false)}>
                    <Text style={styles.retryButtonText}>Try Again</Text>
                </TouchableOpacity>
            </View>
        );
    }

    return (
        <ScrollView contentContainerStyle={styles.container}>
            {/* Scan QR Option */}
            <TouchableOpacity style={styles.qrOption} onPress={handleScanQR}>
                <Ionicons name="qr-code-outline" size={26} color="#007AFF" style={{ marginRight: 10 }} />
                <Text style={styles.qrOptionText}>Scan QR</Text>
            </TouchableOpacity>

            {/* QR Modal */}
            <Modal
                visible={qrModal}
                transparent
                animationType="fade"
                onRequestClose={() => setQrModal(false)}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.qrModalBox}>
                        <Ionicons name="qr-code-outline" size={48} color="#007AFF" style={{ marginBottom: 12 }} />
                        <Text style={styles.modalTitle}>IN PROCESS, try later</Text>
                        <TouchableOpacity style={styles.modalCloseBtn} onPress={() => setQrModal(false)}>
                            <Text style={styles.modalCloseText}>OK</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>

            <Text style={styles.title}>Select Payment Method</Text>
            {paymentOptions.map(opt => (
                <TouchableOpacity
                    key={opt.key}
                    style={[styles.option, selected === opt.key && styles.selectedOption]}
                    onPress={() => setSelected(opt.key)}
                >
                    {opt.icon}
                    <Text style={styles.optionLabel}>{opt.label}</Text>
                    {selected === opt.key && <Ionicons name="checkmark-circle" size={22} color="#0d7f3f" style={{ marginLeft: 'auto' }} />}
                </TouchableOpacity>
            ))}

            {/* UPI Form */}
            {selected === 'upi' && (
                <View style={styles.form}>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter UPI ID"
                        value={upiId}
                        onChangeText={setUpiId}
                        autoCapitalize="none"
                    />
                    <TextInput
                        style={styles.input}
                        placeholder="Amount"
                        keyboardType="numeric"
                        value={amount}
                        onChangeText={setAmount}
                    />
                </View>
            )}

            {/* Card Form */}
            {selected === 'card' && (
                <View style={styles.form}>
                    <TextInput
                        style={styles.input}
                        placeholder="Card Number"
                        keyboardType="numeric"
                        value={cardNumber}
                        onChangeText={setCardNumber}
                        maxLength={16}
                    />
                    <View style={{ flexDirection: 'row', gap: 8 }}>
                        <TextInput
                            style={[styles.input, { flex: 1 }]}
                            placeholder="MM/YY"
                            value={cardExpiry}
                            onChangeText={setCardExpiry}
                            maxLength={5}
                        />
                        <TextInput
                            style={[styles.input, { flex: 1 }]}
                            placeholder="CVV"
                            keyboardType="numeric"
                            value={cardCvv}
                            onChangeText={setCardCvv}
                            maxLength={3}
                            secureTextEntry
                        />
                    </View>
                    <TextInput
                        style={styles.input}
                        placeholder="Amount"
                        keyboardType="numeric"
                        value={amount}
                        onChangeText={setAmount}
                    />
                </View>
            )}

            {/* Net Banking */}
            {selected === 'netbanking' && (
                <View style={styles.form}>
                    <Text style={{ color: '#888', marginBottom: 10 }}>You will be redirected to your bank's secure page.</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Amount"
                        keyboardType="numeric"
                        value={amount}
                        onChangeText={setAmount}
                    />
                </View>
            )}

            {/* Wallet */}
            {selected === 'wallet' && (
                <View style={styles.form}>
                    <TextInput
                        style={styles.input}
                        placeholder="Wallet Name (e.g. Paytm, PhonePe)"
                        value={wallet}
                        onChangeText={setWallet}
                    />
                    <TextInput
                        style={styles.input}
                        placeholder="Amount"
                        keyboardType="numeric"
                        value={amount}
                        onChangeText={setAmount}
                    />
                </View>
            )}

            {/* COD */}
            {selected === 'cod' && (
                <View style={styles.form}>
                    <Text style={{ color: '#888', marginBottom: 10 }}>You will pay when the order is delivered.</Text>
                </View>
            )}

            <TouchableOpacity style={styles.payBtn} onPress={handlePay}>
                <Text style={styles.payBtnText}>
                    {selected === 'cod' ? 'Place Order' : 'Pay Now'}
                </Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: { flexGrow: 1, padding: 20, backgroundColor: '#fff' },
    qrOption: {
        flexDirection: 'row',
        alignItems: 'center',
        alignSelf: 'flex-start',
        marginBottom: 18,
        paddingVertical: 8,
        paddingHorizontal: 12,
        borderRadius: 8,
        backgroundColor: '#eaf1ff',
    },
    qrOptionText: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#007AFF',
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.25)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    qrModalBox: {
        width: 280,
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 24,
        alignItems: 'center',
    },
    modalTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#007AFF',
        marginBottom: 10,
        textAlign: 'center',
    },
    modalCloseBtn: {
        backgroundColor: '#007AFF',
        borderRadius: 8,
        paddingVertical: 10,
        paddingHorizontal: 32,
        marginTop: 14,
    },
    modalCloseText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
    title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
    option: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#f2f2f2',
        padding: 14,
        borderRadius: 10,
        marginBottom: 12,
    },
    selectedOption: {
        borderColor: '#0d7f3f',
        borderWidth: 2,
        backgroundColor: '#eafbe7',
    },
    optionLabel: {
        fontSize: 18,
        marginLeft: 12,
        color: '#333',
        fontWeight: '500',
    },
    form: { marginVertical: 16 },
    input: {
        backgroundColor: '#f9f9f9',
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        marginBottom: 12,
        borderWidth: 1,
        borderColor: '#eee',
    },
    payBtn: {
        backgroundColor: '#0d7f3f',
        borderRadius: 10,
        paddingVertical: 16,
        alignItems: 'center',
        marginTop: 12,
        elevation: 2,
    },
    payBtnText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 18,
        letterSpacing: 0.5,
    },
    centered: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#fff',
    },
    paymentFailedText: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#ff3b30',
        marginTop: 16,
    },
    paymentFailedSubText: {
        fontSize: 16,
        color: '#666',
        marginTop: 8,
        textAlign: 'center',
        paddingHorizontal: 20,
    },
    retryButton: {
        marginTop: 24,
        backgroundColor: '#007AFF',
        paddingVertical: 12,
        paddingHorizontal: 32,
        borderRadius: 8,
    },
    retryButtonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
});
