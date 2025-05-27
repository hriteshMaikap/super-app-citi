import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import Animated, { FadeInUp } from 'react-native-reanimated';

export default function WelcomeScreen() {
    const router = useRouter();

    return (
        <View style={styles.container}>
            <Animated.Text entering={FadeInUp.delay(200)} style={styles.title}>
                Welcome!
            </Animated.Text>

            <Animated.View entering={FadeInUp.delay(400)} style={styles.buttonWrapper}>
                <TouchableOpacity style={styles.button} onPress={() => router.push('/(auth)/Login')}>
                    <Text style={styles.buttonText}>LOGIN</Text>
                </TouchableOpacity>
            </Animated.View>

            <Animated.View entering={FadeInUp.delay(600)} style={styles.buttonWrapper}>
                <TouchableOpacity style={[styles.button, styles.signupButton]} onPress={() => router.push('/(auth)/Signup')}>
                    <Text style={styles.buttonText}>SIGNUP</Text>
                </TouchableOpacity>
            </Animated.View>

            <Animated.View entering={FadeInUp.delay(800)} style={styles.buttonWrapper}>
                <TouchableOpacity style={[styles.button, styles.demoButton]} onPress={() => router.replace('/(tabs)/home')}>
                    <Text style={styles.buttonText}>DEMO APP</Text>
                </TouchableOpacity>
            </Animated.View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0f172a', // dark background
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    title: {
        fontSize: 40,
        color: '#facc15',
        fontWeight: 'bold',
        marginBottom: 50,
    },
    buttonWrapper: {
        width: '100%',
        marginBottom: 20,
    },
    button: {
        backgroundColor: '#f97316',
        paddingVertical: 14,
        borderRadius: 10,
        alignItems: 'center',
        width: '100%',
    },
    signupButton: {
        backgroundColor: '#2563eb', // teal
    },
    demoButton: {
        backgroundColor: '#10b981', // orange
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: '600',
    },
});
