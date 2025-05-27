import { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { useRouter } from 'expo-router';

export default function SignupScreen() {
    const router = useRouter();
    const [form, setForm] = useState({
        email: '',
        username: '',
        firstName: '',
        lastName: '',
        phone: '',
        password: '',
    });

    const handleSignup = () => {
        // Add your signup logic here
        router.replace('/(tabs)/home'); // Redirect after successful signup
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={{ flex: 1 }}
        >
            <ScrollView contentContainerStyle={styles.container}>
                <Text style={styles.title}>Create Account</Text>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Email</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter email"
                        value={form.email}
                        onChangeText={text => setForm({ ...form, email: text })}
                        keyboardType="email-address"
                        autoCapitalize="none"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Username</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Choose username"
                        value={form.username}
                        onChangeText={text => setForm({ ...form, username: text })}
                        autoCapitalize="none"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>First Name</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter first name"
                        value={form.firstName}
                        onChangeText={text => setForm({ ...form, firstName: text })}
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Last Name</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter last name"
                        value={form.lastName}
                        onChangeText={text => setForm({ ...form, lastName: text })}
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Phone Number</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter phone number"
                        value={form.phone}
                        onChangeText={text => setForm({ ...form, phone: text })}
                        keyboardType="phone-pad"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Password</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Create password"
                        value={form.password}
                        onChangeText={text => setForm({ ...form, password: text })}
                        secureTextEntry
                    />
                </View>

                <Button title="Sign Up" onPress={handleSignup} color="#007bff" />

                <View style={styles.loginLink}>
                    <Text>Already have an account? </Text>
                    <TouchableOpacity onPress={() => router.push('/(auth)/Login')}>
                        <Text style={styles.linkText}>Login here</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        justifyContent: 'center',
        padding: 20,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 30,
        textAlign: 'center',
    },
    inputContainer: {
        marginBottom: 15,
    },
    label: {
        marginBottom: 5,
        color: '#333',
    },
    input: {
        height: 40,
        borderColor: '#ddd',
        borderWidth: 1,
        borderRadius: 5,
        paddingHorizontal: 10,
    },
    loginLink: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginTop: 20,
    },
    linkText: {
        color: '#007bff',
        fontWeight: '500',
    },
});
