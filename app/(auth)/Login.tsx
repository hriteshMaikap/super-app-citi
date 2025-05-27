import { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import { useRouter } from 'expo-router';

export default function LoginScreen() {
    const router = useRouter();
    const [credentials, setCredentials] = useState({
        username: '',
        password: '',
    });

    const handleLogin = () => {
        // Add your login logic here
        router.replace('/(tabs)/home'); // Redirect after successful login
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={{ flex: 1, justifyContent: 'center' }}
        >
            <View style={styles.container}>
                <Text style={styles.title}>Welcome Back</Text>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Username</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter username"
                        value={credentials.username}
                        onChangeText={text => setCredentials({ ...credentials, username: text })}
                        autoCapitalize="none"
                    />
                </View>

                <View style={styles.inputContainer}>
                    <Text style={styles.label}>Password</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Enter password"
                        value={credentials.password}
                        onChangeText={text => setCredentials({ ...credentials, password: text })}
                        secureTextEntry
                    />
                </View>

                <TouchableOpacity style={styles.forgotPassword} onPress={() => router.push('/ForgotPassword')}>
                    <Text style={styles.linkText}>Forgot Password?</Text>
                </TouchableOpacity>

                <Button title="Login" onPress={handleLogin} color="#007bff" />

                <View style={styles.signupLink}>
                    <Text>Don't have an account? </Text>
                    <TouchableOpacity onPress={() => router.push('/(auth)/Signup')}>
                        <Text style={styles.linkText}>Sign up</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
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
    forgotPassword: {
        alignItems: 'flex-end',
        marginBottom: 20,
    },
    signupLink: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginTop: 20,
    },
    linkText: {
        color: '#007bff',
        fontWeight: '500',
    },
});
